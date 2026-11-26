import logging
import os
import sys
import winreg

from engine.LauncherConfig import LauncherConfig
from util.PathUtil import PathUtil
from util.StringUtil import StringUtil


class ProtocolRegistry:

	LOGGER = logging.getLogger(__name__)
	PROTOCOL_NAME = "ktopia"
	CLASSES_PATH = "Software\\Classes\\" + PROTOCOL_NAME
	COMMAND_PATH = CLASSES_PATH + "\\shell\\open\\command"
	ICON_PATH = CLASSES_PATH + "\\DefaultIcon"
	PROTOCOL_DESCRIPTION = "URL:ktopia Protocol"
	URL_PROTOCOL_VALUE_NAME = "URL Protocol"
	PYTHONW_FILE_NAME = "pythonw.exe"
	MAIN_SCRIPT_NAME = "main.py"

	def __init__(self):
		raise TypeError("ProtocolRegistry cannot be instantiated")

	@staticmethod
	def getExecutablePath():
		if getattr(sys, "frozen", False):
			return sys.executable
		strPythonDir = os.path.dirname(sys.executable)
		return os.path.join(strPythonDir, ProtocolRegistry.PYTHONW_FILE_NAME)

	@staticmethod
	def getCommand():
		strExecutable = ProtocolRegistry.getExecutablePath()
		if getattr(sys, "frozen", False):
			return "\"" + strExecutable + "\" \"%1\""
		strScript = os.path.join(PathUtil.getAppDir(), ProtocolRegistry.MAIN_SCRIPT_NAME)
		return "\"" + strExecutable + "\" \"" + strScript + "\" \"%1\""

	@staticmethod
	def getRegisteredCommand():
		try:
			oKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, ProtocolRegistry.COMMAND_PATH)
		except FileNotFoundError:
			return ""
		try:
			arrValue = winreg.QueryValueEx(oKey, "")
			return arrValue[0]
		finally:
			winreg.CloseKey(oKey)

	@staticmethod
	def isRegistered():
		return ProtocolRegistry.getRegisteredCommand() == ProtocolRegistry.getCommand()

	@staticmethod
	def register():
		strExecutable = ProtocolRegistry.getExecutablePath()
		ProtocolRegistry._setValue(ProtocolRegistry.CLASSES_PATH, "", ProtocolRegistry.PROTOCOL_DESCRIPTION)
		ProtocolRegistry._setValue(ProtocolRegistry.CLASSES_PATH, ProtocolRegistry.URL_PROTOCOL_VALUE_NAME, "")
		ProtocolRegistry._setValue(ProtocolRegistry.ICON_PATH, "", "\"" + strExecutable + "\",0")
		ProtocolRegistry._setValue(ProtocolRegistry.COMMAND_PATH, "", ProtocolRegistry.getCommand())
		ProtocolRegistry.LOGGER.info("ktopia:// protocol registered : %s", ProtocolRegistry.getCommand())

	@staticmethod
	def unregister():
		if StringUtil.isEmpty(ProtocolRegistry.getRegisteredCommand()):
			return
		ProtocolRegistry._deleteTree(winreg.HKEY_CURRENT_USER, ProtocolRegistry.CLASSES_PATH)
		ProtocolRegistry.LOGGER.info("ktopia:// protocol unregistered")

	@staticmethod
	def applyConfig(oConfig):
		if oConfig.isYes(LauncherConfig.LINK_REGST_IND):
			if not ProtocolRegistry.isRegistered():
				ProtocolRegistry.register()
			return
		ProtocolRegistry.unregister()

	@staticmethod
	def _setValue(strPath, strName, strValue):
		oKey = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, strPath, 0, winreg.KEY_WRITE)
		try:
			winreg.SetValueEx(oKey, strName, 0, winreg.REG_SZ, strValue)
		finally:
			winreg.CloseKey(oKey)

	@staticmethod
	def _deleteTree(oRootKey, strPath):
		oKey = winreg.OpenKey(oRootKey, strPath, 0, winreg.KEY_READ)
		lstSubKeys = []
		try:
			nIndex = 0
			nSubKeyCount = winreg.QueryInfoKey(oKey)[0]
			while nIndex < nSubKeyCount:
				lstSubKeys.append(winreg.EnumKey(oKey, nIndex))
				nIndex += 1
		finally:
			winreg.CloseKey(oKey)
		for strSubKey in lstSubKeys:
			ProtocolRegistry._deleteTree(oRootKey, strPath + "\\" + strSubKey)
		winreg.DeleteKey(oRootKey, strPath)
