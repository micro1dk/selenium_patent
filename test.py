import os
import sys
import time
import shutil
import re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import requests

from paths import *
from classes.selenium_class import Browser
from classes.pyautogui_class import PyautoGUI
from classes.slack import Slack

def explorer_folder(markinfo_acc_no):
    """
    공유폴더 탐색
    """
    classify_list = []
    if os.path.isdir(f'{TARGET_DAY}\\{markinfo_acc_no}'):
        if os.path.isfile(f'{TARGET_DAY}\\{markinfo_acc_no}\\_codes.txt'):
            f = open(f'{TARGET_DAY}\\{markinfo_acc_no}\\_codes.txt', 'r', encoding='utf-8')
            fl = f.readlines()[1:]
            for line in fl:
                classify = int(line.strip('\n').split(',')[-1])
                classify_list.append(classify)
            return True, classify_list
    return False, None


# pass_list = [11, 77]
# exist_classifies, classifies = explorer_folder('TEST_1234')
# if exist_classifies:
#     pass_list.extend(classifies)
# print(pass_list)

# a = 'BIB_35.BIB'
# t = re.search('\d+', a)[0]
# print(t)

# pdfs_1, pdfs_2 = 0, 0
# work_list = []
# for d in os.listdir(f'{FOLDER_DIR}\\202202'):
#     if d.startswith('1-'):
#         classify_1 = re.search('\d-(\d+)', d)[1]
#         if '2-' + classify_1 + '.pdf' in os.listdir(f'{FOLDER_DIR}\\202202'):
#             work_list.append(classify_1)
# print(work_list)

ff = open(f'testtxt.txt', 'r+', encoding='utf-8')
lines = ff.readlines()

# tl, tr = lines[0].strip('\n').split(',')
print(lines[0].strip('\n').split(','))