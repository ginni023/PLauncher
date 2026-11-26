import collections
import logging
import threading

from util.DateUtil import DateUtil
from util.StringUtil import StringUtil
from task.TaskRunner import TaskRunner
from task.code.TaskStatus import TaskStatus
from task.code.TaskType import TaskType
from database.TestTaskDAO import TestTaskDAO


class ManageTestTaskList:

	LOGGER = logging.getLogger(__name__)
	EVENT_ADDED = "ADDED"
	EVENT_RESERVED = "RESERVED"
	EVENT_STARTED = "STARTED"
	EVENT_FINISHED = "FINISHED"
	EVENT_IDLE = "IDLE"

	MESSAGE_ADDED = "작업 등록 : "
	MESSAGE_RESERVATION_ADDED = "예약 작업 등록 : "
	MESSAGE_RESERVED = "예약 작업 준비 : "
	MESSAGE_STARTED = "작업 수행 중 : "
	MESSAGE_FINISHED = "작업 종료 : "
	MESSAGE_IDLE = "대기 중"

	def __init__(self, oConfig, fnOnEvent):
		self.m_oConfig = oConfig
		self.m_fnOnEvent = fnOnEvent
		self.m_oLock = threading.RLock()
		self.m_oBasicQueue = collections.deque()
		self.m_oReservationQueue = collections.deque()
		self.m_lstPendingReservations = []
		self.m_bInterruptFlag = False
		self.m_oCurrentTask = None
		self.m_oStopEvent = None
		self.m_bShutdown = False

	@staticmethod
	def getTaskName(oTask):
		strName = oTask.getStrChordNm()
		if StringUtil.isEmpty(strName):
			strName = oTask.getStrChordId()
		if StringUtil.isEmpty(strName):
			strName = oTask.getStrTaskId()
		return strName

	def addTask(self, oTask):
		with self.m_oLock:
			oTask.setStrTestStatus(TaskStatus.RDY)
			TestTaskDAO.insertTestTask(oTask)
			if StringUtil.equalsIgnoreCase(oTask.getStrTaskType(), TaskType.RESERVATION):
				self.m_lstPendingReservations.append(oTask)
				self._notify(ManageTestTaskList.EVENT_ADDED, oTask, ManageTestTaskList.MESSAGE_RESERVATION_ADDED)
			else:
				self.m_oBasicQueue.append(oTask)
				self._notify(ManageTestTaskList.EVENT_ADDED, oTask, ManageTestTaskList.MESSAGE_ADDED)
		self.startTask()

	def checkReadyTasks(self):
		lstTasks = TestTaskDAO.selectReadyTaskList()
		nLoaded = 0
		with self.m_oLock:
			for oTask in lstTasks:
				if self._isKnownTask(oTask.getStrTaskId()):
					continue
				self.m_oBasicQueue.append(oTask)
				nLoaded += 1
		if nLoaded > 0:
			self.startTask()
		return nLoaded

	def checkReservedTasks(self):
		lstTasks = TestTaskDAO.selectPendingReservationList()
		nLoaded = 0
		with self.m_oLock:
			for oTask in lstTasks:
				if self._isKnownTask(oTask.getStrTaskId()):
					continue
				if StringUtil.equalsIgnoreCase(oTask.getStrTestStatus(), TaskStatus.WAIT):
					self.m_oReservationQueue.append(oTask)
					self.m_bInterruptFlag = True
				else:
					self.m_lstPendingReservations.append(oTask)
				nLoaded += 1
		self.checkReservations()
		self.startTask()
		return nLoaded

	def checkReservations(self):
		strNow = DateUtil.getNowDateTime()
		bQueued = False
		with self.m_oLock:
			lstRemain = []
			for oTask in self.m_lstPendingReservations:
				strReserveDate = oTask.getStrReserveDate()
				if StringUtil.isEmpty(strReserveDate) or strReserveDate <= strNow:
					oTask.setStrTestStatus(TaskStatus.WAIT)
					TestTaskDAO.updateTestTaskStatus(oTask)
					self.m_oReservationQueue.append(oTask)
					self.m_bInterruptFlag = True
					self._notify(ManageTestTaskList.EVENT_RESERVED, oTask, ManageTestTaskList.MESSAGE_RESERVED)
					bQueued = True
				else:
					lstRemain.append(oTask)
			self.m_lstPendingReservations = lstRemain
		if bQueued:
			self.startTask()

	def startTask(self):
		with self.m_oLock:
			if self.m_bShutdown:
				return False
			if self.m_oCurrentTask is not None:
				return False
			oQueue = None
			if len(self.m_oReservationQueue) > 0:
				oQueue = self.m_oReservationQueue
			else:
				self.m_bInterruptFlag = False
				if len(self.m_oBasicQueue) > 0:
					oQueue = self.m_oBasicQueue
			if oQueue is None:
				return False
			oTask = oQueue[0]
			oTask.setStrTestStatus(TaskStatus.WRK)
			oTask.setStrRunDate(DateUtil.getNowDateTime())
			TestTaskDAO.updateTestTaskStatus(oTask)
			oStopEvent = threading.Event()
			self.m_oCurrentTask = oTask
			self.m_oStopEvent = oStopEvent
			oThread = threading.Thread(target=self._runTask, args=(oTask, oQueue, oStopEvent),
									   name="TaskWorker", daemon=True)
			self._notify(ManageTestTaskList.EVENT_STARTED, oTask, ManageTestTaskList.MESSAGE_STARTED)
			oThread.start()
			return True

	def stopTask(self):
		with self.m_oLock:
			if self.m_oStopEvent is not None:
				self.m_oStopEvent.set()

	def shutdown(self):
		with self.m_oLock:
			self.m_bShutdown = True
			if self.m_oCurrentTask is None:
				return
			self.m_oStopEvent.set()
			self.m_oCurrentTask.setStrTestStatus(TaskStatus.STOP)
			TestTaskDAO.updateTestTaskStatus(self.m_oCurrentTask)

	def getCurrentTask(self):
		with self.m_oLock:
			return self.m_oCurrentTask

	def isInterrupted(self):
		with self.m_oLock:
			return self.m_bInterruptFlag

	def _runTask(self, oTask, oQueue, oStopEvent):
		try:
			TaskRunner.run(oTask, self.m_oConfig, oStopEvent)
		except Exception as oException:
			ManageTestTaskList.LOGGER.exception("task failed : %s", oTask.getStrTaskId())
			oTask.setStrTestStatus(TaskStatus.ERR)
			oTask.setStrErrMsg(str(oException))
		if oStopEvent.is_set():
			oTask.setStrTestStatus(TaskStatus.STOP)
		elif not TaskStatus.isFinished(oTask.getStrTestStatus()):
			oTask.setStrTestStatus(TaskStatus.CMP)
		self._finishTask(oTask, oQueue)

	def _finishTask(self, oTask, oQueue):
		with self.m_oLock:
			try:
				if not self.m_bShutdown:
					TestTaskDAO.updateTestTaskStatus(oTask)
			except Exception:
				ManageTestTaskList.LOGGER.exception("failed to save task result : %s", oTask.getStrTaskId())
			finally:
				if len(oQueue) > 0 and oQueue[0] is oTask:
					oQueue.popleft()
				self.m_oCurrentTask = None
				self.m_oStopEvent = None
				if oQueue is self.m_oReservationQueue and len(oQueue) == 0:
					self.m_bInterruptFlag = False
			strLabel = TaskStatus.getLabel(oTask.getStrTestStatus())
			self._notify(ManageTestTaskList.EVENT_FINISHED, oTask,
						 ManageTestTaskList.MESSAGE_FINISHED + strLabel + " - ")
			if self.m_bShutdown:
				return
		bStarted = self.startTask()
		if not bStarted:
			self._notify(ManageTestTaskList.EVENT_IDLE, None, ManageTestTaskList.MESSAGE_IDLE)

	def _isKnownTask(self, strTaskId):
		if self.m_oCurrentTask is not None and self.m_oCurrentTask.getStrTaskId() == strTaskId:
			return True
		for oQueue in (self.m_oBasicQueue, self.m_oReservationQueue, self.m_lstPendingReservations):
			for oTask in oQueue:
				if oTask.getStrTaskId() == strTaskId:
					return True
		return False

	def _notify(self, strEventType, oTask, strMessage):
		strText = strMessage
		if oTask is not None:
			strText = strMessage + ManageTestTaskList.getTaskName(oTask)
		self.m_fnOnEvent(strEventType, oTask, strText)
