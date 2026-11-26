import os

from util.DateUtil import DateUtil


class PropertiesUtil:

	ENCODING = "utf-8"
	COMMENT_CHARS = ("#", "!")
	SEPARATOR_CHARS = ("=", ":")
	ESCAPE_CHAR = "\\"
	ESCAPE_MAP = {"n": "\n", "r": "\r", "t": "\t"}

	def __init__(self):
		raise TypeError("PropertiesUtil cannot be instantiated")

	@staticmethod
	def load(strPath):
		mapValues = {}
		if not os.path.isfile(strPath):
			return mapValues
		with open(strPath, "r", encoding=PropertiesUtil.ENCODING) as oFile:
			for strLine in oFile:
				strTrimmed = strLine.strip()
				if len(strTrimmed) == 0:
					continue
				if strTrimmed[0] in PropertiesUtil.COMMENT_CHARS:
					continue
				nSeparatorPos = PropertiesUtil._findSeparator(strTrimmed)
				if nSeparatorPos < 0:
					mapValues[strTrimmed] = ""
					continue
				strKeyPart = strTrimmed[:nSeparatorPos]
				strValuePart = strTrimmed[nSeparatorPos + 1:]
				strKey = strKeyPart.strip()
				strValue = strValuePart.lstrip()
				mapValues[strKey] = PropertiesUtil.unescape(strValue)
		return mapValues

	@staticmethod
	def store(strPath, mapValues, arrKeyOrder, strHeader):
		lstLines = []
		lstLines.append("#" + strHeader)
		lstLines.append("#" + DateUtil.getNowDateTime())
		for strKey in arrKeyOrder:
			strValue = mapValues.get(strKey, "")
			lstLines.append(strKey + "=" + PropertiesUtil.escape(strValue))
		strContent = "\n".join(lstLines)
		with open(strPath, "w", encoding=PropertiesUtil.ENCODING, newline="\n") as oFile:
			oFile.write(strContent + "\n")

	@staticmethod
	def escape(strValue):
		if strValue is None:
			return ""
		strResult = strValue.replace("\\", "\\\\")
		strResult = strResult.replace("\n", "\\n")
		strResult = strResult.replace("\r", "\\r")
		strResult = strResult.replace("\t", "\\t")
		return strResult

	@staticmethod
	def unescape(strValue):
		lstChars = []
		nIndex = 0
		nLength = len(strValue)
		while nIndex < nLength:
			cChar = strValue[nIndex]
			if cChar == PropertiesUtil.ESCAPE_CHAR and nIndex + 1 < nLength:
				cNext = strValue[nIndex + 1]
				lstChars.append(PropertiesUtil.ESCAPE_MAP.get(cNext, cNext))
				nIndex += 2
				continue
			lstChars.append(cChar)
			nIndex += 1
		return "".join(lstChars)

	@staticmethod
	def _findSeparator(strLine):
		for nIndex in range(len(strLine)):
			if strLine[nIndex] in PropertiesUtil.SEPARATOR_CHARS:
				return nIndex
		return -1
