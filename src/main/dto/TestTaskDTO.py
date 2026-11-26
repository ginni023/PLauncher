class TestTaskDTO:

	TABLE_NAME = "TEST_TASK_LIST"
	COLUMNS = (
		("TASK_ID", "task_Id", "getStrTaskId", "setStrTaskId"),
		("TASK_TYPE", "task_Type", "getStrTaskType", "setStrTaskType"),
		("DTL_TYPE", "dtl_Type", "getStrDtlType", "setStrDtlType"),
		("DEVICE", "device", "getStrDevice", "setStrDevice"),
		("SYS_RECD_CRET_DT", "sys_Recd_Cret_Dt", "getStrSysRecdCretDt", "setStrSysRecdCretDt"),
		("TASK_ADR", "task_Adr", "getStrTaskAdr", "setStrTaskAdr"),
		("TEST_STATUS", "test_Status", "getStrTestStatus", "setStrTestStatus"),
		("TEST_RESULT", "test_Result", "getStrTestResult", "setStrTestResult"),
		("ERR_MSG", "err_Msg", "getStrErrMsg", "setStrErrMsg"),
		("RUN_DATE", "run_Date", "getStrRunDate", "setStrRunDate"),
		("REQ_PROD_SEQ", "req_Prod_Seq", "getStrReqProdSeq", "setStrReqProdSeq"),
		("EXE_CD", "exe_Cd", "getStrExeCd", "setStrExeCd"),
		("PREF_RANK", "pref_Rank", "getStrPrefRank", "setStrPrefRank"),
		("CHORD_ID", "chord_Id", "getStrChordId", "setStrChordId"),
		("CHORD_NM", "chord_Nm", "getStrChordNm", "setStrChordNm"),
		("CHORD_TYPE", "chord_Type", "getStrChordType", "setStrChordType"),
		("CHORD_SBST", "chord_Sbst", "getStrChordSbst", "setStrChordSbst"),
		("RESERVE_DATE", "reserve_Date", "getStrReserveDate", "setStrReserveDate"),
		("RESOURCE", "resource", "getStrResource", "setStrResource"),
		("SYS_TRTR_ID", "sys_Trtr_Id", "getStrSysTrtrId", "setStrSysTrtrId"),
	)

	def __init__(self):
		self.m_strTaskId = None
		self.m_strTaskType = None
		self.m_strDtlType = None
		self.m_strDevice = "PC"
		self.m_strSysRecdCretDt = None
		self.m_strTaskAdr = None
		self.m_strTestStatus = None
		self.m_strTestResult = None
		self.m_strErrMsg = None
		self.m_strRunDate = None
		self.m_strReqProdSeq = None
		self.m_strExeCd = None
		self.m_strPrefRank = None
		self.m_strChordId = None
		self.m_strChordNm = None
		self.m_strChordType = None
		self.m_strChordSbst = None
		self.m_strReserveDate = None
		self.m_strResource = None
		self.m_strSysTrtrId = None

	@staticmethod
	def fromRow(oRow):
		oDto = TestTaskDTO()
		lstKeys = oRow.keys()
		for arrColumn in TestTaskDTO.COLUMNS:
			if arrColumn[0] in lstKeys:
				fnSetter = getattr(oDto, arrColumn[3])
				fnSetter(oRow[arrColumn[0]])
		return oDto

	def getStrTaskId(self):
		return self.m_strTaskId

	def setStrTaskId(self, strValue):
		if strValue is None:
			self.m_strTaskId = None
		else:
			self.m_strTaskId = str(strValue)

	def getStrTaskType(self):
		return self.m_strTaskType

	def setStrTaskType(self, strValue):
		if strValue is None:
			self.m_strTaskType = None
		else:
			self.m_strTaskType = str(strValue)

	def getStrDtlType(self):
		return self.m_strDtlType

	def setStrDtlType(self, strValue):
		if strValue is None:
			self.m_strDtlType = None
		else:
			self.m_strDtlType = str(strValue)

	def getStrDevice(self):
		return self.m_strDevice

	def setStrDevice(self, strValue):
		if strValue is None:
			self.m_strDevice = None
		else:
			self.m_strDevice = str(strValue)

	def getStrSysRecdCretDt(self):
		return self.m_strSysRecdCretDt

	def setStrSysRecdCretDt(self, strValue):
		if strValue is None:
			self.m_strSysRecdCretDt = None
		else:
			self.m_strSysRecdCretDt = str(strValue)

	def getStrTaskAdr(self):
		return self.m_strTaskAdr

	def setStrTaskAdr(self, strValue):
		if strValue is None:
			self.m_strTaskAdr = None
		else:
			self.m_strTaskAdr = str(strValue)

	def getStrTestStatus(self):
		return self.m_strTestStatus

	def setStrTestStatus(self, strValue):
		if strValue is None:
			self.m_strTestStatus = None
		else:
			self.m_strTestStatus = str(strValue)

	def getStrTestResult(self):
		return self.m_strTestResult

	def setStrTestResult(self, strValue):
		if strValue is None:
			self.m_strTestResult = None
		else:
			self.m_strTestResult = str(strValue)

	def getStrErrMsg(self):
		return self.m_strErrMsg

	def setStrErrMsg(self, strValue):
		if strValue is None:
			self.m_strErrMsg = None
		else:
			self.m_strErrMsg = str(strValue)

	def getStrRunDate(self):
		return self.m_strRunDate

	def setStrRunDate(self, strValue):
		if strValue is None:
			self.m_strRunDate = None
		else:
			self.m_strRunDate = str(strValue)

	def getStrReqProdSeq(self):
		return self.m_strReqProdSeq

	def setStrReqProdSeq(self, strValue):
		if strValue is None:
			self.m_strReqProdSeq = None
		else:
			self.m_strReqProdSeq = str(strValue)

	def getStrExeCd(self):
		return self.m_strExeCd

	def setStrExeCd(self, strValue):
		if strValue is None:
			self.m_strExeCd = None
		else:
			self.m_strExeCd = str(strValue)

	def getStrPrefRank(self):
		return self.m_strPrefRank

	def setStrPrefRank(self, strValue):
		if strValue is None:
			self.m_strPrefRank = None
		else:
			self.m_strPrefRank = str(strValue)

	def getStrChordId(self):
		return self.m_strChordId

	def setStrChordId(self, strValue):
		if strValue is None:
			self.m_strChordId = None
		else:
			self.m_strChordId = str(strValue)

	def getStrChordNm(self):
		return self.m_strChordNm

	def setStrChordNm(self, strValue):
		if strValue is None:
			self.m_strChordNm = None
		else:
			self.m_strChordNm = str(strValue)

	def getStrChordType(self):
		return self.m_strChordType

	def setStrChordType(self, strValue):
		if strValue is None:
			self.m_strChordType = None
		else:
			self.m_strChordType = str(strValue)

	def getStrChordSbst(self):
		return self.m_strChordSbst

	def setStrChordSbst(self, strValue):
		if strValue is None:
			self.m_strChordSbst = None
		else:
			self.m_strChordSbst = str(strValue)

	def getStrReserveDate(self):
		return self.m_strReserveDate

	def setStrReserveDate(self, strValue):
		if strValue is None:
			self.m_strReserveDate = None
		else:
			self.m_strReserveDate = str(strValue)

	def getStrResource(self):
		return self.m_strResource

	def setStrResource(self, strValue):
		if strValue is None:
			self.m_strResource = None
		else:
			self.m_strResource = str(strValue)

	def getStrSysTrtrId(self):
		return self.m_strSysTrtrId

	def setStrSysTrtrId(self, strValue):
		if strValue is None:
			self.m_strSysTrtrId = None
		else:
			self.m_strSysTrtrId = str(strValue)

	def toParams(self):
		mapParams = {}
		for arrColumn in TestTaskDTO.COLUMNS:
			fnGetter = getattr(self, arrColumn[2])
			mapParams[arrColumn[1]] = fnGetter()
		return mapParams
