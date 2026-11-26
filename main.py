import logging
import os
import sys

SOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "main")
sys.path.insert(0, SOURCE_DIR)

from KtopiaLauncher import KtopiaLauncher


def main():
	oLauncher = KtopiaLauncher(sys.argv[1:])
	try:
		oLauncher.run()
	except Exception:
		oLogger = logging.getLogger(__name__)
		oLogger.exception("launcher terminated by error")
		raise


if __name__ == "__main__":
	main()
