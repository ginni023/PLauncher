from runner.CrawlingRunner import CrawlingRunner
from util.StringUtil import StringUtil
from task.code.TaskType import TaskType
from runner.UiTestRunner import UiTestRunner


class TaskRunner:

	def __init__(self):
		raise TypeError("TaskRunner cannot be instantiated")

	@staticmethod
	def run(oTask, oConfig, oStopEvent, oTaskManager):
		strTaskType = oTask.getStrTaskType()
		if StringUtil.equalsIgnoreCase(strTaskType, TaskType.CRAWLING):
			CrawlingRunner.run(oTask, oConfig, oStopEvent, oTaskManager)
			return
		if StringUtil.equalsIgnoreCase(strTaskType, TaskType.VALIDATION):
			CrawlingRunner.run(oTask, oConfig, oStopEvent, oTaskManager)
			return
		UiTestRunner.run(oTask, oConfig, oStopEvent, oTaskManager)
