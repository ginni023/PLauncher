import ttkbootstrap as tb


class ChildDialog(tb.Toplevel):

	PADDING = 16

	def __init__(self, oParent, strTitle, nWidth, nHeight, fnOnClose):
		tb.Toplevel.__init__(self, master=oParent)
		self.m_oParent = oParent
		self.m_fnOnClose = fnOnClose
		self.m_oChildDialog = None
		self.withdraw()
		self.title(strTitle)
		self.resizable(False, False)
		self.transient(oParent)
		self.protocol("WM_DELETE_WINDOW", self.closeDialog)
		self._placeOnParent(nWidth, nHeight)

	def showModal(self):
		self.deiconify()
		self.wait_visibility()
		self.grab_set()
		self.focus_set()

	def bringToFront(self):
		if self.m_oChildDialog is not None:
			self.m_oChildDialog.bringToFront()
			return
		self.lift()
		self.focus_set()

	def refresh(self):
		return

	def closeDialog(self):
		self.grab_release()
		if isinstance(self.m_oParent, ChildDialog):
			self.m_oParent.onChildClosed(self)
			self.m_oParent.grab_set()
		fnOnClose = self.m_fnOnClose
		self.destroy()
		if fnOnClose is not None:
			fnOnClose(self)

	def openChild(self, oDialog):
		self.m_oChildDialog = oDialog
		oDialog.showModal()

	def onChildClosed(self, oDialog):
		if self.m_oChildDialog is oDialog:
			self.m_oChildDialog = None

	def _placeOnParent(self, nWidth, nHeight):
		self.m_oParent.update_idletasks()
		nParentX = self.m_oParent.winfo_rootx()
		nParentY = self.m_oParent.winfo_rooty()
		nParentWidth = self.m_oParent.winfo_width()
		nParentHeight = self.m_oParent.winfo_height()
		nX = max(nParentX + (nParentWidth - nWidth) // 2, 0)
		nY = max(nParentY + (nParentHeight - nHeight) // 2, 0)
		self.geometry(str(nWidth) + "x" + str(nHeight) + "+" + str(nX) + "+" + str(nY))
