import logging
import os
import sqlite3
import threading
import xml.etree.ElementTree as ElementTree

from util.PathUtil import PathUtil


class DatabaseUtil:

	LOGGER = logging.getLogger(__name__)
	DB_FILE_NAME = "ktopia.db"
	INIT_SQL_FILE_NAME = "initSql.xml"
	MAIN_SQL_FILE_NAME = "mainSql.xml"
	SQL_TAG = "sql"
	ATTR_ID = "id"
	ATTR_VERSION = "version"
	ATTR_TYPE = "type"
	QUERY_TYPE_SELECT = "S"
	EXECUTE_QUERY_TYPES = ("I", "U", "D")

	s_mapSelectQuery = {}
	s_mapExecuteQuery = {}
	s_mapSystemQuery = {}
	s_oLock = threading.Lock()

	def __init__(self):
		raise TypeError("DatabaseUtil cannot be instantiated")

	@staticmethod
	def getDbPath():
		return os.path.join(PathUtil.getDbDir(), DatabaseUtil.DB_FILE_NAME)

	@staticmethod
	def getInitSqlPath():
		return os.path.join(PathUtil.getDbDir(), DatabaseUtil.INIT_SQL_FILE_NAME)

	@staticmethod
	def getMainSqlPath():
		return os.path.join(PathUtil.getDbDir(), DatabaseUtil.MAIN_SQL_FILE_NAME)

	@staticmethod
	def connect():
		os.makedirs(PathUtil.getDbDir(), exist_ok=True)
		oConn = sqlite3.connect(DatabaseUtil.getDbPath())
		oConn.row_factory = sqlite3.Row
		oConn.execute("PRAGMA foreign_keys = ON")
		return oConn

	@staticmethod
	def initDb():
		lstSqls = DatabaseUtil._loadSqlList(DatabaseUtil.getInitSqlPath())
		oConn = DatabaseUtil.connect()
		try:
			oCursor = oConn.execute("PRAGMA user_version")
			oRow = oCursor.fetchone()
			nCurrentVersion = oRow[0]
			nLatestVersion = nCurrentVersion
			for arrSql in lstSqls:
				if arrSql[1] > nCurrentVersion:
					oConn.executescript(arrSql[2])
					nLatestVersion = max(nLatestVersion, arrSql[1])
					DatabaseUtil.LOGGER.info("initSql applied : %s (version %d)", arrSql[0], arrSql[1])
			if nLatestVersion != nCurrentVersion:
				oConn.execute("PRAGMA user_version = " + str(nLatestVersion))
			oConn.commit()
		finally:
			oConn.close()

	@staticmethod
	def initMappingQuery():
		mapSelectQuery = {}
		mapExecuteQuery = {}
		mapSystemQuery = {}
		lstMainSqls = DatabaseUtil._loadSqlList(DatabaseUtil.getMainSqlPath())
		for arrSql in lstMainSqls:
			strType = arrSql[3]
			if strType == DatabaseUtil.QUERY_TYPE_SELECT:
				mapSelectQuery[arrSql[0]] = arrSql[2]
			elif strType in DatabaseUtil.EXECUTE_QUERY_TYPES:
				mapExecuteQuery[arrSql[0]] = arrSql[2]
			else:
				raise ValueError("mainSql.xml sql has no valid type (S/I/U/D) : " + arrSql[0])
		lstInitSqls = DatabaseUtil._loadSqlList(DatabaseUtil.getInitSqlPath())
		for arrSql in lstInitSqls:
			mapSystemQuery[arrSql[0]] = arrSql[2]
		with DatabaseUtil.s_oLock:
			DatabaseUtil.s_mapSelectQuery = mapSelectQuery
			DatabaseUtil.s_mapExecuteQuery = mapExecuteQuery
			DatabaseUtil.s_mapSystemQuery = mapSystemQuery
		DatabaseUtil.LOGGER.info("query mapped : select %d, execute %d, system %d",
								 len(mapSelectQuery), len(mapExecuteQuery), len(mapSystemQuery))

	@staticmethod
	def getSelectQuery(strSqlId):
		with DatabaseUtil.s_oLock:
			mapQuery = DatabaseUtil.s_mapSelectQuery
		if strSqlId not in mapQuery:
			raise KeyError("selectQueryMap has no sql id : " + strSqlId)
		return mapQuery[strSqlId]

	@staticmethod
	def getExecuteQuery(strSqlId):
		with DatabaseUtil.s_oLock:
			mapQuery = DatabaseUtil.s_mapExecuteQuery
		if strSqlId not in mapQuery:
			raise KeyError("executeQueryMap has no sql id : " + strSqlId)
		return mapQuery[strSqlId]

	@staticmethod
	def getSystemQuery(strSqlId):
		with DatabaseUtil.s_oLock:
			mapQuery = DatabaseUtil.s_mapSystemQuery
		if strSqlId not in mapQuery:
			raise KeyError("systemQueryMap has no sql id : " + strSqlId)
		return mapQuery[strSqlId]

	@staticmethod
	def executeUpdate(strSqlId, mapParams):
		strSql = DatabaseUtil.getExecuteQuery(strSqlId)
		oConn = DatabaseUtil.connect()
		try:
			oConn.execute(strSql, mapParams)
			oConn.commit()
		finally:
			oConn.close()

	@staticmethod
	def selectRows(strSqlId, mapParams):
		strSql = DatabaseUtil.getSelectQuery(strSqlId)
		oConn = DatabaseUtil.connect()
		try:
			oCursor = oConn.execute(strSql, mapParams)
			return oCursor.fetchall()
		finally:
			oConn.close()

	@staticmethod
	def _loadSqlList(strPath):
		oTree = ElementTree.parse(strPath)
		oRoot = oTree.getroot()
		lstSqls = []
		for oElement in oRoot.findall(DatabaseUtil.SQL_TAG):
			strId = oElement.get(DatabaseUtil.ATTR_ID)
			nVersion = int(oElement.get(DatabaseUtil.ATTR_VERSION, "0"))
			strType = oElement.get(DatabaseUtil.ATTR_TYPE, "")
			strText = oElement.text
			if strText is None:
				strText = ""
			lstSqls.append((strId, nVersion, strText.strip(), strType.upper()))
		return lstSqls
