import os
import sys
import time
import shutil
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from paths import *
from classes.selenium_class import Browser
from classes.pyautogui_class import PyautoGUI
from classes.slack import Slack

class UploadFiles(Browser, PyautoGUI):
    def __init__(self, driver):
        self.driver = driver
        self.success = 0
        self.fail = 0
        self.complete_list = []
        self.folder_fail = 0
        self.result_list = [] # slack 결과안내
    
    def open_codes(self, f):
        try:
            txt_file = open(f'{FOLDER_DIR}\\{f}\\_codes.txt', 'r', encoding='utf-8')
            txt_list = txt_file.readlines()
            return [t.strip('\n') for t in txt_list[1:]]
        except Exception as e:
            return []
        
    
    def visit_folder(self):
        """
        폴더하나하나 순회
        """
        try:
            self.visit('https://markinfo.co.kr/front/nanmin/phtml/list.php?code=doc&link_page=reply')
            # 매니저 전체 선택
            self.driver.find_element_by_xpath(
                '//*[@id="selected_manager_name"]').click()
            ul_select = self.driver.find_element_by_xpath(
                '//*[@id="form"]/div[1]/div[1]/div/div[4]/div/ul')
            li_select = ul_select.find_elements_by_tag_name('li')
            li_select[len(li_select) - 1].click()
            # self.driver.find_element_by_xpath('//*[@id="search"]').click()
            # 위까지 테스트
            if not os.path.isdir(FOLDER_DIR):
                raise Exception('오늘날짜의 폴더가 생성이 되지 않았음')

            for f in os.listdir(FOLDER_DIR):
                if f == 'temp':
                    continue
                
                Slack.chat('서식상세', f'4. {f} 폴더 진행 (관리자페이지 파일업로드)')
                if len(os.listdir(f'{FOLDER_DIR}\\{f}')) == 0:
                    Slack.chat('서식상세', f'└        {f}는 빈 폴더')
                    self.folder_fail += 1
                    continue

                pdfs_1, pdfs_2 = 0, 0
                for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
                    if d.startswith('1-'):
                        pdfs_1 += 1
                    elif d.startswith('2-'):
                        pdfs_2 += 1

                if pdfs_1 != pdfs_2:
                    Slack.chat('서식상세', f'└        1-.pdf, 2-.pdf 개수 매치가 안됨')
                    self.folder_fail += 1
                    continue

                complete_list = self.open_codes(f)
                complete_length = len(complete_list)
                if not complete_list:
                    Slack.chat('서식상세', f'└        _codes.txt가 없거나 빈 파일')
                    self.folder_fail += 1
                    continue
                
                complete_cnt = 0
                complete = False
                for com in complete_list:
                    accept_no, application_no, classify_no = com.split(',')
                    # print('page_search _before')
                    Slack.chat('서식상세', f'admin 페이지 {f} {classify_no}류 시작')
                    # 한줄마다 페이지 전체를 순회하여 검색
                    if complete_cnt == complete_length - 1:
                        complete = True # 마지막 항목일 때 True
                    self.page_search(accept_no, application_no, classify_no, f, complete)
                    complete_cnt += 1

                    print('complete!')
                self.result_list = []
        except Exception as e:
            print(f'visit_folder 에러{e}')
            raise Exception(e)

    def page_search(self, accept_no, application_no, classify_no, markinfo_acc_no, complete):
        print(f'{accept_no}, {application_no}, {classify_no}, {markinfo_acc_no}를 탐색한다.')
        self.driver.find_element_by_xpath('//*[@id="search"]').click()
        time.sleep(3)
        page = 1
        pagination = self.driver.find_element_by_xpath(
            '//*[@id="form"]/div[4]/div/div/ul')
        pagination_elem = pagination.find_elements_by_tag_name('li')
        page_count = len(pagination_elem) - 4

        i = 3
        while True:
            if i > 3:
                self.driver.find_element_by_xpath(
                    f'//*[@id="form"]/div[4]/div/div/ul/li[{i}]/a').click()

            # 폴더 순회 -> number 검색 -> 관리자페이지 리스트 순회
            tbody = self.driver.find_element_by_xpath('//*[@id="table-view"]/tbody')
            number_tr = len(tbody.find_elements_by_tag_name('tr'))

            for j in range(1, number_tr + 1):
                if self.driver.find_element_by_xpath(f'//*[@id="table-view"]/tbody/tr[{j}]').get_attribute('class') != 'template':
                    continue
                title_elem = self.driver.find_element_by_xpath(
                    f'//*[@id="table-view"]/tbody/tr[{j}]/td[5]')  # 요기안에 제목 들어있음
                reply_elem = self.driver.find_element_by_xpath(
                    f'//*[@id="table-view"]/tbody/tr[{j}]/td[6]')  # 회신사항
                state_elem = self.driver.find_element_by_xpath(
                    f'//*[@id="table-view"]/tbody/tr[{j}]/td[7]')  # 회신사항

                # print(markinfo_acc_no, title_elem.text)
                if '최종제출동의' == reply_elem.text and '처리대기' in state_elem.text and markinfo_acc_no in title_elem.text and f'({classify_no}류)' in title_elem.text:
                    # print('발견!!!=====================')
                    time.sleep(2)
                    self.click('xpath', f'//*[@id="table-view"]/tbody/tr[{j}]/td[5]/div[3]/span/a')
                    self.switch_windows(2)
                    success = self.detail_page(accept_no, application_no, classify_no, markinfo_acc_no, complete)
                    print('페이지 닫기 성공여부: ', success)

                    self.switch_windows(1)
                    time.sleep(1)
                    # print('ok 상세페이지 업로드 성공?', success)

                    if success:
                        print('처리대기 전')
                        self.click('xpath', f'//*[@id="table-view"]/tbody/tr[{j}]/td[7]/div/div/a') # 처리대기 클릭
                        print('처리대기 누름, 처리완료 누르기 전')
                        self.click('xpath', f'//*[@id="table-view"]/tbody/tr[{j}]/td[7]/div/div/ul/li[4]/a') # 처리완료 클릭
                        print('처리대기 처리완료 누름')
                        Slack.chat('서식상세', f'└        상태값 처리완료로')

                    time.sleep(3)
                    if i > 3:
                        self.driver.find_element_by_xpath(
                            '//*[@id="form"]/div[4]/div/div/ul/li[1]/a').click()
                    return

            if i == 12:
                success, attr = self.check_attribute(
                    f'//*[@id="form"]/div[4]/div/div/ul/li[{i + 1}]/a', 'disabled')
                if success:
                    if attr != 'disabled':
                        self.driver.find_element_by_xpath(
                            f'//*[@id="form"]/div[4]/div/div/ul/li[{i + 1}]/a').click()
                        pagination = self.driver.find_element_by_xpath(
                            '//*[@id="form"]/div[4]/div/div/ul')
                        pagination_elem = pagination.find_elements_by_tag_name(
                            'li')
                        page_count = len(pagination_elem) - 4
                        i = 3
                        continue
            if i == page_count + 2:
                break
            i += 1
        # self.driver.find_element_by_xpath('//*[@id="search"]').click()
    
    def detail_page(self, accept_no, application_no, classify_no, markinfo_acc_no, complete):
        try:
            bib_classifies = self.driver.find_elements_by_class_name(
                'classify_bib')
            number_inputs = self.driver.find_elements_by_class_name(
                'application_number')
            edit_btns = self.driver.find_elements_by_class_name(
                'application_edit')
            
            for i in range(len(bib_classifies)):
                """
                분류번호가 맞는 것
                """
                # print(bib_classifies[i].text, classify_no, application_no)
                if bib_classifies[i].get_attribute('value') == classify_no:
                    Slack.chat('서식상세', f'└        {classify_no}류에 출원번호는 {application_no}')
                    number_inputs[i].send_keys(application_no)
                    time.sleep(1)
                    self.write_key(application_no)
                    Slack.chat('서식상세', f'└         1-{classify_no}.pdf, 2-{classify_no}.pdf 업로드')
                    edit_btns[i].click()
                    alert = self.wait_alert()
                    self.accept_alert(alert)
                    alert = self.wait_alert()
                    self.accept_alert(alert)

                    time.sleep(1)
                    self.driver.refresh()
                    submit_btns = self.driver.find_elements_by_class_name(
                        'btn_add_file')
                    upload_btns = self.driver.find_elements_by_class_name(
                        'pdf_upload_btn'
                    )

                    inputs = self.driver.find_elements_by_class_name('input_imgs')             
                    submit_btns[i].click()
                    inputs[i].send_keys(
                        f'{FOLDER_DIR}\\{markinfo_acc_no}\\1-{classify_no}.pdf')
                    inputs[i].send_keys(
                        f'{FOLDER_DIR}\\{markinfo_acc_no}\\2-{classify_no}.pdf')
                    # 확인 필요
                    upload_btns[i].click()
                    alert = self.wait_alert()
                    self.accept_alert(alert)
                    self.click('xpath', '/html/body/div[8]/div[7]/button[2]')
                    time.sleep(1)
                    print('리프레시중')
                    self.driver.refresh()
                    print('리프레시완료')
                    time.sleep(1)

                    # 메일 보내기: 마지막 항목인 경우 보냄
                    if complete:
                        print('현재가 마지막 파일..')
                        # 폴더 복사
                        if not os.path.isdir(TARGET_MONTH):
                            os.mkdir(TARGET_MONTH)

                        if not os.path.isdir(TARGET_DAY):
                            os.mkdir(TARGET_DAY)

                        shutil.copytree(f'{FOLDER_DIR}\\{markinfo_acc_no}', f'{TARGET_DAY}\\{markinfo_acc_no}')

                        time.sleep(1)
                        elnt = self.driver.find_element_by_xpath('//*[@id="result_report"]/span')
 
                        if '출원컨펌요청' in elnt.text:
                            raise Exception('출원컨펌요청이네요')
                        elnt.click()
                        
                        self.wait_new_window(3, 0.5)
                        self.switch_windows(3)
                        self.click('xpath', '/html/body/div[1]/div[2]/div[1]/div/button[1]')
                        time.sleep(0.4)
                        alert = self.wait_alert()
                        self.accept_alert(alert); time.sleep(0.5)
                        alert = self.wait_alert()
                        self.accept_alert(alert); time.sleep(0.5)

                        self.switch_windows(2)
                        self.result_list.append(classify_no)
                        t = '류, '.join(self.result_list) + '류' if len(self.result_list) > 0 else ''
                        Slack.chat('서식', f'{markinfo_acc_no} {t} 완료!')
                        Slack.chat('서식상세', f'└         메일 & 알림톡 전송 (끝)')
                    else:
                        print('switch 전')
                        self.switch_windows(2)
                        print('switch 후')
                        self.result_list.append(classify_no)
                    print('한페이지 종료')
                    self.driver.close()
                    print('페이지 닫기')
                    self.success += 1
                    return True
            return False
        except Exception as e:
            Slack.chat('서식', f'{markinfo_acc_no} {classify_no}류 에러!\n{e}')
            self.fail += 1
            print(f'출원번호 입력 과정에서 에러\n{e}')
            return False

def main(driver):
    try:
        Slack.chat('서식상세', '=====================< 파일 업로드 시작 >=====================')
        Slack.chat('서식', 'pdf 업로드 / 출원번호 저장 / 출원완료메일 작업 시작')
        upload_files = UploadFiles(driver)
        upload_files.visit_folder()
        total = upload_files.success + upload_files.fail
        Slack.chat('서식', 
            f'''
                업로드 완료, 합: {total}, 성공: {upload_files.success}, 실패: {upload_files.fail}, 폴더방문실패: {upload_files.folder_fail}
            '''
        )
        
    except Exception as e:
        print('업로드 본체에러', e)
        Slack.chat('서식', f'마크인포 관리자페이지 탐색중 에러')
        raise Exception(e)