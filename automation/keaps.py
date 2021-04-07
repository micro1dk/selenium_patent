import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from classes.pyautogui_class import PyautoGUI

from paths import *

class Keaps(PyautoGUI):
  def __init__(self):
    self.IMAGE_PATH = f'{CURRENT_PATH}\\images\\keaps'

  def start_application(self, application_path):
    os.system('taskkill /IM nkeaps* /F /T')
    time.sleep(1)
    os.startfile(application_path)

    self.click_image([f'{self.IMAGE_PATH}\\start_01.PNG', f'{self.IMAGE_PATH}\\start_02.PNG'], '없음', 0.5, 3, False)
    time.sleep(1)
    self.click_image([f'{self.IMAGE_PATH}\\start_01.PNG', f'{self.IMAGE_PATH}\\start_02.PNG'], '없음', 0.5, 1, False)
    time.sleep(3)

  def kill_application(self):
    os.system('taskkill /IM nkeaps* /F /T')
  
  def script_keaps(self):
    try:
      if not os.path.isdir(FOLDER_DIR):
        raise Exception('오늘날짜의 폴더가 생성이 되지 않았음')
      
      for f in os.listdir(FOLDER_DIR):
        if f == 'temp': continue
        if len(os.listdir(f'{FOLDER_DIR}\\{f}')) == 0: 
          print(f'{f}는 비었음') # slack api
          continue
        print(f)
        # 파일검사: bib파일, jpg 파일 분류가 매치되어야함, warrant.pdf파일이 있어야함
        jpgs, bibs, pdf = 0, 0, 0
        for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
          if d.endswith('.jpg'): jpgs += 1
          elif d.endswith('.BIB'): bibs += 1
          if d == 'warrant.pdf': pdf += 1
        if jpgs != bibs:
          print('jpg, bib 매치가 안됨')
          continue
        if pdf != 1:
          print('위임장 pdf가 없음')
          continue
        print('성공')

        for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
          if d.endswith('.BIB'):
            classify = ''
            for c in d:
              if c.isnumeric():
                classify += c
            time.sleep(0.5)
            self.start_one(f'{FOLDER_DIR}\\{f}', f'{FOLDER_DIR}\\{f}\\{d}', classify)

    except Exception as e:
      print(f'서식작성기과정에서 에러\n{e}')
  
          
  def start_one(self, folder_path, application_path, classify):
    print('===================')
    print(classify, ' and ' , folder_path)
    print('===================')
    try:
      # 파일 실행 - 폴더별 순회 bib실행, 현재는 bib 하나일때만
      self.start_application(application_path)
      
      # 시작 대기
      self.wait_image_visible(f'{self.IMAGE_PATH}\\start_1.PNG', 1.5, 20)
      time.sleep(1)

      # # 아래로 버튼
      while True:
        self.click_position(x=1897, y=986, interval=0.5, clicks=3)
        # 첨부서류 입력 누르기 -> 첨부서류 정보 창 open
        elem = self.click_image(
          [f'{self.IMAGE_PATH}\\document_1.PNG', f'{self.IMAGE_PATH}\\document_2.PNG'],
          'wait element visible 에러: document_1, document_2.PNG와 일치하는 이미지가 없음 (첨부서류 입력 버튼)', 1, 15, True
        )
        if elem: break
      
      # 첨부서류 정보 창에서 기타첨부서류로 이동
      time.sleep(1)
      self.press(['down'] * 18)
      
      # 첨부서류 정보에서 찾기버튼 클릭 -> 윈도우 open 다이얼로그 창
      self.click_image(
        f'{self.IMAGE_PATH}\\attachment_search.PNG',
        'wait element visible 에러: attachment_search.PNG와 일치하는 이미지가 없음 (돋보기 + 찾기 버튼)', 0.5, 5, True
      )
      
      # 윈도우 다이얼로그창에서 att를 PNG로 변경 후 파일경로 입력 후 엔터 후 기다려
      element_att = self.click_image(
        f'{self.IMAGE_PATH}\\attachment_att.PNG',
        'wait element visible 에러: attachment_att.PNG와 일치하는 이미지가 없음 (다이얼로그에서 확장자 바꾸는 칸)', 0.5, 3, True
      )
      self.press(['down', 'enter'])
      self.hotkey('alt', 'n')
      self.pyper_copy(f'{folder_path}\\warrant.pdf')
      self.hotkey('ctrl', 'v')
      self.press(['enter'])
      z = self.wait_image_invisible(
        [f'{self.IMAGE_PATH}\\attachment_open_1.PNG', f'{self.IMAGE_PATH}\\attachment_open_2.PNG'],
        0.5, 3
      )
      print(z)

      self.click_image(
        [f'{self.IMAGE_PATH}\\start_01.PNG', f'{self.IMAGE_PATH}\\start_02.PNG'],
        'wait element visible 에러: start_01.PNG와 일치하는 이미지가 없음 (확인버튼)', 0.5, 1, True
      )

      # 입력 클릭
      self.click_image(
        f'{self.IMAGE_PATH}\\attachment_write.PNG',
        'wait element visible 에러: attachment_write.PNG와 일치하는 이미지가 없음 (입력 버튼)', 0.5, 3, True
      )
      
      # 첨부서류 정보 닫기 클릭
      self.click_image(
        f'{self.IMAGE_PATH}\\attachment_close.PNG',
        'wait element visible 에러: attachment_close.PNG와 일치하는 이미지가 없음 (나가기 + 닫기 버튼)', 0.5, 3, True
      )
      
      # 상표 견본 찾기 버튼 클릭 -> 이미지 선택 창
      self.click_image(
        f'{self.IMAGE_PATH}\\search_jpg.PNG',
        'wait element visible 에러: search_jpg.PNG와 일치하는 이미지가 없음 (상표견본 찾기 버튼)', 0.5, 3, True
      )
      
      # 이미지 선택 창에서 파일찾기 버튼 클릭
      self.click_image(
        [f'{self.IMAGE_PATH}\\search_btn_1.PNG', f'{self.IMAGE_PATH}\\search_btn_2.PNG'],
        'wait element visible 에러: search_btn.PNG와 일치하는 이미지가 없음 (상표견본찾기에서 파일 찾기버튼)', 0.5, 3, True
      )
      # 파일경로 입력 후 열기
      self.pyper_copy(f'{folder_path}\\logo_{classify}.jpg')
      self.hotkey('ctrl', 'v')
      self.press(['enter'])

      # 완료버튼 클릭
      self.click_image(
        f'{self.IMAGE_PATH}\\search_complete.PNG',
        'wait element visible 에러: search_complete.PNG와 일치하는 이미지가 없음 (핑크색 완료버튼)', 0.5, 3, True
      )

      # 전자문서 제출 클릭 후 YES
      self.click_image(
        f'{self.IMAGE_PATH}\\document_submit.PNG',
        'wait element visible 에러: document_submit.PNG와 일치하는 이미지가 없음 (전자문서제출 버튼)', 0.5, 2, True
      )
      self.click_image(
        f'{self.IMAGE_PATH}\\document_create_yes.PNG',
        'wait element visible 에러: document_create_yes.PNG와 일치하는 이미지가 없음 (위임장 정보 다이얼로그 > 예 버튼)', 0.5, 3, True
      )

      # # 온라인제출 마법사 에서 제출문서 생성 클릭 후 YES
      self.click_image(
        f'{self.IMAGE_PATH}\\document_create.PNG',
        'wait element visible 에러: document_create.PNG와 일치하는 이미지가 없음 (온라인제출 마법사 창에서 제출문서 생성 버튼)', 0.5, 3, True
      )
      self.click_image(
        f'{self.IMAGE_PATH}\\document_create_yes.PNG',
        'wait element visible 에러: document_create_yes.PNG와 일치하는 이미지가 없음 (제출문서 다이얼로그 > 예 버튼)', 0.5, 3, True
      )

      # 통합뷰어에서 상표견본 클릭
      # self.click_image(
      #   f'{self.IMAGE_PATH}\\viewer_image_check.PNG',
      #   'wait element visible 에러: document_create_yes.PNG와 일치하는 이미지가 없음 (제출문서 다이얼로그 > 예 버튼)', 0.5, 3, True
      # )
      # time.sleep(0.5)
      # print('견본이미지와 일치?')
      
      # # 견본이미지와 일치하는지?
      # self.doubleClick(x=574, y=290)
      # time.sleep(0.5)
      # # mark_image = self.locateOnScreen(f'{self.IMAGE_PATH}\\ttt.jpg') # 테스트용 일치하지 않는 이미지
      # mark_image = self.locateOnScreen(f'{folder_path}\\logo_{classify}.jpg')
      # if not mark_image:
      #   raise Exception('상표견본 이미지와 일치하지 않음')
      # self.hotkey('alt', 'f4')
      
      # 일치하면 서지사항으로 간 뒤 인쇄창 띄우고 pdf 저장하기
      self.click_image(
        f'{self.IMAGE_PATH}\\viewer_this.PNG',
        'wait element visible 에러: viewer_this.PNG와 일치하는 이미지가 없음 (서지사항)', 0.5, 3, True
      )
      self.hotkey('ctrl', 'p')

      # 프린터 선택하기
      self.click_image(
        f'{self.IMAGE_PATH}\\viewer_print_select.PNG',
        'wait element visible 에러: viewer_print_select.PNG와 일치하는 이미지가 없음 (인쇄 창에서 셀렉트박스)', 0.5, 3, True
      )
      time.sleep(0.5)
      self.click_image(
        [f'{self.IMAGE_PATH}\\viewer_pdf_selected_1.PNG', f'{self.IMAGE_PATH}\\viewer_pdf_selected_2.PNG'],
        'wait element visible 에러: viewer_pdf_selected.PNG와 일치하는 이미지가 없음 (마이크로소프트 pdf 가 없음)', 0.5, 3, True
      )
      
      # 인쇄확인
      self.click_image(
        f'{self.IMAGE_PATH}\\viewer_print.PNG',
        'wait element visible 에러: viewer_print.PNG와 일치하는 이미지가 없음 (인쇄 확인버튼)', 0.5, 3, True
      )

      self.hotkey('alt', 'n') # 파일이름 선택
      self.pyper_copy(f'{folder_path}\\1-{classify}.pdf')
      self.hotkey('ctrl', 'v')
      self.press(['enter'])

      # 통합뷰어 닫기
      self.click_image(
        f'{self.IMAGE_PATH}\\viewer_close_1.PNG',
        'wait element visible 에러: viewer_close_1.PNG와 일치하는 이미지가 없음 (왼쪽 상단 버튼)', 0.5, 3, True
      )
      self.click_image(
        f'{self.IMAGE_PATH}\\viewer_close_2.PNG',
        'wait element visible 에러: viewer_close_2.PNG와 일치하는 이미지가 없음 (왼쪽 상단 버튼 누른 뒤 닫기버튼)', 0.5, 3, True
      )

      # self.kill_application()
      # print('끝')
    except Exception as e:
      # raise Exception(f'{classify}에서 에러\n{e}')
      print(f'{classify}에서 에러\n{e}')
      self.kill_application()

def main():
  keaps = Keaps()
  keaps.script_keaps()