import logging
import threading

import pystray

from ui.IconFactory import IconFactory
from ui.UiAction import UiAction


class TrayIcon:

	LOGGER = logging.getLogger(__name__)
	ICON_NAME = "KTOPIA"
	TOOLTIP = "K-TOPIA Launcher"
	ICON_SIZE = 64
	MENU_OPEN = "열기(&O)"
	MENU_TASK_LIST = "작업목록(&T)"
	MENU_CONFIG = "설정(&C)"
	MENU_EXIT = "종료"

	def __init__(self, oLauncher):
		self.m_oLauncher = oLauncher
		self.m_oIcon = None
		self.m_oThread = None

	def start(self):
		oImage = IconFactory.createImage(TrayIcon.ICON_SIZE)
		oMenu = pystray.Menu(
			pystray.MenuItem(TrayIcon.MENU_OPEN, self._onOpen, default=True),
			pystray.MenuItem(TrayIcon.MENU_TASK_LIST, self._onTaskList),
			pystray.MenuItem(TrayIcon.MENU_CONFIG, self._onConfig),
			pystray.Menu.SEPARATOR,
			pystray.MenuItem(TrayIcon.MENU_EXIT, self._onExit),
		)
		self.m_oIcon = pystray.Icon(TrayIcon.ICON_NAME, oImage, TrayIcon.TOOLTIP, oMenu)
		self.m_oThread = threading.Thread(target=self.m_oIcon.run, name="TrayIcon", daemon=True)
		self.m_oThread.start()

	def stop(self):
		if self.m_oIcon is not None:
			self.m_oIcon.stop()
			self.m_oIcon = None

	def _onOpen(self, oIcon, oItem):
		self.m_oLauncher.postUiAction(UiAction.OPEN, None)

	def _onTaskList(self, oIcon, oItem):
		self.m_oLauncher.postUiAction(UiAction.TASK_LIST, None)

	def _onConfig(self, oIcon, oItem):
		self.m_oLauncher.postUiAction(UiAction.CONFIG, None)

	def _onExit(self, oIcon, oItem):
		self.m_oLauncher.postUiAction(UiAction.EXIT, None)
