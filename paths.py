from datetime import datetime, timedelta, date

WINDOW_SIZE = '1300,1000'
CURRENT_PATH = 'C:\\Users\\MKINFO22\\Desktop\\seosik_2'
CHROMEDRIVER_PATH = f'{CURRENT_PATH}\\driver\\chromedriver.exe'
DATETIME_NOW = datetime.now().strftime("%Y%m%d_%H%M%S")
DATETIME_TODAY = datetime.now().strftime("%Y%m%d")
COOKIE_PATH = f'{CURRENT_PATH}\\cookies\\cookies.pkl'
ACC_PATH = f'{CURRENT_PATH}\\cookies\\acc.pkl'
DOWNLOAD_PATH = f'{CURRENT_PATH}\\Files\\{DATETIME_TODAY}'
FOLDER_DIR = f'{CURRENT_PATH}\\Files\\{DATETIME_TODAY}'
IMAGE_PATH = f'{CURRENT_PATH}\\images'