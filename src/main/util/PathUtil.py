import os
import sys


class PathUtil:

	RESOURCE_DIR_NAME = "resource"
	DB_DIR_NAME = "db"
	LOG_DIR_NAME = "log"
	SOURCE_DEPTH_FROM_ROOT = 3

	def __init__(self):
		raise TypeError("PathUtil cannot be instantiated")

	@staticmethod
	def getAppDir():
		if getattr(sys, "frozen", False):
			return os.path.dirname(sys.executable)
		strFilePath = os.path.abspath(__file__)
		strDir = os.path.dirname(strFilePath)
		for nIndex in range(PathUtil.SOURCE_DEPTH_FROM_ROOT):
			strDir = os.path.dirname(strDir)
		return strDir

	@staticmethod
	def getDbDir():
		strAppDir = PathUtil.getAppDir()
		return os.path.join(strAppDir, PathUtil.RESOURCE_DIR_NAME, PathUtil.DB_DIR_NAME)

	@staticmethod
	def getLogDir():
		strAppDir = PathUtil.getAppDir()
		return os.path.join(strAppDir, PathUtil.LOG_DIR_NAME)
