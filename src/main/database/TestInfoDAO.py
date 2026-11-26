from database.DatabaseUtil import DatabaseUtil
from dto.TestInfoDTO import TestInfoDTO


class TestInfoDAO:

	SQL_SELECT_TEST_INFO_LIST = "selectTestInfoList"
	BIND_TASK_ID = "task_Id"

	def __init__(self):
		raise TypeError("TestInfoDAO cannot be instantiated")

	@staticmethod
	def selectTestInfoList(strTaskId):
		mapParams = {TestInfoDAO.BIND_TASK_ID: strTaskId}
		lstRows = DatabaseUtil.selectRows(TestInfoDAO.SQL_SELECT_TEST_INFO_LIST, mapParams)
		lstInfos = []
		for oRow in lstRows:
			lstInfos.append(TestInfoDTO.fromRow(oRow))
		return lstInfos
