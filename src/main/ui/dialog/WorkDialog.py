import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import ttkbootstrap as tb
from PIL import ImageTk

from database.DatabaseUtil import DatabaseUtil
from engine.LauncherConfig import LauncherConfig
from engine.LauncherEnvironment import LauncherEnvironment
from engine.SystemApiClient import SystemApiClient
from task.code.TaskStatus import TaskStatus
from ui.dialog.ConfigDialog import ConfigDialog
from ui.dialog.ErrorDialog import ErrorDialog
from ui.IconFactory import IconFactory
from ui.dialog.ReservationListDialog import ReservationListDialog
from ui.UiTheme import UiTheme
from util.StringUtil import StringUtil
from ui.dialog.TaskListDialog import TaskListDialog
from database.TestInfoDAO import TestInfoDAO


class WorkDialog(tb.Window):

	LOGGER = logging.getLogger(__name__)
	TITLE = "K-TOPIA Launcher"
	WIDTH = 640
	HEIGHT = 480
	PADDING = 12
	ICON_SIZE = 32
	CONTENT_LINES = 3
	LABEL_WIDTH = 10

	LABEL_TEST_NAME = "테스트 명"
	LABEL_TEST_CONTENT = "테스트 내용"
	BUTTON_RESERVATION_LIST = "예약목록"
	BUTTON_TASK_LIST = "작업목록"
	BUTTON_ERROR = "오류"
	STATUS_READY = "대기 중"
	INIT_DONE = "초기화 완료"
	INIT_NEW_VERSION = "새 버전 있음 : "
	INIT_NO_NODE = "Node.js 없음"
	INIT_NO_PLAYWRIGHT = "Playwright 없음"
	INIT_SEPARATOR = ", "

	COLUMN_NO = "no"
	COLUMN_NAME = "name"
	COLUMN_RESULT = "result"
	COLUMN_DEFS = (
		(COLUMN_NO, "No", 50, tk.CENTER),
		(COLUMN_NAME, "테스트명", 440, tk.W),
		(COLUMN_RESULT, "결과", 110, tk.CENTER),
	)

	def __init__(self, oLauncher):
		tb.Window.__init__(self, title=WorkDialog.TITLE, themename=UiTheme.THEME_NAME, iconphoto=None, high_dpi=False)
		self.m_oLauncher = oLauncher
		self.m_oDisplayedTask = None
		self.m_oActiveDialog = None
		self.m_oIconImage = None
		self.m_oTestNameVar = tk.StringVar(self)
		self.m_oStatusVar = tk.StringVar(self, WorkDialog.STATUS_READY)
		self.m_oStatusDot = None
		self.m_oContentText = None
		self.m_oTree = None
		self._initWindow()
		self._buildInfoArea()
		self._buildBottomArea()
		self._buildTableArea()

	def init(self):
		oConfig = self.m_oLauncher.getConfig()
		lstWarnings = []

		strCurrentVersion = LauncherConfig.LAUNCHER_VERSION
		strLatestVersion = SystemApiClient.fetchLatestVersion(oConfig.getValue(LauncherConfig.RESERVATION_SYSTEM),
															  strCurrentVersion)
		WorkDialog.LOGGER.info("init 1 version : current %s, latest %s", strCurrentVersion, strLatestVersion)
		if strLatestVersion != strCurrentVersion:
			lstWarnings.append(WorkDialog.INIT_NEW_VERSION + strLatestVersion)

		DatabaseUtil.initMappingQuery()
		WorkDialog.LOGGER.info("init 2 query mapping done")

		bNodeInstalled = LauncherEnvironment.isNodeInstalled(oConfig)
		WorkDialog.LOGGER.info("init 3 node : %s (%s)", bNodeInstalled, LauncherEnvironment.getNodeExePath(oConfig))
		if not bNodeInstalled:
			lstWarnings.append(WorkDialog.INIT_NO_NODE)

		bPlaywrightInstalled = LauncherEnvironment.isPlaywrightInstalled(oConfig)
		WorkDialog.LOGGER.info("init 4 playwright : %s (%s)", bPlaywrightInstalled,
							   LauncherEnvironment.getPlaywrightPackagePath(oConfig))
		if not bPlaywrightInstalled:
			lstWarnings.append(WorkDialog.INIT_NO_PLAYWRIGHT)

		oTaskManager = self.m_oLauncher.getTaskManager()
		nReadyTasks = oTaskManager.checkReadyTasks()
		WorkDialog.LOGGER.info("init 5 ready tasks : %d", nReadyTasks)

		nReservedTasks = oTaskManager.checkReservedTasks()
		WorkDialog.LOGGER.info("init 6 reserved tasks : %d", nReservedTasks)

		if len(lstWarnings) == 0:
			self.setStatusMessage(WorkDialog.INIT_DONE)
			return
		strWarnings = WorkDialog.INIT_SEPARATOR.join(lstWarnings)
		self.setStatusMessage(WorkDialog.INIT_DONE + " (" + strWarnings + ")", TaskStatus.STOP)

	def report_callback_exception(self, oExceptionType, oException, oTraceback):
		WorkDialog.LOGGER.error("ui error", exc_info=(oExceptionType, oException, oTraceback))
		messagebox.showerror(WorkDialog.TITLE, str(oException), parent=self)

	def showWindow(self):
		self.deiconify()
		self.lift()
		self.focus_force()
		if self.m_oActiveDialog is not None:
			self.m_oActiveDialog.bringToFront()

	def hideWindow(self):
		self.withdraw()

	def setStatusMessage(self, strMessage, strStatus=None):
		self.m_oStatusVar.set(strMessage)
		strColorName = UiTheme.getStatusColorName(strStatus)
		self.m_oStatusDot.configure(foreground=UiTheme.getColor(strColorName))

	def getDisplayedTask(self):
		return self.m_oDisplayedTask

	def displayTask(self, oTask):
		self.m_oDisplayedTask = oTask
		self._renderTask()

	def refreshDisplayedTask(self):
		self._renderTask()

	def refreshActiveDialog(self):
		if self.m_oActiveDialog is not None:
			self.m_oActiveDialog.refresh()

	def openReservationList(self):
		if self._prepareOpen():
			self._showDialog(ReservationListDialog(self, self.onChildDialogClosed))

	def openTaskList(self):
		if self._prepareOpen():
			self._showDialog(TaskListDialog(self, self.onChildDialogClosed))

	def openErrorDialog(self):
		if self._prepareOpen():
			self._showDialog(ErrorDialog(self, self.m_oDisplayedTask, self.onChildDialogClosed))

	def openConfigDialog(self):
		if self._prepareOpen():
			self._showDialog(ConfigDialog(self, self.m_oLauncher, self.onChildDialogClosed))

	def onChildDialogClosed(self, oDialog):
		if self.m_oActiveDialog is oDialog:
			self.m_oActiveDialog = None

	def _initWindow(self):
		self.geometry(str(WorkDialog.WIDTH) + "x" + str(WorkDialog.HEIGHT))
		self.resizable(False, False)
		self.protocol("WM_DELETE_WINDOW", self.hideWindow)
		UiTheme.apply(self)
		oImage = IconFactory.createImage(WorkDialog.ICON_SIZE)
		self.m_oIconImage = ImageTk.PhotoImage(oImage, master=self)
		self.iconphoto(True, self.m_oIconImage)

	def _buildInfoArea(self):
		oFrame = ttk.Frame(self, padding=(WorkDialog.PADDING + 6, WorkDialog.PADDING + 2, WorkDialog.PADDING + 6, 0))
		oFrame.pack(side=tk.TOP, fill=tk.X)
		oFrame.columnconfigure(1, weight=1)

		oNameLabel = ttk.Label(oFrame, text=WorkDialog.LABEL_TEST_NAME, font=UiTheme.FONT_BOLD,
							   width=WorkDialog.LABEL_WIDTH)
		oNameLabel.grid(row=0, column=0, sticky=tk.W, pady=(0, 6))
		oNameValue = ttk.Label(oFrame, textvariable=self.m_oTestNameVar)
		oNameValue.grid(row=0, column=1, sticky=tk.EW, pady=(0, 6))

		oContentLabel = ttk.Label(oFrame, text=WorkDialog.LABEL_TEST_CONTENT, font=UiTheme.FONT_BOLD,
								  width=WorkDialog.LABEL_WIDTH)
		oContentLabel.grid(row=1, column=0, sticky=tk.NW)
		self.m_oContentText = tk.Text(oFrame, height=WorkDialog.CONTENT_LINES, wrap=tk.WORD, relief=tk.FLAT,
									  borderwidth=0, highlightthickness=0, font=UiTheme.FONT,
									  background=UiTheme.getColor(UiTheme.COLOR_BACKGROUND),
									  foreground=UiTheme.getColor(UiTheme.COLOR_FOREGROUND))
		self.m_oContentText.grid(row=1, column=1, sticky=tk.EW)
		self.m_oContentText.configure(state=tk.DISABLED)

	def _buildTableArea(self):
		oFrame = ttk.Frame(self, padding=(WorkDialog.PADDING + 6, WorkDialog.PADDING, WorkDialog.PADDING + 6, 0))
		oFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		arrColumns = (WorkDialog.COLUMN_NO, WorkDialog.COLUMN_NAME, WorkDialog.COLUMN_RESULT)
		self.m_oTree = tb.Treeview(oFrame, columns=arrColumns, show="headings", selectmode=tk.BROWSE,
								   bootstyle=UiTheme.TABLE_STYLE)
		for arrDef in WorkDialog.COLUMN_DEFS:
			self.m_oTree.heading(arrDef[0], text=arrDef[1])
			self.m_oTree.column(arrDef[0], width=arrDef[2], anchor=arrDef[3], stretch=(arrDef[0] == WorkDialog.COLUMN_NAME))
		UiTheme.configureColorTags(self.m_oTree)
		oScrollbar = ttk.Scrollbar(oFrame, orient=tk.VERTICAL, command=self.m_oTree.yview)
		self.m_oTree.configure(yscrollcommand=oScrollbar.set)
		self.m_oTree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		oScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

	def _buildBottomArea(self):
		oSeparator = ttk.Separator(self)
		oFrame = ttk.Frame(self, padding=(WorkDialog.PADDING + 6, 10))
		oFrame.pack(side=tk.BOTTOM, fill=tk.X)
		oSeparator.pack(side=tk.BOTTOM, fill=tk.X)
		self.m_oStatusDot = ttk.Label(oFrame, text=UiTheme.STATUS_DOT,
									  foreground=UiTheme.getColor(UiTheme.COLOR_DEFAULT))
		self.m_oStatusDot.pack(side=tk.LEFT)
		oStatusLabel = ttk.Label(oFrame, textvariable=self.m_oStatusVar)
		oStatusLabel.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))
		oErrorButton = UiTheme.createButton(oFrame, WorkDialog.BUTTON_ERROR, UiTheme.BUTTON_OUTLINE_DANGER,
											self.openErrorDialog)
		oErrorButton.pack(side=tk.RIGHT)
		oTaskButton = UiTheme.createButton(oFrame, WorkDialog.BUTTON_TASK_LIST, UiTheme.BUTTON_PRIMARY,
										   self.openTaskList)
		oTaskButton.pack(side=tk.RIGHT, padx=(0, 6))
		oReservationButton = UiTheme.createButton(oFrame, WorkDialog.BUTTON_RESERVATION_LIST,
												  UiTheme.BUTTON_OUTLINE_SECONDARY, self.openReservationList)
		oReservationButton.pack(side=tk.RIGHT, padx=(0, 6))

	def _prepareOpen(self):
		self.showWindow()
		return self.m_oActiveDialog is None

	def _showDialog(self, oDialog):
		self.m_oActiveDialog = oDialog
		oDialog.showModal()

	def _renderTask(self):
		oTask = self.m_oDisplayedTask
		strName = ""
		strContent = ""
		lstInfos = []
		if oTask is not None:
			strName = StringUtil.nvl(oTask.getStrChordNm(), "")
			strContent = StringUtil.nvl(oTask.getStrChordSbst(), "")
			lstInfos = TestInfoDAO.selectTestInfoList(oTask.getStrTaskId())
		self.m_oTestNameVar.set(strName)
		self.m_oContentText.configure(state=tk.NORMAL)
		self.m_oContentText.delete("1.0", tk.END)
		self.m_oContentText.insert("1.0", strContent)
		self.m_oContentText.configure(state=tk.DISABLED)
		for strItemId in self.m_oTree.get_children():
			self.m_oTree.delete(strItemId)
		nNo = 1
		for oInfo in lstInfos:
			strResult = oInfo.getStrActResult()
			arrValues = (nNo, StringUtil.nvl(oInfo.getStrActSbst(), ""), UiTheme.getResultText(strResult))
			strColorName = UiTheme.getResultColorName(strResult)
			if StringUtil.isEmpty(strColorName):
				self.m_oTree.insert("", tk.END, values=arrValues)
			else:
				self.m_oTree.insert("", tk.END, values=arrValues, tags=(strColorName,))
			nNo += 1
