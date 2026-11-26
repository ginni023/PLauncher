import datetime


class DateUtil:

	DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
	TIMESTAMP_FORMAT = "%Y%m%d%H%M%S"

	def __init__(self):
		raise TypeError("DateUtil cannot be instantiated")

	@staticmethod
	def getNowDateTime():
		oNow = datetime.datetime.now()
		return oNow.strftime(DateUtil.DATE_TIME_FORMAT)

	@staticmethod
	def getNowTimestamp():
		oNow = datetime.datetime.now()
		return oNow.strftime(DateUtil.TIMESTAMP_FORMAT)
