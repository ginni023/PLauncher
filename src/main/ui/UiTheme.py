import ttkbootstrap as tb

from task.code.TaskStatus import TaskStatus
from util.StringUtil import StringUtil


class UiTheme:

	THEME_NAME = "flatly"
	FONT_NAME = "맑은 고딕"
	FONT_SIZE = 9
	FONT = (FONT_NAME, FONT_SIZE)
	FONT_BOLD = (FONT_NAME, FONT_SIZE, "bold")
	ROW_HEIGHT = 26
	BUTTON_PADDING = (10, 2)
	STATUS_DOT = "●"
	MARK_SUCCESS = "✔ "
	MARK_FAIL = "✖ "

	COLOR_BACKGROUND = "bg"
	COLOR_FOREGROUND = "fg"
	COLOR_DEFAULT = "secondary"
	COLOR_SUCCESS = "success"
	COLOR_DANGER = "danger"
	COLOR_WARNING = "warning"
	COLOR_INFO = "info"
	TAG_COLORS = (COLOR_DEFAULT, COLOR_SUCCESS, COLOR_DANGER, COLOR_WARNING, COLOR_INFO)

	BUTTON_PRIMARY = "primary"
	BUTTON_SECONDARY = "secondary"
	BUTTON_OUTLINE_PRIMARY = "outline-primary"
	BUTTON_OUTLINE_SECONDARY = "outline-secondary"
	BUTTON_OUTLINE_DANGER = "outline-danger"
	TABLE_STYLE = "primary"
	CHECK_STYLE = "primary-round-toggle"

	STATUS_COLORS = (
		(TaskStatus.RDY, COLOR_DEFAULT),
		(TaskStatus.WAIT, COLOR_DEFAULT),
		(TaskStatus.WRK, COLOR_INFO),
		(TaskStatus.CMP, COLOR_SUCCESS),
		(TaskStatus.FAIL, COLOR_DANGER),
		(TaskStatus.ERR, COLOR_DANGER),
		(TaskStatus.STOP, COLOR_WARNING),
	)
	SUCCESS_RESULTS = ("성공", "SUCCESS", "PASS", "OK", "Y", "CMP")
	FAIL_RESULTS = ("실패", "FAIL", "ERROR", "ERR", "N")

	def __init__(self):
		raise TypeError("UiTheme cannot be instantiated")

	@staticmethod
	def apply(oRoot):
		oStyle = tb.Style()
		oStyle.configure(".", font=UiTheme.FONT)
		oStyle.configure("Treeview", rowheight=UiTheme.ROW_HEIGHT, font=UiTheme.FONT)
		oStyle.configure("Treeview.Heading", font=UiTheme.FONT_BOLD)
		oRoot.option_add("*Font", UiTheme.FONT)

	@staticmethod
	def getColor(strColorName):
		oStyle = tb.Style()
		oColors = oStyle.colors
		return oColors.get(strColorName)

	@staticmethod
	def getStatusColorName(strStatus):
		for arrStatusColor in UiTheme.STATUS_COLORS:
			if StringUtil.equalsIgnoreCase(strStatus, arrStatusColor[0]):
				return arrStatusColor[1]
		return UiTheme.COLOR_DEFAULT

	@staticmethod
	def getResultColorName(strResult):
		if StringUtil.isEmpty(strResult):
			return ""
		strTrimmed = strResult.strip()
		for strSuccess in UiTheme.SUCCESS_RESULTS:
			if StringUtil.equalsIgnoreCase(strTrimmed, strSuccess):
				return UiTheme.COLOR_SUCCESS
		for strFail in UiTheme.FAIL_RESULTS:
			if StringUtil.equalsIgnoreCase(strTrimmed, strFail):
				return UiTheme.COLOR_DANGER
		return ""

	@staticmethod
	def getResultText(strResult):
		strText = StringUtil.nvl(strResult, "")
		strColorName = UiTheme.getResultColorName(strText)
		if strColorName == UiTheme.COLOR_SUCCESS:
			return UiTheme.MARK_SUCCESS + strText
		if strColorName == UiTheme.COLOR_DANGER:
			return UiTheme.MARK_FAIL + strText
		return strText

	@staticmethod
	def configureColorTags(oTree):
		for strColorName in UiTheme.TAG_COLORS:
			oTree.tag_configure(strColorName, foreground=UiTheme.getColor(strColorName))

	@staticmethod
	def createButton(oParent, strText, strBootstyle, fnCommand):
		return tb.Button(oParent, text=strText, bootstyle=strBootstyle, padding=UiTheme.BUTTON_PADDING,
						 command=fnCommand)
