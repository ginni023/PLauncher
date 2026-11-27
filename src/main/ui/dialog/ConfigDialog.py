import tkinter as tk
from tkinter import ttk

import ttkbootstrap as tb

from ui.dialog.ChildDialog import ChildDialog
from engine.LauncherConfig import LauncherConfig
from engine.ProtocolRegistry import ProtocolRegistry
from util.StringUtil import StringUtil
from engine.SystemApiClient import SystemApiClient
from ui.UiTheme import UiTheme


class ConfigDialog(ChildDialog):

	TITLE = "설정"
	WIDTH = 600
	HEIGHT = 470
	SECRET_MASK = "*"
	ENTRY_WIDTH = 46
	CHECK_TIME_MIN = 1
	CHECK_TIME_MAX = 1440

	BUTTON_APPLY = "적용"
	BUTTON_CLOSE = "닫기"
	BUTTON_AUTH = "인증"
	CHECK_TEXT = "사용"
	AUTH_STATE_OK = "인증됨"
	AUTH_STATE_REQUIRED = "인증 필요"
	MESSAGE_APPLIED = "설정이 적용되었습니다."
	MESSAGE_AUTH_OK = "인증되었습니다."
	MESSAGE_AUTH_FAIL = "인증에 실패했습니다."
	MESSAGE_AUTH_EMPTY = "API 토큰을 입력하세요."
	MESSAGE_AUTH_NEEDED = "API 토큰을 바꾸면 인증 후에 적용할 수 있습니다."
	MESSAGE_INVALID_CHECK_TIME = "예약 체크 타임은 1 이상의 숫자로 입력하세요."

	LABELS = (
		(LauncherConfig.RESERVATION_SYSTEM, "시스템 도메인"),
		(LauncherConfig.INSTALL_PATH, "설치 경로"),
		(LauncherConfig.LINK_REGST_IND, "웹에서 런처 실행"),
		(LauncherConfig.RESERVATION_USE, "예약 기능"),
		(LauncherConfig.API_TOKEN, "API 토큰"),
		(LauncherConfig.NODEJS_PATH, "Node.js 경로"),
		(LauncherConfig.PLAYWRIGHT_PATH, "Playwright 경로"),
		(LauncherConfig.MINIMIZE_IND, "최소화(HEADLESS)"),
		(LauncherConfig.SAVE_PATH, "캡처 저장 경로"),
		(LauncherConfig.RESERVATION_CHECK_TIME, "예약 체크 타임(분)"),
	)

	def __init__(self, oParent, oLauncher, fnOnClose):
		ChildDialog.__init__(self, oParent, ConfigDialog.TITLE, ConfigDialog.WIDTH, ConfigDialog.HEIGHT, fnOnClose)
		self.m_oLauncher = oLauncher
		self.m_oConfig = oLauncher.getConfig()
		self.m_mapOriginal = self.m_oConfig.copyValues()
		self.m_strAuthedToken = self.m_mapOriginal.get(LauncherConfig.API_TOKEN, "")
		self.m_mapVars = {}
		self.m_oAuthStateVar = tk.StringVar(self)
		self.m_oMessageVar = tk.StringVar(self)
		self.m_oApplyButton = None
		self._buildForm()
		self._buildBottomArea()
		self._updateState()

	def _buildForm(self):
		oFrame = ttk.Frame(self, padding=ChildDialog.PADDING)
		oFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		oFrame.columnconfigure(1, weight=1)
		nRow = 0
		for arrLabel in ConfigDialog.LABELS:
			strKey = arrLabel[0]
			oLabel = ttk.Label(oFrame, text=arrLabel[1])
			oLabel.grid(row=nRow, column=0, sticky=tk.W, padx=(0, 10), pady=5)
			self._buildField(oFrame, nRow, strKey)
			nRow += 1
		oMessageLabel = ttk.Label(oFrame, textvariable=self.m_oMessageVar, foreground=UiTheme.getColor(UiTheme.COLOR_INFO))
		oMessageLabel.grid(row=nRow, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))

	def _buildField(self, oFrame, nRow, strKey):
		strValue = self.m_mapOriginal.get(strKey, "")
		if strKey in LauncherConfig.FLAG_KEYS:
			oVar = tk.BooleanVar(self, StringUtil.equalsIgnoreCase(strValue, LauncherConfig.YES))
			oWidget = tb.Checkbutton(oFrame, text=ConfigDialog.CHECK_TEXT, variable=oVar,
									 bootstyle=UiTheme.CHECK_STYLE)
			oWidget.grid(row=nRow, column=1, sticky=tk.W)
		elif strKey == LauncherConfig.RESERVATION_CHECK_TIME:
			oVar = tk.StringVar(self, strValue)
			oWidget = tb.Spinbox(oFrame, from_=ConfigDialog.CHECK_TIME_MIN, to=ConfigDialog.CHECK_TIME_MAX,
								  textvariable=oVar, width=8)
			oWidget.grid(row=nRow, column=1, sticky=tk.W)
		else:
			oVar = tk.StringVar(self, strValue)
			oWidget = ttk.Entry(oFrame, textvariable=oVar, width=ConfigDialog.ENTRY_WIDTH)
			oWidget.grid(row=nRow, column=1, sticky=tk.EW)
			if strKey in LauncherConfig.AUTO_PATH_KEYS:
				oWidget.configure(state="readonly")
			if strKey in LauncherConfig.SECRET_KEYS:
				oWidget.configure(show=ConfigDialog.SECRET_MASK)
		if strKey == LauncherConfig.API_TOKEN:
			oAuthFrame = ttk.Frame(oFrame)
			oAuthFrame.grid(row=nRow, column=2, sticky=tk.W, padx=(6, 0))
			oAuthButton = UiTheme.createButton(oAuthFrame, ConfigDialog.BUTTON_AUTH, UiTheme.BUTTON_OUTLINE_PRIMARY,
											   self._onAuthenticate)
			oAuthButton.pack(side=tk.LEFT)
			oAuthState = ttk.Label(oAuthFrame, textvariable=self.m_oAuthStateVar, width=9)
			oAuthState.pack(side=tk.LEFT, padx=(6, 0))
		oVar.trace_add("write", self._onValueChanged)
		self.m_mapVars[strKey] = oVar

	def _buildBottomArea(self):
		oSeparator = ttk.Separator(self)
		oSeparator.pack(side=tk.TOP, fill=tk.X)
		oFrame = ttk.Frame(self, padding=ChildDialog.PADDING)
		oFrame.pack(side=tk.BOTTOM, fill=tk.X)
		oCloseButton = UiTheme.createButton(oFrame, ConfigDialog.BUTTON_CLOSE, UiTheme.BUTTON_SECONDARY,
											self.closeDialog)
		oCloseButton.pack(side=tk.RIGHT)
		self.m_oApplyButton = UiTheme.createButton(oFrame, ConfigDialog.BUTTON_APPLY, UiTheme.BUTTON_PRIMARY,
												   self._onApply)
		self.m_oApplyButton.pack(side=tk.RIGHT, padx=(0, 6))

	def _collectValues(self):
		mapValues = dict(self.m_mapOriginal)
		for strKey in LauncherConfig.KEY_ORDER:
			oVar = self.m_mapVars[strKey]
			if strKey in LauncherConfig.FLAG_KEYS:
				if oVar.get():
					mapValues[strKey] = LauncherConfig.YES
				else:
					mapValues[strKey] = LauncherConfig.NO
			else:
				strValue = oVar.get()
				mapValues[strKey] = strValue.strip()
		return mapValues

	def _onValueChanged(self, *arrArgs):
		self.m_oMessageVar.set("")
		self._updateState()

	def _updateState(self):
		mapCurrent = self._collectValues()
		bChanged = mapCurrent != self.m_mapOriginal
		strToken = mapCurrent[LauncherConfig.API_TOKEN]
		bAuthOk = StringUtil.isEmpty(strToken) or strToken == self.m_strAuthedToken
		bCheckTimeOk = StringUtil.isPositiveInteger(mapCurrent[LauncherConfig.RESERVATION_CHECK_TIME])
		if StringUtil.isEmpty(strToken):
			self.m_oAuthStateVar.set("")
		elif bAuthOk:
			self.m_oAuthStateVar.set(ConfigDialog.AUTH_STATE_OK)
		else:
			self.m_oAuthStateVar.set(ConfigDialog.AUTH_STATE_REQUIRED)
		if not bCheckTimeOk:
			self.m_oMessageVar.set(ConfigDialog.MESSAGE_INVALID_CHECK_TIME)
		elif bChanged and not bAuthOk:
			self.m_oMessageVar.set(ConfigDialog.MESSAGE_AUTH_NEEDED)
		if bChanged and bAuthOk and bCheckTimeOk:
			self.m_oApplyButton.configure(state=tk.NORMAL)
		else:
			self.m_oApplyButton.configure(state=tk.DISABLED)

	def _onAuthenticate(self):
		mapCurrent = self._collectValues()
		strToken = mapCurrent[LauncherConfig.API_TOKEN]
		if StringUtil.isEmpty(strToken):
			self.m_oMessageVar.set(ConfigDialog.MESSAGE_AUTH_EMPTY)
			return
		bAuthenticated = SystemApiClient.authenticate(mapCurrent[LauncherConfig.RESERVATION_SYSTEM], strToken)
		if bAuthenticated:
			self.m_strAuthedToken = strToken
		self._updateState()
		if bAuthenticated:
			self.m_oMessageVar.set(ConfigDialog.MESSAGE_AUTH_OK)
		else:
			self.m_oMessageVar.set(ConfigDialog.MESSAGE_AUTH_FAIL)

	def _onApply(self):
		mapCurrent = self._collectValues()
		for strKey in LauncherConfig.KEY_ORDER:
			if strKey not in LauncherConfig.AUTO_PATH_KEYS:
				self.m_oConfig.setValue(strKey, mapCurrent[strKey])
		self.m_oConfig.save()
		ProtocolRegistry.applyConfig(self.m_oConfig)
		self.m_mapOriginal = self.m_oConfig.copyValues()
		self._updateState()
		self.m_oMessageVar.set(ConfigDialog.MESSAGE_APPLIED)
		self.m_oLauncher.onConfigApplied()
