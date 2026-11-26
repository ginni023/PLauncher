import os

from engine.LauncherConfig import LauncherConfig


class LauncherEnvironment:

	NODE_EXE_NAME = "node.exe"
	NODE_MODULES_DIR_NAME = "node_modules"
	PLAYWRIGHT_SCOPE_DIR_NAME = "@playwright"
	PLAYWRIGHT_TEST_DIR_NAME = "test"
	PACKAGE_JSON_NAME = "package.json"

	def __init__(self):
		raise TypeError("LauncherEnvironment cannot be instantiated")

	@staticmethod
	def getNodeExePath(oConfig):
		return os.path.join(oConfig.getValue(LauncherConfig.NODEJS_PATH), LauncherEnvironment.NODE_EXE_NAME)

	@staticmethod
	def getPlaywrightPackagePath(oConfig):
		return os.path.join(oConfig.getValue(LauncherConfig.PLAYWRIGHT_PATH), LauncherEnvironment.NODE_MODULES_DIR_NAME,
							LauncherEnvironment.PLAYWRIGHT_SCOPE_DIR_NAME, LauncherEnvironment.PLAYWRIGHT_TEST_DIR_NAME,
							LauncherEnvironment.PACKAGE_JSON_NAME)

	@staticmethod
	def isNodeInstalled(oConfig):
		return os.path.isfile(LauncherEnvironment.getNodeExePath(oConfig))

	@staticmethod
	def isPlaywrightInstalled(oConfig):
		return os.path.isfile(LauncherEnvironment.getPlaywrightPackagePath(oConfig))
