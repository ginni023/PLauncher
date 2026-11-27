import json
import logging
import urllib.request

from util.StringUtil import StringUtil


class SystemApiClient:

	LOGGER = logging.getLogger(__name__)
	SERVER_DATA_PATH = "/api/launcher/getServerData"
	REQUEST_TIMEOUT_SECONDS = 10
	HEADER_CONTENT_TYPE = "Content-Type"
	HEADER_AUTHORIZATION = "Authorization"
	AUTH_SCHEME_BEARER = "Bearer "
	CONTENT_TYPE_JSON = "application/json; charset=utf-8"
	METHOD_POST = "POST"
	ENCODING = "utf-8"
	REQUEST_SYSTEM_ID = "systemId"
	REQUEST_TYPE = "type"
	URL_SEPARATOR = "/"
	ERROR_NO_DOMAIN = "서버 주소(domain)가 없습니다."
	ERROR_NOT_OBJECT = "서버 응답이 JSON 객체가 아닙니다 : "

	s_strAuthToken = ""

	def __init__(self):
		raise TypeError("SystemApiClient cannot be instantiated")

	@staticmethod
	def setAuthToken(strToken):
		if strToken is None:
			SystemApiClient.s_strAuthToken = ""
		else:
			SystemApiClient.s_strAuthToken = strToken.strip()

	@staticmethod
	def hasAuthToken():
		return not StringUtil.isEmpty(SystemApiClient.s_strAuthToken)

	@staticmethod
	def fetchLatestVersion(strDomain, strCurrentVersion):
		SystemApiClient.LOGGER.info("fetchLatestVersion not implemented yet : %s (current %s)", strDomain,
									strCurrentVersion)
		return strCurrentVersion

	@staticmethod
	def fetchReservations(strDomain):
		SystemApiClient.LOGGER.info("fetchReservations not implemented yet : %s", strDomain)
		return []

	@staticmethod
	def authenticate(strDomain, strToken):
		SystemApiClient.LOGGER.info("authenticate not implemented yet : %s", strDomain)
		return not StringUtil.isEmpty(strToken)

	@staticmethod
	def getServerData(strDomain, strSystemId, strType):
		strUrl = SystemApiClient.buildUrl(strDomain, SystemApiClient.SERVER_DATA_PATH)
		mapRequest = {}
		mapRequest[SystemApiClient.REQUEST_SYSTEM_ID] = strSystemId
		mapRequest[SystemApiClient.REQUEST_TYPE] = strType
		return SystemApiClient.postJson(strUrl, mapRequest)

	@staticmethod
	def buildUrl(strDomain, strPath):
		if StringUtil.isEmpty(strDomain):
			raise ValueError(SystemApiClient.ERROR_NO_DOMAIN)
		strBase = strDomain.rstrip(SystemApiClient.URL_SEPARATOR)
		return strBase + strPath

	@staticmethod
	def postJson(strUrl, mapRequest):
		strBody = json.dumps(mapRequest, ensure_ascii=False)
		byBody = strBody.encode(SystemApiClient.ENCODING)
		oRequest = urllib.request.Request(strUrl, data=byBody, method=SystemApiClient.METHOD_POST)
		oRequest.add_header(SystemApiClient.HEADER_CONTENT_TYPE, SystemApiClient.CONTENT_TYPE_JSON)
		bHasToken = SystemApiClient.hasAuthToken()
		if bHasToken:
			strAuthorization = SystemApiClient.AUTH_SCHEME_BEARER + SystemApiClient.s_strAuthToken
			oRequest.add_header(SystemApiClient.HEADER_AUTHORIZATION, strAuthorization)
		SystemApiClient.LOGGER.info("api request : %s %s (token %s)", strUrl, strBody, bHasToken)
		with urllib.request.urlopen(oRequest, timeout=SystemApiClient.REQUEST_TIMEOUT_SECONDS) as oResponse:
			byResponse = oResponse.read()
		strResponse = byResponse.decode(SystemApiClient.ENCODING)
		SystemApiClient.LOGGER.info("api response : %s %s", strUrl, strResponse)
		oData = json.loads(strResponse)
		if not isinstance(oData, dict):
			raise ValueError(SystemApiClient.ERROR_NOT_OBJECT + strResponse)
		return oData
