import logging
import threading
import time

from engine.LauncherConfig import LauncherConfig
from engine.SystemApiClient import SystemApiClient


class ReservationScheduler:

	LOGGER = logging.getLogger(__name__)
	DUE_CHECK_SECONDS = 10
	SECONDS_PER_MINUTE = 60

	def __init__(self, oConfig, oTaskManager):
		self.m_oConfig = oConfig
		self.m_oTaskManager = oTaskManager
		self.m_oStopEvent = threading.Event()
		self.m_oThread = None
		self.m_dLastFetchTime = None

	def start(self):
		self.m_oThread = threading.Thread(target=self._loop, name="ReservationScheduler", daemon=True)
		self.m_oThread.start()

	def stop(self):
		self.m_oStopEvent.set()

	def _loop(self):
		while not self.m_oStopEvent.wait(ReservationScheduler.DUE_CHECK_SECONDS):
			try:
				self._checkOnce()
			except Exception:
				ReservationScheduler.LOGGER.exception("reservation check failed")

	def _checkOnce(self):
		if self.m_oConfig.isYes(LauncherConfig.RESERVATION_USE):
			dNow = time.monotonic()
			nIntervalSeconds = self.m_oConfig.getReservationCheckMinutes() * ReservationScheduler.SECONDS_PER_MINUTE
			if self.m_dLastFetchTime is None or dNow - self.m_dLastFetchTime >= nIntervalSeconds:
				self.m_dLastFetchTime = dNow
				self._fetchReservations()
		self.m_oTaskManager.checkReservations()

	def _fetchReservations(self):
		strDomain = self.m_oConfig.getValue(LauncherConfig.RESERVATION_SYSTEM)
		lstTasks = SystemApiClient.fetchReservations(strDomain)
		for oTask in lstTasks:
			self.m_oTaskManager.addTask(oTask)
