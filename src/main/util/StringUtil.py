class StringUtil:

	def __init__(self):
		raise TypeError("StringUtil cannot be instantiated")

	@staticmethod
	def isEmpty(strValue):
		return strValue is None or len(strValue) == 0

	@staticmethod
	def nvl(strValue, strDefault):
		if StringUtil.isEmpty(strValue):
			return strDefault
		return strValue

	@staticmethod
	def equalsIgnoreCase(strValue1, strValue2):
		if strValue1 is None or strValue2 is None:
			return strValue1 is None and strValue2 is None
		strFolded1 = strValue1.casefold()
		strFolded2 = strValue2.casefold()
		return strFolded1 == strFolded2

	@staticmethod
	def isPositiveInteger(strValue):
		if StringUtil.isEmpty(strValue):
			return False
		if not strValue.isdigit():
			return False
		return int(strValue) > 0
