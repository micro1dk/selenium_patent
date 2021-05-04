from datetime import datetime, timedelta, date

today = datetime.now()

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


TARGET_PATH = r'\\Desktop-r4udot6\마크인포공유폴더\1.상표출원'

month = '0' + str(today.month) if today.month < 10 else str(today.month)
day = '0' + str(today.day) if today.day < 10 else str(today.day)

TARGET_MONTH = f'{TARGET_PATH}\\{today.year}\\{today.year}.{month}'
TARGET_DAY = f'{TARGET_MONTH}\\{today.year}{month}{day}'