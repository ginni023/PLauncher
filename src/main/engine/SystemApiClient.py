import logging

from util.StringUtil import StringUtil


class SystemApiClient:

	LOGGER = logging.getLogger(__name__)

	def __init__(self):
		raise TypeError("SystemApiClient cannot be instantiated")

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
	def authenticate(strDomain, strTrtrId):
		SystemApiClient.LOGGER.info("authenticate not implemented yet : %s / %s", strDomain, strTrtrId)
		return not StringUtil.isEmpty(strTrtrId)
