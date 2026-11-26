from ui.dialog.TaskHistoryDialog import TaskHistoryDialog
from database.TestTaskDAO import TestTaskDAO


class TaskListDialog(TaskHistoryDialog):

	TITLE = "작업목록"

	def __init__(self, oParent, fnOnClose):
		TaskHistoryDialog.__init__(self, oParent, TaskListDialog.TITLE, fnOnClose)

	def _loadTasks(self):
		return TestTaskDAO.selectTaskList()

	def _getColumnDefs(self):
		return (
			(TaskHistoryDialog.COLUMN_NO, "No", 50),
			(TaskHistoryDialog.COLUMN_NAME, "테스트명", 200),
			(TaskHistoryDialog.COLUMN_TASK_TYPE, "작업타입", 80),
			(TaskHistoryDialog.COLUMN_STATUS, "상태", 100),
			(TaskHistoryDialog.COLUMN_RESULT, "결과", 210),
			(TaskHistoryDialog.COLUMN_RUN_DATE, "수행시간", 140),
		)
