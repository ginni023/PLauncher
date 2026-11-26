from ui.dialog.TaskHistoryDialog import TaskHistoryDialog
from database.TestTaskDAO import TestTaskDAO


class ReservationListDialog(TaskHistoryDialog):

	TITLE = "예약목록"

	def __init__(self, oParent, fnOnClose):
		TaskHistoryDialog.__init__(self, oParent, ReservationListDialog.TITLE, fnOnClose)

	def _loadTasks(self):
		return TestTaskDAO.selectReservationList()

	def _getColumnDefs(self):
		return (
			(TaskHistoryDialog.COLUMN_NO, "No", 50),
			(TaskHistoryDialog.COLUMN_NAME, "테스트명", 200),
			(TaskHistoryDialog.COLUMN_STATUS, "상태", 100),
			(TaskHistoryDialog.COLUMN_RESULT, "결과", 150),
			(TaskHistoryDialog.COLUMN_RESERVE_DATE, "예약일시", 140),
			(TaskHistoryDialog.COLUMN_RUN_DATE, "수행시간", 140),
		)
