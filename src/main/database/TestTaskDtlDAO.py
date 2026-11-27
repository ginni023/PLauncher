from database.DatabaseUtil import DatabaseUtil
from dto.TestTaskDtlDTO import TestTaskDtlDTO


class TestTaskDtlDAO:

	SQL_SELECT_TEST_TASK_DTL_LIST = "selectTestTaskDtlList"
	SQL_SELECT_TEST_TASK_DTL = "selectTestTaskDtl"
	SQL_INSERT_TEST_TASK_DTL = "insertTestTaskDtl"
	SQL_UPDATE_TEST_TASK_DTL_RESULT = "updateTestTaskDtlResult"
	BIND_TASK_ID = "task_Id"

	def __init__(self):
		raise TypeError("TestTaskDtlDAO cannot be instantiated")

	@staticmethod
	def selectTestTaskDtlList(strTaskId):
		mapParams = {TestTaskDtlDAO.BIND_TASK_ID: strTaskId}
		lstRows = DatabaseUtil.selectRows(TestTaskDtlDAO.SQL_SELECT_TEST_TASK_DTL_LIST, mapParams)
		lstDtls = []
		for oRow in lstRows:
			lstDtls.append(TestTaskDtlDTO.fromRow(oRow))
		return lstDtls

	@staticmethod
	def selectTestTaskDtl(oDtl):
		lstRows = DatabaseUtil.selectRows(TestTaskDtlDAO.SQL_SELECT_TEST_TASK_DTL, oDtl.toParams())
		if len(lstRows) == 0:
			return None
		return TestTaskDtlDTO.fromRow(lstRows[0])

	@staticmethod
	def insertTestTaskDtl(oDtl):
		DatabaseUtil.executeUpdate(TestTaskDtlDAO.SQL_INSERT_TEST_TASK_DTL, oDtl.toParams())

	@staticmethod
	def updateTestTaskDtlResult(oDtl):
		DatabaseUtil.executeUpdate(TestTaskDtlDAO.SQL_UPDATE_TEST_TASK_DTL_RESULT, oDtl.toParams())
