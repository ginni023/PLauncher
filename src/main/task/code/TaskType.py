from util.StringUtil import StringUtil


class TaskType:

	STANDARD = "STANDARD"
	VALIDATION = "VALIDATION"
	RESERVATION = "RESERVATION"
	CRAWLING = "CRAWLING"
	LABELS = (
		(STANDARD, "기본수행"),
		(VALIDATION, "검사"),
		(RESERVATION, "예약"),
		(CRAWLING, "크롤링"),
	)

	def __init__(self):
		raise TypeError("TaskType cannot be instantiated")

	@staticmethod
	def getLabel(strTaskType):
		if StringUtil.isEmpty(strTaskType):
			return ""
		for arrLabel in TaskType.LABELS:
			if StringUtil.equalsIgnoreCase(strTaskType, arrLabel[0]):
				return arrLabel[1]
		return strTaskType
