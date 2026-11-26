class TestInfoDTO:

	TABLE_NAME = "TEST_TASK_DTL"
	COLUMNS = (
		("TASK_ID", "task_Id", "getStrTaskId", "setStrTaskId"),
		("DATA_SEQ", "data_Seq", "getNDataSeq", "setNDataSeq"),
		("ACT_TYPE", "act_Type", "getStrActType", "setStrActType"),
		("ACT_RESULT", "act_Result", "getStrActResult", "setStrActResult"),
		("ACT_STATE", "act_State", "getStrActState", "setStrActState"),
		("ELM_ID", "elm_Id", "getStrElmId", "setStrElmId"),
		("INPUT_VALUE", "input_Value", "getStrInputValue", "setStrInputValue"),
		("DELAY_TIME", "delay_Time", "getNDelayTime", "setNDelayTime"),
		("CAPTURE_IND", "capture_Ind", "getStrCaptureInd", "setStrCaptureInd"),
		("ACT_SBST", "act_Sbst", "getStrActSbst", "setStrActSbst"),
		("ACT_NO", "act_No", "getNActNo", "setNActNo"),
		("ACT_RST_SBST", "act_Rst_Sbst", "getStrActRstSbst", "setStrActRstSbst"),
		("ELM_TAG", "elm_Tag", "getStrElmTag", "setStrElmTag"),
		("ELM_NM", "elm_Nm", "getStrElmNm", "setStrElmNm"),
		("ELM_TYPE", "elm_Type", "getStrElmType", "setStrElmType"),
		("ELM_SEQ", "elm_Seq", "getStrElmSeq", "setStrElmSeq"),
		("ELM_CLASS", "elm_Class", "getStrElmClass", "setStrElmClass"),
		("INNER_TEXT", "inner_Text", "getStrInnerText", "setStrInnerText"),
		("ERROR_CLASS", "error_Class", "getStrErrorClass", "setStrErrorClass"),
		("ERROR_MSG", "error_Msg", "getStrErrorMsg", "setStrErrorMsg"),
		("PAGE_NO", "page_No", "getStrPageNo", "setStrPageNo"),
		("TARGET", "target", "getStrTarget", "setStrTarget"),
	)

	def __init__(self):
		self.m_strTaskId = None
		self.m_nDataSeq = 0
		self.m_strActType = None
		self.m_strActResult = None
		self.m_strActState = None
		self.m_strElmId = None
		self.m_strInputValue = None
		self.m_nDelayTime = 2
		self.m_strCaptureInd = None
		self.m_strActSbst = None
		self.m_nActNo = 0
		self.m_strActRstSbst = None
		self.m_strElmTag = None
		self.m_strElmNm = None
		self.m_strElmType = None
		self.m_strElmSeq = None
		self.m_strElmClass = None
		self.m_strInnerText = None
		self.m_strErrorClass = None
		self.m_strErrorMsg = None
		self.m_strPageNo = None
		self.m_strTarget = None

	@staticmethod
	def fromRow(oRow):
		oDto = TestInfoDTO()
		lstKeys = oRow.keys()
		for arrColumn in TestInfoDTO.COLUMNS:
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

	def getNDataSeq(self):
		return self.m_nDataSeq

	def setNDataSeq(self, nValue):
		if nValue is None:
			self.m_nDataSeq = 0
		else:
			self.m_nDataSeq = int(nValue)

	def getStrActType(self):
		return self.m_strActType

	def setStrActType(self, strValue):
		if strValue is None:
			self.m_strActType = None
		else:
			self.m_strActType = str(strValue)

	def getStrActResult(self):
		return self.m_strActResult

	def setStrActResult(self, strValue):
		if strValue is None:
			self.m_strActResult = None
		else:
			self.m_strActResult = str(strValue)

	def getStrActState(self):
		return self.m_strActState

	def setStrActState(self, strValue):
		if strValue is None:
			self.m_strActState = None
		else:
			self.m_strActState = str(strValue)

	def getStrElmId(self):
		return self.m_strElmId

	def setStrElmId(self, strValue):
		if strValue is None:
			self.m_strElmId = None
		else:
			self.m_strElmId = str(strValue)

	def getStrInputValue(self):
		return self.m_strInputValue

	def setStrInputValue(self, strValue):
		if strValue is None:
			self.m_strInputValue = None
		else:
			self.m_strInputValue = str(strValue)

	def getNDelayTime(self):
		return self.m_nDelayTime

	def setNDelayTime(self, nValue):
		if nValue is None:
			self.m_nDelayTime = 0
		else:
			self.m_nDelayTime = int(nValue)

	def getStrCaptureInd(self):
		return self.m_strCaptureInd

	def setStrCaptureInd(self, strValue):
		if strValue is None:
			self.m_strCaptureInd = None
		else:
			self.m_strCaptureInd = str(strValue)

	def getStrActSbst(self):
		return self.m_strActSbst

	def setStrActSbst(self, strValue):
		if strValue is None:
			self.m_strActSbst = None
		else:
			self.m_strActSbst = str(strValue)

	def getNActNo(self):
		return self.m_nActNo

	def setNActNo(self, nValue):
		if nValue is None:
			self.m_nActNo = 0
		else:
			self.m_nActNo = int(nValue)

	def getStrActRstSbst(self):
		return self.m_strActRstSbst

	def setStrActRstSbst(self, strValue):
		if strValue is None:
			self.m_strActRstSbst = None
		else:
			self.m_strActRstSbst = str(strValue)

	def getStrElmTag(self):
		return self.m_strElmTag

	def setStrElmTag(self, strValue):
		if strValue is None:
			self.m_strElmTag = None
		else:
			self.m_strElmTag = str(strValue)

	def getStrElmNm(self):
		return self.m_strElmNm

	def setStrElmNm(self, strValue):
		if strValue is None:
			self.m_strElmNm = None
		else:
			self.m_strElmNm = str(strValue)

	def getStrElmType(self):
		return self.m_strElmType

	def setStrElmType(self, strValue):
		if strValue is None:
			self.m_strElmType = None
		else:
			self.m_strElmType = str(strValue)

	def getStrElmSeq(self):
		return self.m_strElmSeq

	def setStrElmSeq(self, strValue):
		if strValue is None:
			self.m_strElmSeq = None
		else:
			self.m_strElmSeq = str(strValue)

	def getStrElmClass(self):
		return self.m_strElmClass

	def setStrElmClass(self, strValue):
		if strValue is None:
			self.m_strElmClass = None
		else:
			self.m_strElmClass = str(strValue)

	def getStrInnerText(self):
		return self.m_strInnerText

	def setStrInnerText(self, strValue):
		if strValue is None:
			self.m_strInnerText = None
		else:
			self.m_strInnerText = str(strValue)

	def getStrErrorClass(self):
		return self.m_strErrorClass

	def setStrErrorClass(self, strValue):
		if strValue is None:
			self.m_strErrorClass = None
		else:
			self.m_strErrorClass = str(strValue)

	def getStrErrorMsg(self):
		return self.m_strErrorMsg

	def setStrErrorMsg(self, strValue):
		if strValue is None:
			self.m_strErrorMsg = None
		else:
			self.m_strErrorMsg = str(strValue)

	def getStrPageNo(self):
		return self.m_strPageNo

	def setStrPageNo(self, strValue):
		if strValue is None:
			self.m_strPageNo = None
		else:
			self.m_strPageNo = str(strValue)

	def getStrTarget(self):
		return self.m_strTarget

	def setStrTarget(self, strValue):
		if strValue is None:
			self.m_strTarget = None
		else:
			self.m_strTarget = str(strValue)

	def toParams(self):
		mapParams = {}
		for arrColumn in TestInfoDTO.COLUMNS:
			fnGetter = getattr(self, arrColumn[2])
			mapParams[arrColumn[1]] = fnGetter()
		return mapParams
