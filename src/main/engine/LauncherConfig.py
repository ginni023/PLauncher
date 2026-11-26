import logging
import os

from util.PathUtil import PathUtil
from util.PropertiesUtil import PropertiesUtil
from util.StringUtil import StringUtil


class LauncherConfig:

	LOGGER = logging.getLogger(__name__)
	FILE_NAME = "config.properties"
	FILE_HEADER = "K-TOPIA Launcher configuration"
	LAUNCHER_VERSION = "0.1.0"
	YES = "Y"
	NO = "N"

	RESERVATION_SYSTEM = "RESERVATION_SYSTEM"
	INSTALL_PATH = "INSTALL_PATH"
	LINK_REGST_IND = "LINK_REGST_IND"
	RESERVATION_USE = "RESERVATION_USE"
	DEV_TRTR_ID = "DEV_TRTR_ID"
	NODEJS_PATH = "NODEJS_PATH"
	PLAYWRIGHT_PATH = "PLAYWRIGHT_PATH"
	MINIMIZE_IND = "MINIMIZE_IND"
	SAVE_PATH = "SAVE_PATH"
	RESERVATION_CHECK_TIME = "RESERVATION_CHECK_TIME"

	KEY_ORDER = (
		RESERVATION_SYSTEM, INSTALL_PATH, LINK_REGST_IND, RESERVATION_USE, DEV_TRTR_ID,
		NODEJS_PATH, PLAYWRIGHT_PATH, MINIMIZE_IND, SAVE_PATH, RESERVATION_CHECK_TIME,
	)
	AUTO_PATH_KEYS = (INSTALL_PATH, NODEJS_PATH, PLAYWRIGHT_PATH, SAVE_PATH)
	FLAG_KEYS = (LINK_REGST_IND, RESERVATION_USE, MINIMIZE_IND)

	DEFAULT_RESERVATION_SYSTEM = "http://www.ktopia.co.kr"
	DEFAULT_RESERVATION_CHECK_TIME = 5
	NODEJS_DIR_NAME = "node"
	PLAYWRIGHT_DIR_NAME = "playwright"
	SAVE_DIR_NAME = "screenShot"

	def __init__(self):
		self.m_mapValues = {}
		self.m_bCreated = False

	@staticmethod
	def getConfigPath():
		return os.path.join(PathUtil.getAppDir(), LauncherConfig.FILE_NAME)

	@staticmethod
	def getDefaultValues():
		strAppDir = PathUtil.getAppDir()
		mapDefaults = {}
		mapDefaults[LauncherConfig.RESERVATION_SYSTEM] = LauncherConfig.DEFAULT_RESERVATION_SYSTEM
		mapDefaults[LauncherConfig.INSTALL_PATH] = strAppDir
		mapDefaults[LauncherConfig.LINK_REGST_IND] = LauncherConfig.YES
		mapDefaults[LauncherConfig.RESERVATION_USE] = LauncherConfig.NO
		mapDefaults[LauncherConfig.DEV_TRTR_ID] = ""
		mapDefaults[LauncherConfig.NODEJS_PATH] = os.path.join(strAppDir, LauncherConfig.NODEJS_DIR_NAME)
		mapDefaults[LauncherConfig.PLAYWRIGHT_PATH] = os.path.join(strAppDir, LauncherConfig.PLAYWRIGHT_DIR_NAME)
		mapDefaults[LauncherConfig.MINIMIZE_IND] = LauncherConfig.NO
		mapDefaults[LauncherConfig.SAVE_PATH] = os.path.join(strAppDir, LauncherConfig.SAVE_DIR_NAME)
		mapDefaults[LauncherConfig.RESERVATION_CHECK_TIME] = str(LauncherConfig.DEFAULT_RESERVATION_CHECK_TIME)
		return mapDefaults

	def load(self):
		strPath = LauncherConfig.getConfigPath()
		mapDefaults = LauncherConfig.getDefaultValues()
		if not os.path.isfile(strPath):
			self.m_mapValues = mapDefaults
			self.m_bCreated = True
			self.save()
			LauncherConfig.LOGGER.info("config created with defaults : %s", strPath)
			return
		mapLoaded = PropertiesUtil.load(strPath)
		bChanged = False
		for strKey in LauncherConfig.KEY_ORDER:
			if strKey not in mapLoaded:
				mapLoaded[strKey] = mapDefaults[strKey]
				bChanged = True
		for strKey in LauncherConfig.AUTO_PATH_KEYS:
			if mapLoaded[strKey] != mapDefaults[strKey]:
				mapLoaded[strKey] = mapDefaults[strKey]
				bChanged = True
		self.m_mapValues = mapLoaded
		if bChanged:
			self.save()

	def save(self):
		PropertiesUtil.store(LauncherConfig.getConfigPath(), self.m_mapValues, LauncherConfig.KEY_ORDER,
							 LauncherConfig.FILE_HEADER)

	def isCreated(self):
		return self.m_bCreated

	def getValue(self, strKey):
		return self.m_mapValues.get(strKey, "")

	def setValue(self, strKey, strValue):
		self.m_mapValues[strKey] = strValue

	def copyValues(self):
		return dict(self.m_mapValues)

	def isYes(self, strKey):
		return StringUtil.equalsIgnoreCase(self.getValue(strKey), LauncherConfig.YES)

	def getReservationCheckMinutes(self):
		strValue = self.getValue(LauncherConfig.RESERVATION_CHECK_TIME)
		if StringUtil.isPositiveInteger(strValue):
			return int(strValue)
		return LauncherConfig.DEFAULT_RESERVATION_CHECK_TIME
