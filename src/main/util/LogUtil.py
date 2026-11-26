import logging
import logging.handlers
import os

from util.PathUtil import PathUtil


class LogUtil:

	LOG_FILE_NAME = "ktopia.log"
	MAX_BYTES = 5 * 1024 * 1024
	BACKUP_COUNT = 5
	LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s : %(message)s"
	ENCODING = "utf-8"

	s_bInitialized = False

	def __init__(self):
		raise TypeError("LogUtil cannot be instantiated")

	@staticmethod
	def setup():
		if LogUtil.s_bInitialized:
			return
		strLogDir = PathUtil.getLogDir()
		os.makedirs(strLogDir, exist_ok=True)
		strLogPath = os.path.join(strLogDir, LogUtil.LOG_FILE_NAME)
		oHandler = logging.handlers.RotatingFileHandler(
			strLogPath, maxBytes=LogUtil.MAX_BYTES, backupCount=LogUtil.BACKUP_COUNT, encoding=LogUtil.ENCODING)
		oFormatter = logging.Formatter(LogUtil.LOG_FORMAT)
		oHandler.setFormatter(oFormatter)
		oRootLogger = logging.getLogger()
		oRootLogger.setLevel(logging.INFO)
		oRootLogger.addHandler(oHandler)
		LogUtil.s_bInitialized = True
