import logging

from task.code.TaskStatus import TaskStatus


class UiTestRunner:

	LOGGER = logging.getLogger(__name__)
	STUB_SECONDS = 3
	RESULT_NOT_IMPLEMENTED = "UI TEST(Playwright) 실행 기능 미구현"

	def __init__(self):
		raise TypeError("UiTestRunner cannot be instantiated")

	@staticmethod
	def run(oTask, oConfig, oStopEvent, oTaskManager):
		UiTestRunner.LOGGER.info("ui test start (stub) : %s", oTask.getStrTaskId())
		oStopEvent.wait(UiTestRunner.STUB_SECONDS)
		if oStopEvent.is_set():
			return
		oTask.setStrTestStatus(TaskStatus.CMP)
		oTask.setStrTestResult(UiTestRunner.RESULT_NOT_IMPLEMENTED)
