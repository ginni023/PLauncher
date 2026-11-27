import logging
import os
import threading

from crawling import CrawlerConfig
from crawling import CrawlerEngine
from crawling import LoginResult
from crawling import Status

from database.TestCommDAO import TestCommDAO
from dto.TestCommDTO import TestCommDTO
from engine.LaunchUrlParser import LaunchUrlParser
from engine.SystemApiClient import SystemApiClient
from task.code.TaskResult import TaskResult
from task.code.TaskStatus import TaskStatus
from util.DateUtil import DateUtil
from util.PathUtil import PathUtil
from util.StringUtil import StringUtil


class CrawlingRunner:

	LOGGER = logging.getLogger(__name__)
	CRAWLER_CONFIG_FILE_NAME = "crawler.properties"
	KEY_SYSTEM_NM = "systemNm"
	KEY_SYSTEM_URL = "systemUrl"
	KEY_LOGIN_YN = "loginYn"
	LOGIN_YES = "Y"
	UPR_DIV_KEY_SYSTEM_INFO = "PL_UI_SYSTEM_INFO"
	META_VALUE_NO_LOGIN = "loginYn:N,expMin:0"
	META_VALUE_LOGIN = "loginYn:Y,expMin:20"
	VALUE_DESC_SESSION_PREFIX = "sessionSaveDt:"
	CANCEL_CHECK_SECONDS = 0.5
	SUCCESS_STATUSES = (Status.COMPLETED, Status.MAX_STATES)
	ERROR_NO_SYSTEM_URL = "서버 정보에 시스템 URL(systemUrl)이 없습니다."
	ERROR_LOGIN_FAILED = "로그인 실패 : "
	ERROR_CRAWL_FAILED = "크롤링 실패 : "
	MESSAGE_SEND = "보내기"

	def __init__(self, oTask, oConfig, oStopEvent, oTaskManager):
		self.m_oTask = oTask
		self.m_oConfig = oConfig
		self.m_oStopEvent = oStopEvent
		self.m_oTaskManager = oTaskManager
		self.m_mapServerData = {}
		self.m_oEngine = None
		self.m_oDoneEvent = None

	@staticmethod
	def run(oTask, oConfig, oStopEvent, oTaskManager):
		oRunner = CrawlingRunner(oTask, oConfig, oStopEvent, oTaskManager)
		oRunner.execute()

	def initMembers(self):
		self.m_mapServerData = {}
		self.m_oEngine = None
		self.m_oDoneEvent = threading.Event()

	def execute(self):
		self.initMembers()
		try:
			self._executeSteps()
		finally:
			self.m_oDoneEvent.set()

	def _executeSteps(self):
		mapParams = LaunchUrlParser.parseParams(self.m_oTask.getStrTaskAdr())
		strDomain = LaunchUrlParser.getParam(mapParams, LaunchUrlParser.PARAM_DOMAIN)
		strSystemId = self.m_oTask.getStrChordId()
		strType = self.m_oTask.getStrTaskType()
		CrawlingRunner.LOGGER.info("crawling 2 server data : %s, %s, %s", strDomain, strSystemId, strType)
		mapData = SystemApiClient.getServerData(strDomain, strSystemId, strType)
		self._storeServerData(mapData)
		CrawlingRunner.LOGGER.info("crawling 3 parse : %s", self.m_mapServerData)
		if self._isStopped():
			return
		self._createEngine()
		strLoginYn = self._getServerValue(CrawlingRunner.KEY_LOGIN_YN)
		bLoginRequired = StringUtil.equalsIgnoreCase(strLoginYn, CrawlingRunner.LOGIN_YES)
		CrawlingRunner.LOGGER.info("crawling 4 login required : %s", bLoginRequired)
		if bLoginRequired:
			if not self._login():
				return
		else:
			self._saveSystemInfo(CrawlingRunner.META_VALUE_NO_LOGIN, None)
		if self._isStopped():
			return
		oResult = self._crawl(bLoginRequired)
		if oResult is None:
			return
		self._sendResult(strDomain, oResult)
		self.m_oTask.setStrTestResult(TaskResult.SUCCESS)
		self.m_oTask.setStrTestStatus(TaskStatus.CMP)

	def _storeServerData(self, mapData):
		for strKey in mapData:
			oValue = mapData[strKey]
			if oValue is None:
				self.m_mapServerData[strKey] = ""
			else:
				self.m_mapServerData[strKey] = str(oValue)
		strSystemUrl = self._getServerValue(CrawlingRunner.KEY_SYSTEM_URL)
		if StringUtil.isEmpty(strSystemUrl):
			raise ValueError(CrawlingRunner.ERROR_NO_SYSTEM_URL)
		self.m_oTask.setStrChordNm(self._getServerValue(CrawlingRunner.KEY_SYSTEM_NM))
		self.m_oTask.setStrChordSbst(strSystemUrl)

	def _createEngine(self):
		strConfigPath = os.path.join(PathUtil.getAppDir(), CrawlingRunner.CRAWLER_CONFIG_FILE_NAME)
		oCrawlerConfig = CrawlerConfig.load(strConfigPath)
		oCrawlerConfig.set_auth_dir(CrawlingRunner._toAppPath(oCrawlerConfig.get_auth_dir()))
		oCrawlerConfig.set_output_dir(CrawlingRunner._toAppPath(oCrawlerConfig.get_output_dir()))
		oCrawlerConfig.set_start_url(self._getServerValue(CrawlingRunner.KEY_SYSTEM_URL))
		self.m_oEngine = CrawlerEngine(oCrawlerConfig)
		oThread = threading.Thread(target=self._watchCancel, name="CrawlingCancelWatcher", daemon=True)
		oThread.start()

	def _watchCancel(self):
		while not self.m_oDoneEvent.wait(CrawlingRunner.CANCEL_CHECK_SECONDS):
			if self.m_oStopEvent.is_set():
				CrawlingRunner.LOGGER.info("crawling cancel : %s", self.m_oTask.getStrTaskId())
				self.m_oEngine.cancel()
				return

	def _login(self):
		strSystemUrl = self._getServerValue(CrawlingRunner.KEY_SYSTEM_URL)
		oLoginDoneEvent = self.m_oTaskManager.requestLogin(self.m_oTask)
		try:
			oLoginResult = self.m_oEngine.login(strSystemUrl, oLoginDoneEvent, self.m_oTask.getStrChordId())
		finally:
			self.m_oTaskManager.finishLogin(self.m_oTask)
		CrawlingRunner.LOGGER.info("crawling 4-2 login : %s", oLoginResult.value)
		if oLoginResult != LoginResult.SAVED:
			if not self._isStopped():
				strReason = oLoginResult.value + " " + self.m_oEngine.get_error_message()
				self._setFail(CrawlingRunner.ERROR_LOGIN_FAILED + strReason)
			return False
		strValueDesc = CrawlingRunner.VALUE_DESC_SESSION_PREFIX + DateUtil.getNowDateTime()
		self._saveSystemInfo(CrawlingRunner.META_VALUE_LOGIN, strValueDesc)
		return True

	def _crawl(self, bLoginRequired):
		strSystemUrl = self._getServerValue(CrawlingRunner.KEY_SYSTEM_URL)
		oResult = self.m_oEngine.crawl(strSystemUrl, bLoginRequired, None, None, self.m_oTask.getStrChordId())
		CrawlingRunner.LOGGER.info("crawling 5 crawl : %s (%s)", oResult.status.value, oResult.output_dir)
		if oResult.status in CrawlingRunner.SUCCESS_STATUSES:
			return oResult
		if not self._isStopped():
			self._setFail(CrawlingRunner.ERROR_CRAWL_FAILED + oResult.status.value + " " + oResult.message)
		return None

	def _sendResult(self, strDomain, oResult):
		strMessage = CrawlingRunner.MESSAGE_SEND + " : " + strDomain + " (" + str(oResult.output_dir) + ")"
		CrawlingRunner.LOGGER.info("crawling 6 %s", strMessage)
		print(strMessage)

	def _saveSystemInfo(self, strMetaValue, strValueDesc):
		oComm = TestCommDTO()
		oComm.setStrMetaKey(self.m_oTask.getStrChordId())
		oComm.setStrUprDivKey(CrawlingRunner.UPR_DIV_KEY_SYSTEM_INFO)
		oComm.setStrDisNm(self._getServerValue(CrawlingRunner.KEY_SYSTEM_NM))
		oComm.setStrAliasNm(self._getServerValue(CrawlingRunner.KEY_SYSTEM_URL))
		oComm.setStrMetaValue(strMetaValue)
		oComm.setStrValueDesc(strValueDesc)
		strNow = DateUtil.getNowDateTime()
		oSaved = TestCommDAO.selectTestComm(oComm)
		if oSaved is None:
			oComm.setStrSysRecdCretDt(strNow)
			TestCommDAO.insertTestComm(oComm)
		else:
			oComm.setStrSysRecdChgDt(strNow)
			TestCommDAO.updateTestComm(oComm)
		CrawlingRunner.LOGGER.info("crawling system info saved : %s (%s)", oComm.getStrMetaKey(), strMetaValue)

	def _setFail(self, strMessage):
		CrawlingRunner.LOGGER.warning("crawling fail : %s", strMessage)
		self.m_oTask.setStrTestResult(TaskResult.FAIL)
		self.m_oTask.setStrTestStatus(TaskStatus.FAIL)
		self.m_oTask.setStrErrMsg(strMessage)

	def _getServerValue(self, strKey):
		return self.m_mapServerData.get(strKey, "")

	def _isStopped(self):
		return self.m_oStopEvent.is_set()

	@staticmethod
	def _toAppPath(strPath):
		if os.path.isabs(strPath):
			return strPath
		strJoined = os.path.join(PathUtil.getAppDir(), strPath)
		return os.path.normpath(strJoined)
