from database.DatabaseUtil import DatabaseUtil
from dto.TestCommDTO import TestCommDTO


class TestCommDAO:

	SQL_SELECT_TEST_COMM_LIST = "selectTestCommList"
	SQL_SELECT_TEST_COMM = "selectTestComm"
	SQL_INSERT_TEST_COMM = "insertTestComm"
	SQL_UPDATE_TEST_COMM = "updateTestComm"
	BIND_UPR_DIV_KEY = "upr_Div_Key"

	def __init__(self):
		raise TypeError("TestCommDAO cannot be instantiated")

	@staticmethod
	def selectTestCommList(strUprDivKey):
		mapParams = {TestCommDAO.BIND_UPR_DIV_KEY: strUprDivKey}
		lstRows = DatabaseUtil.selectRows(TestCommDAO.SQL_SELECT_TEST_COMM_LIST, mapParams)
		lstComms = []
		for oRow in lstRows:
			lstComms.append(TestCommDTO.fromRow(oRow))
		return lstComms

	@staticmethod
	def selectTestComm(oComm):
		lstRows = DatabaseUtil.selectRows(TestCommDAO.SQL_SELECT_TEST_COMM, oComm.toParams())
		if len(lstRows) == 0:
			return None
		return TestCommDTO.fromRow(lstRows[0])

	@staticmethod
	def insertTestComm(oComm):
		DatabaseUtil.executeUpdate(TestCommDAO.SQL_INSERT_TEST_COMM, oComm.toParams())

	@staticmethod
	def updateTestComm(oComm):
		DatabaseUtil.executeUpdate(TestCommDAO.SQL_UPDATE_TEST_COMM, oComm.toParams())
