import threading

from util.DateUtil import DateUtil


class Util:

	DIGIT_SEQ_START = 1000

	s_nDigitSeq = DIGIT_SEQ_START
	s_oLock = threading.Lock()

	def __init__(self):
		raise TypeError("Util cannot be instantiated")

	@staticmethod
	def makeTaskId():
		strDateTime = DateUtil.getNowTimestamp()
		with Util.s_oLock:
			nDigitSeq = Util.s_nDigitSeq
			Util.s_nDigitSeq += 1
		return strDateTime + str(nDigitSeq)
