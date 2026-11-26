import logging

from task.code.TaskStatus import TaskStatus


class CrawlingRunner:

	LOGGER = logging.getLogger(__name__)
	STUB_SECONDS = 3
	RESULT_NOT_IMPLEMENTED = "크롤링 실행 기능 미구현"

	def __init__(self):
		raise TypeError("CrawlingRunner cannot be instantiated")

	@staticmethod
	def run(oTask, oConfig, oStopEvent):
		CrawlingRunner.LOGGER.info("crawling start (stub) : %s", oTask.getStrTaskId())
		oStopEvent.wait(CrawlingRunner.STUB_SECONDS)
		if oStopEvent.is_set():
			return
		oTask.setStrTestStatus(TaskStatus.CMP)
		oTask.setStrTestResult(CrawlingRunner.RESULT_NOT_IMPLEMENTED)
