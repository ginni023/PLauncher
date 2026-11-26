import logging
import socket
import threading


class SingleInstanceServer:

	LOGGER = logging.getLogger(__name__)
	HOST = "127.0.0.1"
	PORT = 47321
	BUFFER_SIZE = 4096
	BACKLOG = 5
	ENCODING = "utf-8"
	CONNECT_TIMEOUT_SECONDS = 3

	def __init__(self, fnOnMessage):
		self.m_fnOnMessage = fnOnMessage
		self.m_oSocket = None
		self.m_oThread = None
		self.m_bRunning = False

	@staticmethod
	def sendToRunning(strMessage):
		oSocket = socket.create_connection((SingleInstanceServer.HOST, SingleInstanceServer.PORT),
										   timeout=SingleInstanceServer.CONNECT_TIMEOUT_SECONDS)
		try:
			byData = strMessage.encode(SingleInstanceServer.ENCODING)
			oSocket.sendall(byData)
			oSocket.shutdown(socket.SHUT_WR)
		finally:
			oSocket.close()

	def start(self):
		oSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
			oSocket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
		try:
			oSocket.bind((SingleInstanceServer.HOST, SingleInstanceServer.PORT))
		except OSError:
			oSocket.close()
			return False
		oSocket.listen(SingleInstanceServer.BACKLOG)
		self.m_oSocket = oSocket
		self.m_bRunning = True
		self.m_oThread = threading.Thread(target=self._acceptLoop, name="SingleInstanceServer", daemon=True)
		self.m_oThread.start()
		return True

	def stop(self):
		self.m_bRunning = False
		if self.m_oSocket is not None:
			self.m_oSocket.close()
			self.m_oSocket = None

	def _acceptLoop(self):
		while self.m_bRunning:
			try:
				arrAccepted = self.m_oSocket.accept()
			except OSError:
				break
			try:
				strMessage = self._receive(arrAccepted[0])
				self.m_fnOnMessage(strMessage)
			except Exception:
				SingleInstanceServer.LOGGER.exception("failed to handle message from another instance")

	def _receive(self, oConnection):
		lstChunks = []
		try:
			while True:
				byChunk = oConnection.recv(SingleInstanceServer.BUFFER_SIZE)
				if len(byChunk) == 0:
					break
				lstChunks.append(byChunk)
		finally:
			oConnection.close()
		byData = b"".join(lstChunks)
		return byData.decode(SingleInstanceServer.ENCODING)
