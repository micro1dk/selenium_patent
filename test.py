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

# import os

# print(os.path.isfile('./testtdxt.txt'))

# import re
# reg_name = '(.*)\(\d'

# target = '주식회사 기지개핌(z1-2021-034521-6)'
# match = re.search(reg_name, target)

# print(match)
# # print(match.group(1))

# def open_codes():
#     try:
#         txt_file = open(f'testtxt.txt', 'r', encoding='utf-8')
#         txt_list = txt_file.readlines()
#         return [t.strip('\n') for t in txt_list[1:]]
#     except Exception as e:
#         return []

# complete_list = open_codes()
# complete_length = len(complete_list)

# complete_cnt = 0
# for com in complete_list:
#     accept_no, application_no, classify_no = com.split(',')
#     # print('page_search _before')
#     # 한줄마다 페이지 전체를 순회하여 검색
#     print(com)
#     if complete_cnt == complete_length - 1:
#         complete = True # 마지막 항목일 때 True
#         print('마지막 시작')
#     complete_cnt += 1

#
#  test_list = [
#     ('11', '컨펌요청'),
#     ('src', 'temp'),
#     ('02', '출원완료'),
#     ('src', ''),
#     ('05', '출원완료'),
#     ('src', ''),
#     ('66', '컨펌요청'),
#     ('src', ''),
# ]

# pass_list = []

# temp = ''
# for i in range(len(test_list)):
#     if i % 2 == 0:
#         classify = test_list[i][0]
#         temp = classify
#         state = test_list[i][1]
#         if state != '컨펌요청':
#             pass_list.append(classify)
#     else:
#         if temp not in pass_list:
#             print(temp)

# print(pass_list)

# test = ['22', '11']
# tt = '류' if len(test) > 0 else ''
# t = '류, '.join(test) + '류' if len(test) > 0 else ''

# print(t)

# import requests

# TOKEN = "xoxb-2001561769222-2046544931922-cgbq5QHml1M6RDdLPZ6IlSxe"

# class Slack:
#     @staticmethod
#     def chat(channel, message):
#         response = requests.post("https://slack.com/api/chat.postMessage",
#             headers={"Authorization": "Bearer "+ TOKEN},
#             data={"channel": channel,"text": message}
#         )
#         # print(response.__dict__)
 
# Slack.chat('#서식', 'test')

import os

p = os.path.isfile('./index.py')
print(p)