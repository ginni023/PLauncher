import urllib.parse

from util.DateUtil import DateUtil
from task.code.DtlType import DtlType
from util.StringUtil import StringUtil
from util.Util import Util
from task.code.TaskStatus import TaskStatus
from task.code.TaskType import TaskType
from dto.TestTaskDTO import TestTaskDTO


class LaunchUrlParser:

	SCHEME = "ktopia"
	ACTION_START = "start"
	PARAM_DOMAIN = "domain"
	PARAM_REQ_PROD_SEQ = "reqProdSeq"
	PARAM_EXE_SEQ = "exeSeq"
	PARAM_CHORD_ID = "chordId"
	PARAM_CHORD_TYPE = "chordType"
	PARAM_CHORD_TOKEN = "chordToken"
	PARAM_MODE = "mode"
	PARAM_SYSTEM_ID = "systemId"
	MODE_CRAWLING = "CRAWLING"
	SCHEME_SEPARATOR = "://"
	WINDOWS_ADDED_PATH = "/"
	QUERY_DELIMITER = "?"
	PARAM_DELIMITER = "&"
	VALUE_DELIMITER = "="

	ERROR_INVALID_SCHEME = "ktopia:// 주소가 아닙니다."
	ERROR_INVALID_ACTION = "지원하지 않는 실행 동작입니다 : "
	ERROR_NO_DOMAIN = "domain 파라미터가 없습니다."
	ERROR_NO_SYSTEM_ID = "systemId 파라미터가 없습니다. (mode=CRAWLING)"
	ERROR_UNKNOWN_TASK = "작업 타입을 알 수 없습니다. (mode=CRAWLING, reqProdSeq·exeSeq·chordId 또는 chordToken 필요)"

	def __init__(self):
		raise TypeError("LaunchUrlParser cannot be instantiated")

	@staticmethod
	def isLaunchUrl(strValue):
		if StringUtil.isEmpty(strValue):
			return False
		strPrefix = LaunchUrlParser.SCHEME + ":"
		strHead = strValue[:len(strPrefix)]
		return StringUtil.equalsIgnoreCase(strHead, strPrefix)

	@staticmethod
	def parse(strUrl):
		oParts = urllib.parse.urlsplit(strUrl)
		if not StringUtil.equalsIgnoreCase(oParts.scheme, LaunchUrlParser.SCHEME):
			raise ValueError(LaunchUrlParser.ERROR_INVALID_SCHEME)
		strAction = oParts.netloc
		if StringUtil.isEmpty(strAction):
			strAction = oParts.path.strip("/")
		if not StringUtil.equalsIgnoreCase(strAction, LaunchUrlParser.ACTION_START):
			raise ValueError(LaunchUrlParser.ERROR_INVALID_ACTION + strAction)

		mapParams = LaunchUrlParser.parseParams(strUrl)
		strDomain = LaunchUrlParser.getParam(mapParams, LaunchUrlParser.PARAM_DOMAIN)
		if StringUtil.isEmpty(strDomain):
			raise ValueError(LaunchUrlParser.ERROR_NO_DOMAIN)

		strReqProdSeq = LaunchUrlParser.getParam(mapParams, LaunchUrlParser.PARAM_REQ_PROD_SEQ)
		strExeSeq = LaunchUrlParser.getParam(mapParams, LaunchUrlParser.PARAM_EXE_SEQ)
		strChordId = LaunchUrlParser.getParam(mapParams, LaunchUrlParser.PARAM_CHORD_ID)
		strChordType = LaunchUrlParser.getParam(mapParams, LaunchUrlParser.PARAM_CHORD_TYPE)
		strChordToken = LaunchUrlParser.getParam(mapParams, LaunchUrlParser.PARAM_CHORD_TOKEN)
		strMode = LaunchUrlParser.getParam(mapParams, LaunchUrlParser.PARAM_MODE)
		strSystemId = LaunchUrlParser.getParam(mapParams, LaunchUrlParser.PARAM_SYSTEM_ID)

		oTask = TestTaskDTO()
		oTask.setStrTaskId(Util.makeTaskId())
		oTask.setStrSysRecdCretDt(DateUtil.getNowDateTime())
		oTask.setStrTaskAdr(LaunchUrlParser.restoreOriginalUrl(strUrl))
		oTask.setStrTestStatus(TaskStatus.RDY)
		oTask.setStrChordType(strChordType)

		if StringUtil.equalsIgnoreCase(strMode, LaunchUrlParser.MODE_CRAWLING):
			if StringUtil.isEmpty(strSystemId):
				raise ValueError(LaunchUrlParser.ERROR_NO_SYSTEM_ID)
			oTask.setStrTaskType(TaskType.CRAWLING)
			oTask.setStrChordId(strSystemId)
			return oTask
		bUiTest = not StringUtil.isEmpty(strReqProdSeq) and not StringUtil.isEmpty(strExeSeq) \
			and not StringUtil.isEmpty(strChordId)
		if bUiTest:
			oTask.setStrTaskType(TaskType.STANDARD)
			oTask.setStrDtlType(DtlType.PLAYWRIGHT)
			oTask.setStrReqProdSeq(strReqProdSeq)
			oTask.setStrExeCd(strExeSeq)
			oTask.setStrChordId(strChordId)
			return oTask
		if not StringUtil.isEmpty(strChordToken):
			oTask.setStrTaskType(TaskType.VALIDATION)
			oTask.setStrChordId(strChordToken)
			return oTask
		raise ValueError(LaunchUrlParser.ERROR_UNKNOWN_TASK)

	@staticmethod
	def restoreOriginalUrl(strUrl):
		oParts = urllib.parse.urlsplit(strUrl)
		if oParts.path != LaunchUrlParser.WINDOWS_ADDED_PATH:
			return strUrl
		nHeadLength = len(oParts.scheme) + len(LaunchUrlParser.SCHEME_SEPARATOR) + len(oParts.netloc)
		strHead = strUrl[:nHeadLength]
		strRest = strUrl[nHeadLength + len(LaunchUrlParser.WINDOWS_ADDED_PATH):]
		return strHead + strRest

	@staticmethod
	def parseParams(strUrl):
		mapParams = {}
		nQueryPos = strUrl.find(LaunchUrlParser.QUERY_DELIMITER)
		if nQueryPos < 0:
			return mapParams
		strQuery = strUrl[nQueryPos + len(LaunchUrlParser.QUERY_DELIMITER):]
		lstPairs = strQuery.split(LaunchUrlParser.PARAM_DELIMITER)
		for strPair in lstPairs:
			if StringUtil.isEmpty(strPair):
				continue
			nValuePos = strPair.find(LaunchUrlParser.VALUE_DELIMITER)
			if nValuePos < 0:
				strKey = strPair
				strRawValue = ""
			else:
				strKey = strPair[:nValuePos]
				strRawValue = strPair[nValuePos + len(LaunchUrlParser.VALUE_DELIMITER):]
			strTrimmedKey = strKey.strip()
			strUpperKey = strTrimmedKey.upper()
			if StringUtil.isEmpty(strUpperKey) or strUpperKey in mapParams:
				continue
			strValue = urllib.parse.unquote(strRawValue)
			mapParams[strUpperKey] = strValue.strip()
		return mapParams

	@staticmethod
	def getParam(mapParams, strName):
		strKey = strName.upper()
		return mapParams.get(strKey, "")
