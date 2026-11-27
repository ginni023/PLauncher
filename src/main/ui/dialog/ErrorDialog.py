import tkinter as tk
from tkinter import ttk

from ui.dialog.ChildDialog import ChildDialog
from ui.UiTheme import UiTheme
from util.StringUtil import StringUtil
from database.TestTaskDtlDAO import TestTaskDtlDAO


class ErrorDialog(ChildDialog):

	TITLE = "오류"
	WIDTH = 560
	HEIGHT = 360
	BUTTON_CLOSE = "닫기"
	MESSAGE_NO_TASK = "표시 중인 작업이 없습니다."
	MESSAGE_NO_ERROR = "발생한 오류가 없습니다."
	LABEL_TASK = "작업 : "
	LABEL_TASK_ERROR = "[작업 오류] "
	LABEL_ACT_PREFIX = "[동작 "
	LABEL_ACT_SUFFIX = "] "
	TEXT_PADDING = 8

	def __init__(self, oParent, oTask, fnOnClose):
		ChildDialog.__init__(self, oParent, ErrorDialog.TITLE, ErrorDialog.WIDTH, ErrorDialog.HEIGHT, fnOnClose)
		self.m_oTask = oTask
		self.m_oText = None
		self._buildBottomArea()
		self._buildTextArea()
		self.refresh()

	def refresh(self):
		strContent = self._buildContent()
		self.m_oText.configure(state=tk.NORMAL)
		self.m_oText.delete("1.0", tk.END)
		self.m_oText.insert("1.0", strContent)
		self.m_oText.configure(state=tk.DISABLED)

	def _buildContent(self):
		if self.m_oTask is None:
			return ErrorDialog.MESSAGE_NO_TASK
		lstLines = []
		lstLines.append(ErrorDialog.LABEL_TASK + self.m_oTask.getStrTaskId())
		lstLines.append("")
		bHasError = False
		strTaskError = self.m_oTask.getStrErrMsg()
		if not StringUtil.isEmpty(strTaskError):
			lstLines.append(ErrorDialog.LABEL_TASK_ERROR + strTaskError)
			bHasError = True
		lstDtls = TestTaskDtlDAO.selectTestTaskDtlList(self.m_oTask.getStrTaskId())
		for oDtl in lstDtls:
			strErrorMsg = oDtl.getStrErrorMsg()
			if StringUtil.isEmpty(strErrorMsg):
				continue
			strErrorClass = StringUtil.nvl(oDtl.getStrErrorClass(), "")
			strLine = ErrorDialog.LABEL_ACT_PREFIX + str(oDtl.getNActNo()) + ErrorDialog.LABEL_ACT_SUFFIX
			if not StringUtil.isEmpty(strErrorClass):
				strLine = strLine + strErrorClass + " : "
			lstLines.append(strLine + strErrorMsg)
			bHasError = True
		if not bHasError:
			lstLines.append(ErrorDialog.MESSAGE_NO_ERROR)
		return "\n".join(lstLines)

	def _buildTextArea(self):
		oFrame = ttk.Frame(self, padding=(ChildDialog.PADDING, ChildDialog.PADDING, ChildDialog.PADDING, 0))
		oFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.m_oText = tk.Text(oFrame, wrap=tk.WORD, font=UiTheme.FONT, relief=tk.FLAT,
							   padx=ErrorDialog.TEXT_PADDING, pady=ErrorDialog.TEXT_PADDING,
							   highlightthickness=1, highlightcolor=UiTheme.getColor("border"),
							   highlightbackground=UiTheme.getColor("border"),
							   background=UiTheme.getColor("inputbg"), foreground=UiTheme.getColor("inputfg"))
		oScrollbar = ttk.Scrollbar(oFrame, orient=tk.VERTICAL, command=self.m_oText.yview)
		self.m_oText.configure(yscrollcommand=oScrollbar.set)
		self.m_oText.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		oScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

	def _buildBottomArea(self):
		oFrame = ttk.Frame(self, padding=ChildDialog.PADDING)
		oFrame.pack(side=tk.BOTTOM, fill=tk.X)
		oCloseButton = UiTheme.createButton(oFrame, ErrorDialog.BUTTON_CLOSE, UiTheme.BUTTON_SECONDARY,
											self.closeDialog)
		oCloseButton.pack(side=tk.RIGHT)
