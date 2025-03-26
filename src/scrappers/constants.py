import os

THIS_FILE_PATH = os.path.abspath(os.path.dirname(__file__))
RELATIVE_CHROME_PATH = "../../drivers/chrome/chromedriver-linux64/chromedriver"
CHROME_PATH = os.path.join(THIS_FILE_PATH, RELATIVE_CHROME_PATH)