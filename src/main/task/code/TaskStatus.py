from util.StringUtil import StringUtil


class TaskStatus:

	RDY = "RDY"
	WAIT = "WAIT"
	WRK = "WRK"
	CMP = "CMP"
	FAIL = "FAIL"
	ERR = "ERR"
	STOP = "STOP"
	FINISHED_STATUSES = (CMP, FAIL, ERR, STOP)
	LABELS = (
		(RDY, "대기중"),
		(WAIT, "작업준비중"),
		(WRK, "작동중"),
		(CMP, "완료"),
		(FAIL, "실패"),
		(ERR, "오류"),
		(STOP, "강제종료"),
	)

	def __init__(self):
		raise TypeError("TaskStatus cannot be instantiated")

	@staticmethod
	def isFinished(strStatus):
		for strFinished in TaskStatus.FINISHED_STATUSES:
			if StringUtil.equalsIgnoreCase(strStatus, strFinished):
				return True
		return False

	@staticmethod
	def getName(strStatus):
		if StringUtil.isEmpty(strStatus):
			return ""
		for arrLabel in TaskStatus.LABELS:
			if StringUtil.equalsIgnoreCase(strStatus, arrLabel[0]):
				return arrLabel[1]
		return strStatus

	@staticmethod
	def getLabel(strStatus):
		if StringUtil.isEmpty(strStatus):
			return ""
		for arrLabel in TaskStatus.LABELS:
			if StringUtil.equalsIgnoreCase(strStatus, arrLabel[0]):
				return arrLabel[1] + "(" + arrLabel[0] + ")"
		return strStatus
