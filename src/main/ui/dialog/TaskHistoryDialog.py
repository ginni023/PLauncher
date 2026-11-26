import tkinter as tk
from tkinter import ttk

import ttkbootstrap as tb

from ui.dialog.ChildDialog import ChildDialog
from ui.UiTheme import UiTheme
from util.StringUtil import StringUtil
from task.code.TaskStatus import TaskStatus
from task.code.TaskType import TaskType


class TaskHistoryDialog(ChildDialog):

	WIDTH = 820
	HEIGHT = 440
	LABEL_COUNT = "전체 "
	LABEL_COUNT_SUFFIX = "건"
	BUTTON_CLOSE = "닫기"

	COLUMN_NO = "no"
	COLUMN_CRET_DT = "cretDt"
	COLUMN_RESERVE_DATE = "reserveDate"
	COLUMN_RUN_DATE = "runDate"
	COLUMN_TASK_ID = "taskId"
	COLUMN_TASK_TYPE = "taskType"
	COLUMN_NAME = "name"
	COLUMN_STATUS = "status"
	COLUMN_RESULT = "result"
	CENTER_COLUMNS = (COLUMN_NO, COLUMN_TASK_TYPE, COLUMN_STATUS, COLUMN_RESERVE_DATE, COLUMN_RUN_DATE)

	def __init__(self, oParent, strTitle, fnOnClose):
		ChildDialog.__init__(self, oParent, strTitle, TaskHistoryDialog.WIDTH, TaskHistoryDialog.HEIGHT, fnOnClose)
		self.m_oCountVar = tk.StringVar(self)
		self.m_oTree = None
		self._buildBottomArea()
		self._buildTable()
		self.refresh()

	def refresh(self):
		lstTasks = self._loadTasks()
		arrSelection = self.m_oTree.selection()
		for strItemId in self.m_oTree.get_children():
			self.m_oTree.delete(strItemId)
		arrColumnDefs = self._getColumnDefs()
		nNo = 1
		for oTask in lstTasks:
			mapValues = self._getRowValueMap(oTask)
			mapValues[TaskHistoryDialog.COLUMN_NO] = nNo
			nNo += 1
			lstValues = []
			for arrDef in arrColumnDefs:
				lstValues.append(mapValues[arrDef[0]])
			strColorName = UiTheme.getStatusColorName(oTask.getStrTestStatus())
			self.m_oTree.insert("", tk.END, iid=oTask.getStrTaskId(), values=lstValues, tags=(strColorName,))
		for strItemId in arrSelection:
			if self.m_oTree.exists(strItemId):
				self.m_oTree.selection_add(strItemId)
		self.m_oCountVar.set(TaskHistoryDialog.LABEL_COUNT + str(len(lstTasks)) + TaskHistoryDialog.LABEL_COUNT_SUFFIX)

	def _loadTasks(self):
		raise NotImplementedError("_loadTasks must be implemented")

	def _getColumnDefs(self):
		return (
			(TaskHistoryDialog.COLUMN_CRET_DT, "등록일시", 140),
			(TaskHistoryDialog.COLUMN_TASK_TYPE, "작업타입", 80),
			(TaskHistoryDialog.COLUMN_NAME, "테스트명", 220),
			(TaskHistoryDialog.COLUMN_STATUS, "상태", 100),
			(TaskHistoryDialog.COLUMN_RESULT, "결과", 230),
		)

	def _getRowValueMap(self, oTask):
		mapValues = {}
		mapValues[TaskHistoryDialog.COLUMN_CRET_DT] = StringUtil.nvl(oTask.getStrSysRecdCretDt(), "")
		mapValues[TaskHistoryDialog.COLUMN_RESERVE_DATE] = StringUtil.nvl(oTask.getStrReserveDate(), "")
		mapValues[TaskHistoryDialog.COLUMN_RUN_DATE] = StringUtil.nvl(oTask.getStrRunDate(), "")
		mapValues[TaskHistoryDialog.COLUMN_TASK_ID] = oTask.getStrTaskId()
		mapValues[TaskHistoryDialog.COLUMN_TASK_TYPE] = TaskType.getLabel(oTask.getStrTaskType())
		mapValues[TaskHistoryDialog.COLUMN_NAME] = self._getTaskName(oTask)
		mapValues[TaskHistoryDialog.COLUMN_STATUS] = UiTheme.STATUS_DOT + " " + TaskStatus.getName(oTask.getStrTestStatus())
		mapValues[TaskHistoryDialog.COLUMN_RESULT] = StringUtil.nvl(oTask.getStrTestResult(), "")
		return mapValues

	def _getTaskName(self, oTask):
		strName = oTask.getStrChordNm()
		if StringUtil.isEmpty(strName):
			strName = oTask.getStrChordId()
		return StringUtil.nvl(strName, "")

	def _buildTable(self):
		oFrame = ttk.Frame(self, padding=(ChildDialog.PADDING, ChildDialog.PADDING, ChildDialog.PADDING, 0))
		oFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		arrColumnDefs = self._getColumnDefs()
		lstColumnIds = []
		for arrDef in arrColumnDefs:
			lstColumnIds.append(arrDef[0])
		self.m_oTree = tb.Treeview(oFrame, columns=lstColumnIds, show="headings", selectmode=tk.BROWSE,
								   bootstyle=UiTheme.TABLE_STYLE)
		for arrDef in arrColumnDefs:
			self.m_oTree.heading(arrDef[0], text=arrDef[1])
			if arrDef[0] in TaskHistoryDialog.CENTER_COLUMNS:
				self.m_oTree.column(arrDef[0], width=arrDef[2], anchor=tk.CENTER)
			else:
				self.m_oTree.column(arrDef[0], width=arrDef[2], anchor=tk.W)
		UiTheme.configureColorTags(self.m_oTree)
		oScrollbar = ttk.Scrollbar(oFrame, orient=tk.VERTICAL, command=self.m_oTree.yview)
		self.m_oTree.configure(yscrollcommand=oScrollbar.set)
		self.m_oTree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		oScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

	def _buildBottomArea(self):
		oFrame = ttk.Frame(self, padding=ChildDialog.PADDING)
		oFrame.pack(side=tk.BOTTOM, fill=tk.X)
		oCountLabel = tb.Label(oFrame, textvariable=self.m_oCountVar, bootstyle=UiTheme.COLOR_DEFAULT)
		oCountLabel.pack(side=tk.LEFT)
		oCloseButton = UiTheme.createButton(oFrame, TaskHistoryDialog.BUTTON_CLOSE, UiTheme.BUTTON_SECONDARY,
											self.closeDialog)
		oCloseButton.pack(side=tk.RIGHT)
