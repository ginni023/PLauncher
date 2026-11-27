class TestCommDTO:

	TABLE_NAME = "TEST_COMM_LIST"
	COLUMNS = (
		("META_KEY", "meta_Key", "getStrMetaKey", "setStrMetaKey"),
		("UPR_DIV_KEY", "upr_Div_Key", "getStrUprDivKey", "setStrUprDivKey"),
		("SYS_RECD_CRET_DT", "sys_Recd_Cret_Dt", "getStrSysRecdCretDt", "setStrSysRecdCretDt"),
		("SYS_RECD_CHG_DT", "sys_Recd_Chg_Dt", "getStrSysRecdChgDt", "setStrSysRecdChgDt"),
		("DIS_NM", "dis_Nm", "getStrDisNm", "setStrDisNm"),
		("ALIAS_NM", "alias_Nm", "getStrAliasNm", "setStrAliasNm"),
		("META_VALUE", "meta_Value", "getStrMetaValue", "setStrMetaValue"),
		("VALUE_DESC", "value_Desc", "getStrValueDesc", "setStrValueDesc"),
	)

	def __init__(self):
		self.m_strMetaKey = None
		self.m_strUprDivKey = None
		self.m_strSysRecdCretDt = None
		self.m_strSysRecdChgDt = None
		self.m_strDisNm = None
		self.m_strAliasNm = None
		self.m_strMetaValue = None
		self.m_strValueDesc = None

	@staticmethod
	def fromRow(oRow):
		oDto = TestCommDTO()
		lstKeys = oRow.keys()
		for arrColumn in TestCommDTO.COLUMNS:
			if arrColumn[0] in lstKeys:
				fnSetter = getattr(oDto, arrColumn[3])
				fnSetter(oRow[arrColumn[0]])
		return oDto

	def getStrMetaKey(self):
		return self.m_strMetaKey

	def setStrMetaKey(self, strValue):
		if strValue is None:
			self.m_strMetaKey = None
		else:
			self.m_strMetaKey = str(strValue)

	def getStrUprDivKey(self):
		return self.m_strUprDivKey

	def setStrUprDivKey(self, strValue):
		if strValue is None:
			self.m_strUprDivKey = None
		else:
			self.m_strUprDivKey = str(strValue)

	def getStrSysRecdCretDt(self):
		return self.m_strSysRecdCretDt

	def setStrSysRecdCretDt(self, strValue):
		if strValue is None:
			self.m_strSysRecdCretDt = None
		else:
			self.m_strSysRecdCretDt = str(strValue)

	def getStrSysRecdChgDt(self):
		return self.m_strSysRecdChgDt

	def setStrSysRecdChgDt(self, strValue):
		if strValue is None:
			self.m_strSysRecdChgDt = None
		else:
			self.m_strSysRecdChgDt = str(strValue)

	def getStrDisNm(self):
		return self.m_strDisNm

	def setStrDisNm(self, strValue):
		if strValue is None:
			self.m_strDisNm = None
		else:
			self.m_strDisNm = str(strValue)

	def getStrAliasNm(self):
		return self.m_strAliasNm

	def setStrAliasNm(self, strValue):
		if strValue is None:
			self.m_strAliasNm = None
		else:
			self.m_strAliasNm = str(strValue)

	def getStrMetaValue(self):
		return self.m_strMetaValue

	def setStrMetaValue(self, strValue):
		if strValue is None:
			self.m_strMetaValue = None
		else:
			self.m_strMetaValue = str(strValue)

	def getStrValueDesc(self):
		return self.m_strValueDesc

	def setStrValueDesc(self, strValue):
		if strValue is None:
			self.m_strValueDesc = None
		else:
			self.m_strValueDesc = str(strValue)

	def toParams(self):
		mapParams = {}
		for arrColumn in TestCommDTO.COLUMNS:
			fnGetter = getattr(self, arrColumn[2])
			mapParams[arrColumn[1]] = fnGetter()
		return mapParams
