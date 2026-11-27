import tkinter as tk
from tkinter import ttk

from ui.dialog.ChildDialog import ChildDialog
from ui.UiTheme import UiTheme


class LoginGuideDialog(ChildDialog):

	TITLE = "로그인 안내"
	WIDTH = 420
	HEIGHT = 150
	MESSAGE = "브라우저에서 로그인을 마친 뒤 이 창의 [확인] 버튼을 눌러주세요.\n(브라우저는 닫지 마세요)"
	BUTTON_CONFIRM = "확인"
	WRAP_LENGTH = 380

	def __init__(self, oParent, fnOnConfirm, fnOnClose):
		ChildDialog.__init__(self, oParent, LoginGuideDialog.TITLE, LoginGuideDialog.WIDTH, LoginGuideDialog.HEIGHT,
							 fnOnClose)
		self.m_fnOnConfirm = fnOnConfirm
		self.protocol("WM_DELETE_WINDOW", self.confirmLogin)
		self.attributes("-topmost", True)
		self._buildBottomArea()
		self._buildMessageArea()

	def confirmLogin(self):
		self.m_fnOnConfirm()
		self.closeDialog()

	def _buildMessageArea(self):
		oFrame = ttk.Frame(self, padding=(ChildDialog.PADDING, ChildDialog.PADDING, ChildDialog.PADDING, 0))
		oFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		oLabel = ttk.Label(oFrame, text=LoginGuideDialog.MESSAGE, font=UiTheme.FONT,
						   wraplength=LoginGuideDialog.WRAP_LENGTH, justify=tk.LEFT)
		oLabel.pack(side=tk.TOP, anchor=tk.W)

	def _buildBottomArea(self):
		oFrame = ttk.Frame(self, padding=ChildDialog.PADDING)
		oFrame.pack(side=tk.BOTTOM, fill=tk.X)
		oConfirmButton = UiTheme.createButton(oFrame, LoginGuideDialog.BUTTON_CONFIRM, UiTheme.BUTTON_PRIMARY,
											  self.confirmLogin)
		oConfirmButton.pack(side=tk.RIGHT)
