import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class IconFactory:

	BACKGROUND_COLOR = (30, 90, 200, 255)
	TEXT_COLOR = (255, 255, 255, 255)
	TRANSPARENT = (0, 0, 0, 0)
	LETTER = "K"
	FONT_FILE_NAME = "arialbd.ttf"
	WINDOWS_DIR_ENV = "WINDIR"
	DEFAULT_WINDOWS_DIR = "C:\\Windows"
	FONTS_DIR_NAME = "Fonts"
	RADIUS_RATIO = 5
	FONT_RATIO = 0.7

	def __init__(self):
		raise TypeError("IconFactory cannot be instantiated")

	@staticmethod
	def createImage(nSize):
		oImage = Image.new("RGBA", (nSize, nSize), IconFactory.TRANSPARENT)
		oDraw = ImageDraw.Draw(oImage)
		nRadius = nSize // IconFactory.RADIUS_RATIO
		oDraw.rounded_rectangle((0, 0, nSize - 1, nSize - 1), radius=nRadius, fill=IconFactory.BACKGROUND_COLOR)
		oFont = IconFactory._loadFont(int(nSize * IconFactory.FONT_RATIO))
		arrBox = oDraw.textbbox((0, 0), IconFactory.LETTER, font=oFont)
		nX = (nSize - (arrBox[2] - arrBox[0])) // 2 - arrBox[0]
		nY = (nSize - (arrBox[3] - arrBox[1])) // 2 - arrBox[1]
		oDraw.text((nX, nY), IconFactory.LETTER, font=oFont, fill=IconFactory.TEXT_COLOR)
		return oImage

	@staticmethod
	def _loadFont(nPixelSize):
		strWindowsDir = os.environ.get(IconFactory.WINDOWS_DIR_ENV, IconFactory.DEFAULT_WINDOWS_DIR)
		strFontPath = os.path.join(strWindowsDir, IconFactory.FONTS_DIR_NAME, IconFactory.FONT_FILE_NAME)
		if os.path.isfile(strFontPath):
			return ImageFont.truetype(strFontPath, nPixelSize)
		return ImageFont.load_default(nPixelSize)
