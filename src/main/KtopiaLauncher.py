import logging
import queue

from database.DatabaseUtil import DatabaseUtil
from engine.LaunchUrlParser import LaunchUrlParser
from engine.LauncherConfig import LauncherConfig
from util.LogUtil import LogUtil
from task.ManageTestTaskList import ManageTestTaskList
from engine.ProtocolRegistry import ProtocolRegistry
from task.ReservationScheduler import ReservationScheduler
from engine.SingleInstanceServer import SingleInstanceServer
from util.StringUtil import StringUtil
from task.code.TaskStatus import TaskStatus
from ui.TrayIcon import TrayIcon
from ui.UiAction import UiAction
from ui.dialog.WorkDialog import WorkDialog


class KtopiaLauncher:

	LOGGER = logging.getLogger(__name__)
	POLL_INTERVAL_MS = 100
	MESSAGE_INVALID_URL = "잘못된 실행 주소 : "
	MESSAGE_CONFIG_APPLIED = "설정이 적용되었습니다."

	def __init__(self, lstArgs):
		self.m_lstArgs = lstArgs
		self.m_oUiQueue = queue.Queue()
		self.m_oConfig = LauncherConfig()
		self.m_oServer = None
		self.m_oTaskManager = None
		self.m_oScheduler = None
		self.m_oTray = None
		self.m_oWorkDialog = None
		self.m_bExiting = False

	def run(self):
		LogUtil.setup()
		strLaunchUrl = self._findLaunchUrl()
		self.m_oServer = SingleInstanceServer(self.onRemoteMessage)
		if not self.m_oServer.start():
			KtopiaLauncher.LOGGER.info("launcher already running, forward : %s", strLaunchUrl)
			SingleInstanceServer.sendToRunning(strLaunchUrl)
			return
		KtopiaLauncher.LOGGER.info("launcher start : %s", strLaunchUrl)
		self.m_oConfig.load()
		DatabaseUtil.initDb()
		ProtocolRegistry.applyConfig(self.m_oConfig)
		self.m_oTaskManager = ManageTestTaskList(self.m_oConfig, self.onTaskEvent)
		self.m_oScheduler = ReservationScheduler(self.m_oConfig, self.m_oTaskManager)
		self.m_oScheduler.start()
		self.m_oWorkDialog = WorkDialog(self)
		self.m_oWorkDialog.init()
		self.m_oTray = TrayIcon(self)
		self.m_oTray.start()
		if not StringUtil.isEmpty(strLaunchUrl):
			self.postUiAction(UiAction.LAUNCH_URL, strLaunchUrl)
		if self.m_oConfig.isCreated():
			self.postUiAction(UiAction.CONFIG, None)
		self.m_oWorkDialog.after(KtopiaLauncher.POLL_INTERVAL_MS, self._pollUiQueue)
		self.m_oWorkDialog.mainloop()
		KtopiaLauncher.LOGGER.info("launcher end")

	def getConfig(self):
		return self.m_oConfig

	def getTaskManager(self):
		return self.m_oTaskManager

	def postUiAction(self, strAction, oPayload):
		self.m_oUiQueue.put((strAction, oPayload))

	def onRemoteMessage(self, strMessage):
		if LaunchUrlParser.isLaunchUrl(strMessage):
			self.postUiAction(UiAction.LAUNCH_URL, strMessage)
			return
		self.postUiAction(UiAction.OPEN, None)

	def onTaskEvent(self, strEventType, oTask, strMessage):
		self.postUiAction(UiAction.TASK_EVENT, (strEventType, oTask, strMessage))

	def onConfigApplied(self):
		self.m_oWorkDialog.setStatusMessage(KtopiaLauncher.MESSAGE_CONFIG_APPLIED)

	def exitApplication(self):
		self.m_bExiting = True
		KtopiaLauncher.LOGGER.info("exit requested")
		if self.m_oTaskManager is not None:
			self.m_oTaskManager.shutdown()
		if self.m_oScheduler is not None:
			self.m_oScheduler.stop()
		if self.m_oTray is not None:
			self.m_oTray.stop()
		if self.m_oServer is not None:
			self.m_oServer.stop()
		self.m_oWorkDialog.destroy()

	def _findLaunchUrl(self):
		for strArg in self.m_lstArgs:
			if LaunchUrlParser.isLaunchUrl(strArg):
				return strArg
		return ""

	def _pollUiQueue(self):
		try:
			while not self.m_bExiting:
				try:
					arrItem = self.m_oUiQueue.get_nowait()
				except queue.Empty:
					break
				self._dispatchUiAction(arrItem[0], arrItem[1])
		finally:
			if not self.m_bExiting:
				self.m_oWorkDialog.after(KtopiaLauncher.POLL_INTERVAL_MS, self._pollUiQueue)

	def _dispatchUiAction(self, strAction, oPayload):
		if strAction == UiAction.OPEN:
			self.m_oWorkDialog.showWindow()
		elif strAction == UiAction.TASK_LIST:
			self.m_oWorkDialog.openTaskList()
		elif strAction == UiAction.CONFIG:
			self.m_oWorkDialog.openConfigDialog()
		elif strAction == UiAction.EXIT:
			self.exitApplication()
		elif strAction == UiAction.LAUNCH_URL:
			self._handleLaunchUrl(oPayload)
		elif strAction == UiAction.TASK_EVENT:
			self._handleTaskEvent(oPayload[0], oPayload[1], oPayload[2])

	def _handleLaunchUrl(self, strUrl):
		self.m_oWorkDialog.showWindow()
		try:
			oTask = LaunchUrlParser.parse(strUrl, self.m_oConfig.getValue(LauncherConfig.DEV_TRTR_ID))
		except ValueError as oException:
			KtopiaLauncher.LOGGER.warning("invalid launch url : %s (%s)", strUrl, oException)
			self.m_oWorkDialog.setStatusMessage(KtopiaLauncher.MESSAGE_INVALID_URL + str(oException), TaskStatus.ERR)
			return
		self.m_oTaskManager.addTask(oTask)

	def _handleTaskEvent(self, strEventType, oTask, strMessage):
		strStatus = None
		if oTask is not None:
			strStatus = oTask.getStrTestStatus()
		self.m_oWorkDialog.setStatusMessage(strMessage, strStatus)
		if strEventType == ManageTestTaskList.EVENT_STARTED:
			self.m_oWorkDialog.displayTask(oTask)
		elif strEventType == ManageTestTaskList.EVENT_FINISHED:
			if self.m_oWorkDialog.getDisplayedTask() is oTask:
				self.m_oWorkDialog.refreshDisplayedTask()
		self.m_oWorkDialog.refreshActiveDialog()
