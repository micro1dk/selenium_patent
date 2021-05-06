from classes.slack import Slack
from classes.handling_error import HandlingError
from classes.pyautogui_class import PyautoGUI
from paths import *
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class Keaps(PyautoGUI):
    def __init__(self):
        self.IMAGE_PATH = f'{CURRENT_PATH}\\images\\keaps'
        self.success = 0
        self.fail = 0
        self.folder_fail = 0

    def start_application(self, application_path):
        for f in os.listdir(PATENT_HISTORY_PATH):
            if f.endswith('.zip'):
                os.remove(f'{PATENT_HISTORY_PATH}\\{f}')

        os.system('taskkill /IM nkeaps* /F /T')
        time.sleep(1)
        os.startfile(application_path)
        print('start application')
        self.click_image([f'{self.IMAGE_PATH}\\start_01.PNG',
                         f'{self.IMAGE_PATH}\\start_02.PNG'], '없음', 0.5, 3, False)
        print('pass')

        time.sleep(1)
        self.click_image([f'{self.IMAGE_PATH}\\start_01.PNG',
                         f'{self.IMAGE_PATH}\\start_02.PNG'], '없음', 0.5, 1, False)
        time.sleep(3)

    def kill_application(self):
        os.system('taskkill /IM nkeaps* /F /T')

    def visit_folder(self):
        try:
            if not os.path.isdir(FOLDER_DIR):
                raise Exception('오늘날짜의 폴더가 생성이 되지 않았음')

            for f in os.listdir(FOLDER_DIR):
                if f == 'temp':
                    continue

                Slack.chat('서식상세', f'2. {f} 폴더 진행 (서식작성기)')
                if len(os.listdir(f'{FOLDER_DIR}\\{f}')) == 0:
                    Slack.chat('서식상세', f'└        {f}는 빈 폴더')
                    self.folder_fail += 1
                    continue

                # 파일검사: bib파일, jpg 파일 분류가 매치되어야함, warrant.pdf파일이 있어야함
                jpgs, bibs, pdf = 0, 0, 0
                for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
                    if d.endswith('.jpg'):
                        jpgs += 1
                    elif d.endswith('.BIB'):
                        bibs += 1
                    if d == 'warrant.pdf':
                        pdf += 1
                if jpgs != bibs:
                    Slack.chat('서식상세', f'└        jpg, bib 개수 매치가 안됨')
                    self.folder_fail += 1
                    continue
                if pdf != 1:
                    Slack.chat('서식상세', f'└        위임장pdf가 없음')
                    self.folder_fail += 1
                    continue
                print('성공')

                for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
                    if d.endswith('.BIB'):
                        classify = ''
                        for c in d:
                            if c.isnumeric():
                                classify += c
                        time.sleep(0.5)
                        self.classify = classify
                        self.start_one(f'{FOLDER_DIR}\\{f}',
                                       f'{FOLDER_DIR}\\{f}\\{d}', classify)
        except Exception as e:
            Slack.chat('서식상세', '-------------------')
            print(f'서식작성기과정에서 에러\n{e}')
            raise Exception(e)

    def extract_number(self, string):
        print('extract_number: ', string)
        ret = ''
        for s in string:
            if s.isnumeric():
                ret += s
            elif s == '-':
                ret += s
        print('extract 결과: ', ret)
        return ret

    def start_one(self, folder_path, application_path, classify):
        # print('===================')
        # print(classify, ' and ', folder_path)
        # print('===================')
        try:
            # 파일 실행 - 폴더별 순회 bib실행, 현재는 bib 하나일때만
            Slack.chat('서식상세', f'└        BIB_{classify}.BIB 실행')
            self.start_application(application_path)

            # 시작 대기
            self.wait_image_visible(f'{self.IMAGE_PATH}\\start_1.PNG', 1.5, 20)
            time.sleep(1)

            # 아래로 버튼
            e_cnt = 0
            while True:
                # self.click_position(x=1897, y=986, interval=0.7, clicks=4)
                self.click_position(x=1897, y=986)

                s, e = self.wait_image_visible(
                    f'{self.IMAGE_PATH}\\search_jpg.PNG', 0.2, 0.4)
                if s:
                    break
                e_cnt += 1
                if e_cnt >= 25:
                    raise Exception('bib 에러')

            # 첨부서류 입력 누르기 -> 첨부서류 정보 창 open
            self.click_image(
                [f'{self.IMAGE_PATH}\\document_1.PNG',
                    f'{self.IMAGE_PATH}\\document_2.PNG'],
                'wait element visible 에러: document_1, document_2.PNG와 일치하는 이미지가 없음 (첨부서류 입력 버튼)', 1, 15, True
            )

            # 첨부서류 정보 창에서 기타첨부서류로 이동
            time.sleep(1)
            self.press_key(['down'] * 18)

            # 첨부서류 정보에서 찾기버튼 클릭 -> 윈도우 open 다이얼로그 창
            self.click_image(
                f'{self.IMAGE_PATH}\\attachment_search.PNG',
                'wait element visible 에러: attachment_search.PNG와 일치하는 이미지가 없음 (돋보기 + 찾기 버튼)', 0.5, 5, True
            )

            # 윈도우 다이얼로그창에서 att를 PNG로 변경 후 파일경로 입력 후 엔터 후 기다려
            Slack.chat('서식상세', f'└        att 업로드')
            element_att = self.click_image(
                f'{self.IMAGE_PATH}\\attachment_att.PNG',
                'wait element visible 에러: attachment_att.PNG와 일치하는 이미지가 없음 (다이얼로그에서 확장자 바꾸는 칸)', 0.5, 3, True
            )
            self.press_key(['down', 'enter'])
            self.hot_key('alt', 'n')
            self.pyper_copy(f'{folder_path}\\warrant.pdf')
            self.hot_key('ctrl', 'v')
            self.press_key(['enter'])
            z = self.wait_image_invisible(
                [f'{self.IMAGE_PATH}\\attachment_open_1.PNG',
                    f'{self.IMAGE_PATH}\\attachment_open_2.PNG'],
                0.5, 3
            )

            self.click_image(
                [f'{self.IMAGE_PATH}\\start_01.PNG',
                    f'{self.IMAGE_PATH}\\start_02.PNG'],
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
            Slack.chat('서식상세', f'└        상표이미지입력')
            self.click_image(
                f'{self.IMAGE_PATH}\\search_jpg.PNG',
                'wait element visible 에러: search_jpg.PNG와 일치하는 이미지가 없음 (상표견본 찾기 버튼)', 0.5, 3, True
            )

            # 이미지 선택 창에서 파일찾기 버튼 클릭
            self.click_image(
                [f'{self.IMAGE_PATH}\\search_btn_1.PNG',
                    f'{self.IMAGE_PATH}\\search_btn_2.PNG'],
                'wait element visible 에러: search_btn.PNG와 일치하는 이미지가 없음 (상표견본찾기에서 파일 찾기버튼)', 0.5, 3, True
            )
            # 파일경로 입력 후 열기
            self.pyper_copy(f'{folder_path}\\logo_{classify}.jpg')
            self.hot_key('ctrl', 'v')
            self.press_key(['enter'])

            # 완료버튼 클릭
            self.click_image(
                f'{self.IMAGE_PATH}\\search_complete.PNG',
                'wait element visible 에러: search_complete.PNG와 일치하는 이미지가 없음 (핑크색 완료버튼)', 0.5, 3, True
            )

            cnt = 0
            while True:
                Slack.chat('서식상세', f'└        전자문서 제출 시작 {cnt + 1}회')
                # 전자문서 제출 클릭 후 YES
                self.click_image(
                    f'{self.IMAGE_PATH}\\document_submit.PNG',
                    'wait element visible 에러: document_submit.PNG와 일치하는 이미지가 없음 (전자문서제출 버튼)', 0.5, 2, True
                )
                self.click_image(
                    f'{self.IMAGE_PATH}\\document_create_yes.PNG',
                    'wait element visible 에러: document_create_yes.PNG와 일치하는 이미지가 없음 (위임장 정보 다이얼로그 > 예 버튼)', 0.5, 3, True
                )

                # 온라인제출 마법사 에서 제출문서 생성 클릭 후 YES
                self.click_image(
                    f'{self.IMAGE_PATH}\\document_create.PNG',
                    'wait element visible 에러: document_create.PNG와 일치하는 이미지가 없음 (온라인제출 마법사 창에서 제출문서 생성 버튼)', 0.5, 3, True
                )
                self.click_image(
                    f'{self.IMAGE_PATH}\\document_create_yes.PNG',
                    'wait element visible 에러: document_create_yes.PNG와 일치하는 이미지가 없음 (제출문서 다이얼로그 > 예 버튼)', 0.5, 3, True
                )

                # 일치하면 서지사항으로 간 뒤 인쇄창 띄우고 pdf 저장하기
                self.click_image(
                    f'{self.IMAGE_PATH}\\viewer_this.PNG',
                    'wait element visible 에러: viewer_this.PNG와 일치하는 이미지가 없음 (서지사항)', 0.5, 3, True
                )
                self.hot_key('ctrl', 'p')
                if cnt == 0:  # 첫 실패 후 두 번째부터는 저장할 필요가 없음
                    # 프린터 선택하기
                    self.click_image(
                        f'{self.IMAGE_PATH}\\viewer_print_select.PNG',
                        'wait element visible 에러: viewer_print_select.PNG와 일치하는 이미지가 없음 (인쇄 창에서 셀렉트박스)', 0.5, 3, True
                    )
                    time.sleep(0.5)
                    self.click_image(
                        [f'{self.IMAGE_PATH}\\viewer_pdf_selected_1.PNG',
                            f'{self.IMAGE_PATH}\\viewer_pdf_selected_2.PNG'],
                        'wait element visible 에러: viewer_pdf_selected.PNG와 일치하는 이미지가 없음 (마이크로소프트 pdf 가 없음)', 0.5, 3, True
                    )

                    # 인쇄확인
                    self.click_image(
                        f'{self.IMAGE_PATH}\\viewer_print.PNG',
                        'wait element visible 에러: viewer_print.PNG와 일치하는 이미지가 없음 (인쇄 확인버튼)', 0.5, 3, True
                    )
                    Slack.chat('서식상세', f'└        1-{classify}.pdf 저장')
                    self.hot_key('alt', 'n')  # 파일이름 선택
                    self.pyper_copy(f'{folder_path}\\1-{classify}.pdf')
                    self.hot_key('ctrl', 'v')
                    self.press_key(['enter'])

                # 통합뷰어 닫기
                self.click_image(
                    f'{self.IMAGE_PATH}\\viewer_close_1.PNG',
                    'wait element visible 에러: viewer_close_1.PNG와 일치하는 이미지가 없음 (왼쪽 상단 버튼)', 0.5, 3, True
                )
                self.click_image(
                    [f'{self.IMAGE_PATH}\\viewer_close_2.PNG',
                        f'{self.IMAGE_PATH}\\viewer_close_2_1.PNG', ],
                    'wait element visible 에러: viewer_close_2.PNG와 일치하는 이미지가 없음 (왼쪽 상단 버튼 누른 뒤 닫기버튼)', 0.5, 3, True
                )

                # 공인인증서 로그인
                # 실제 제출진행
                self.click_image(  # 서명클릭
                    f'{self.IMAGE_PATH}\\final_submit_1.png',
                    'wait element visible 에러: final_submit_1.PNG 이미지 없음. 서명버튼', 0.8, 4.0, True)
                self.click_image(
                    [f'{self.IMAGE_PATH}\\final_submit_name_1.PNG',
                        f'{self.IMAGE_PATH}\\final_submit_name_2.PNG'],
                    'wait element visible 에러: final_submit_name_1,2.PNG 이미지 없음. 구공호', 0.3, 2, True)
                self.press_key(['tab', 'tab', 'tab'])
                self.write_key('akzmdlsvh2015!!')
                self.click_image(
                    f'{self.IMAGE_PATH}\\final_submit_login_btn.PNG',
                    'wait element visible 에러: final_submit_login_btn.PNG 확인버튼', 0.3, 2, True)
                time.sleep(0.7)
                self.click_image(
                    f'{self.IMAGE_PATH}\\final_submit_name_3.PNG',
                    'wait element visible 에러: final_submit_name_3.PNG 구공호버튼', 0.3, 2, True)
                self.click_image(
                    f'{self.IMAGE_PATH}\\final_submit_next_btn.PNG',  # 다음단계
                    'wait element visible 에러: final_submit_next_btn.PNG 에러 다음단계 버튼', 0.5, 4, True)
                time.sleep(0.7)
                self.move_mouse_pos(1987, 986)
                self.click_image(
                    f'{self.IMAGE_PATH}\\final_submit_next_btn_2.PNG',  # 다음단계
                    'wait element visible 에러: final_submit_next_btn_2.PNG 에러 다음단계 버튼', 0.5, 4, True)
                time.sleep(0.5)

                self.click_image(
                    f'{self.IMAGE_PATH}\\final_submit_final_btn.PNG',  # 온라인제출
                    'wait element visible 에러: final_submit_next_btn.PNG 에러', 0.5, 4, True)

                # 예 버튼 최종제출
                self.click_image(
                    f'{self.IMAGE_PATH}\\document_create_yes.PNG',
                    'wait element visible 에러: document_create_yes.PNG와 일치하는 이미지가 없음 (최종제출 > 예)', 0.5, 4, True
                )

                time.sleep(7)

                # 온라인제출 안내 뜰 때까지 대기
                success, elmt = self.wait_image_visible(
                    f'{self.IMAGE_PATH}\\final_submit_online_text.PNG', 1, 25)

                
                self.click_image(f'{self.IMAGE_PATH}\\final_submit_search_file.PNG',
                                 'wait element visible 에러: 온라인제출 > 파일찾기 버튼 에러', 0.4, 8, True)
                self.pyper_copy(f'{PATENT_HISTORY_PATH}\\bib_{classify}.zip')
                self.hot_key('ctrl', 'v')
                self.press_key(['enter'])
                self.click_image(f'{self.IMAGE_PATH}\\final_submit_search_submit.PNG',
                                'wait element visible 에러: 온라인제출 > 최종제출 버튼 에러',  0.4, 8, True)
                # # 예 버튼 최종제출
                # self.click_image(
                #     f'{self.IMAGE_PATH}\\document_create_yes.PNG',
                #     'wait element visible 에러: document_create_yes.PNG와 일치하는 이미지가 없음 (최종제출 > 예)', 0.5, 4, True
                # )

                time.sleep(3)
                # 제출결과 안내 뜰 때까지 대기?
                success, elmt = self.wait_image_visible(
                    f'{self.IMAGE_PATH}\\final_result_text.PNG',
                    0.5, 25
                )

                accept_no = self.extract_number(
                    self.drag_mouse_and_paste(566, 755, 691, 755, 0.7))
                application_no = self.extract_number(
                    self.drag_mouse_and_paste(712, 737, 852, 760, 0.7))
                success = self.drag_mouse_and_paste(1292, 755, 1350, 755, 0.7)
                # 접수번호 끝이 XX이거나, 출원번호가 없는 경우 Err
                # 있는경우면 출원번호 가공
                print(accept_no, '접수번호')
                print(application_no, '출원번호')
                print(success, '성공여부')
                if accept_no[-2:] != 'XX' and application_no != '' and '접수완료' in success:
                    Slack.chat(
                        '서식상세', f'└        _codes.txt 생성 {accept_no}, {application_no}, {classify}')

                    # 접수완료
                    f = open(f'{folder_path}\\_codes.txt',
                             'a', encoding='utf-8')
                    f.write(f'{accept_no},{application_no},{classify}\n')
                    f.close()
                    break
                else:
                    # 실패 -> 닫기
                    Slack.chat('서식상세', f'└        출원실패! 다시')
                    self.click_position(1381, 262, 1, 1)
                    cnt += 1

                # 실패 3번실패시 에러띄우고 다음 폴더로 넘어가기.
                if cnt == 3:
                    raise Exception(f'3번 연속 실패')
            self.success += 1
            self.kill_application()
        except Exception as e:
            Slack.chat('서식상세', f'└        {classify}류에서 에러\n{e}')
            self.kill_application()
            self.fail += 1
            raise Exception(f'{application_path} {classify}류에서 에러\n{e}')


def main():
    try:
        Slack.chat(
            '서식상세', '=====================< 서식작성기 시작 >=====================')
        Slack.chat('서식', '서식작성기 작업 시작')
        keaps = Keaps()
        keaps.visit_folder()
        total = keaps.success + keaps.fail
        Slack.chat('서식',
                   f'''
                서식작성기 완료 , 합: {total} , 성공: {keaps.success} , 실패: {keaps.fail} , 폴더방문실패: {keaps.folder_fail}
            '''
                   )
    except Exception as e:
        Slack.chat('서식', f'서식작성기 에러')
        raise Exception(e)
