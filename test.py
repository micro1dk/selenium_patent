# import pyautogui
# import pyperclip

# pyautogui.moveTo(361, 203)
# pyautogui.dragTo(407, 229, 0.5 ,button='left')
# pyautogui.hotkey('ctrl', 'c') # 드래그된 내용 복사하기
# t = pyperclip.paste() # 클립보드에 저장된 데이터 할당하기

# a = '12345678'
# print(a[-2:])

import os
import shutil
from paths import *

# from datetime import datetime

# current_folder = f'{FOLDER_DIR}\\20210318_0065'

# target = r'\\Desktop-r4udot6\마크인포공유폴더\1.상표출원'

# today = datetime.now()

# month = '0' + str(today.month) if today.month < 10 else str(today.month)
# day = '0' + str(today.day) if today.day < 10 else str(today.day)

# # print(os.path.isdir(f'{target}\\{today.year}\\{today.year}.{month}'))

# month_path = f'{target}\\{today.year}\\{today.year}.{month}'
# day_path = f'{month_path}\\{today.year}{month}{day}'
# # year \\ year.month 폴더 생성
# if not os.path.isdir(month_path):
#     os.mkdir(month_path)

# if not os.path.isdir(day_path):
#     os.mkdir(day_path)

# shutil.copytree(current_folder, f'{day_path}\\20210318_0065')

# for f in os.listdir(PATENT_HISTORY_PATH):
#     if f.endswith('.zip'):
#         os.remove(f'{PATENT_HISTORY_PATH}\\{f}')

# a = ['aa', 'bb', 'cc']
# a.pop(1)
# print(a)

# aa = [
#     ('20210503_0073', 'a'),
#     ('20210503_0073', 'a'), 
#     ('20210503_0075', 'a'), 
#     ('20210503_0075', 'b'), 
#     ('20210503_0075', 'a'),
#     ('20210503_0080', 'b'),
#     ('20210503_0080', 'b'),
#     ('20210503_0080', 'a'),
#     ('20210503_0111', 'a'),
#     ('20210503_0111', 'a'),
#     ('20210503_0166', 'b'),

# ]

# wait_list = []
# remove_list = []
# complete_list = []

# for mode in range(1, 3):
#     if mode == 1:
#         for a, b in aa:
#             if b == 'a':
#                 if a not in remove_list and a not in wait_list:
#                     wait_list.append(a)
                
#             elif b == 'b':
#                 if a in wait_list:
#                     wait_list.remove(a)
#                     if a not in remove_list:
#                         remove_list.append(a)
#                 else:
#                     if a not in remove_list:
#                         remove_list.append(a)
#     elif mode == 2:
#         for a, b in aa:
#             if a in wait_list and a not in complete_list:
#                 print(a, b, '진행')
#                 complete_list.append(a)

# print(wait_list)
# print(remove_list)

# f = open('./testtxt.txt', 'r', encoding='utf-8')

# t_list = f.readlines()
# t_1 = t_list[0].strip('\n')
# t_2 = [t.strip('\n') for t in t_list[1:]]
# print(t_1, t_2)
# f = open('./testtxt.txt', 'r', encoding='utf-8')

# complete_list = []
# while True:
#     line = f.readline()
#     if not line:
#         break
#     complete_list.append(line.split('\n')[0])
# print(complete_list)

import os

print(os.path.isfile('./testtdxt.txt'))