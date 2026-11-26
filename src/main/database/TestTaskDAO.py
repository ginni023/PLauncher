from database.DatabaseUtil import DatabaseUtil
from dto.TestTaskDTO import TestTaskDTO


class TestTaskDAO:

	SQL_INSERT_TEST_TASK = "insertTestTask"
	SQL_UPDATE_TEST_TASK_STATUS = "updateTestTaskStatus"
	SQL_SELECT_TASK_LIST = "selectTaskList"
	SQL_SELECT_RESERVATION_LIST = "selectReservationList"
	SQL_SELECT_READY_TASK_LIST = "selectReadyTaskList"
	SQL_SELECT_PENDING_RESERVATION_LIST = "selectPendingReservationList"

	def __init__(self):
		raise TypeError("TestTaskDAO cannot be instantiated")

	@staticmethod
	def insertTestTask(oTask):
		DatabaseUtil.executeUpdate(TestTaskDAO.SQL_INSERT_TEST_TASK, oTask.toParams())

	@staticmethod
	def updateTestTaskStatus(oTask):
		DatabaseUtil.executeUpdate(TestTaskDAO.SQL_UPDATE_TEST_TASK_STATUS, oTask.toParams())

	@staticmethod
	def selectTaskList():
		return TestTaskDAO._selectTasks(TestTaskDAO.SQL_SELECT_TASK_LIST)

	@staticmethod
	def selectReservationList():
		return TestTaskDAO._selectTasks(TestTaskDAO.SQL_SELECT_RESERVATION_LIST)

	@staticmethod
	def selectReadyTaskList():
		return TestTaskDAO._selectTasks(TestTaskDAO.SQL_SELECT_READY_TASK_LIST)

	@staticmethod
	def selectPendingReservationList():
		return TestTaskDAO._selectTasks(TestTaskDAO.SQL_SELECT_PENDING_RESERVATION_LIST)

	@staticmethod
	def _selectTasks(strSqlId):
		lstRows = DatabaseUtil.selectRows(strSqlId, {})
		lstTasks = []
		for oRow in lstRows:
			lstTasks.append(TestTaskDTO.fromRow(oRow))
		return lstTasks
