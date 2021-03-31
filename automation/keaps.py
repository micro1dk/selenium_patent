import os
import sys
import time
import json
import pickle
import shutil
import getpass
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from classes.pyautogui_class import PyautoGUI

class Keaps(PyautoGUI):
  def __init__(self):
    self.K_IMG_PAHT = f'{IMAGE_PATH}\\keaps'

  def start_application(self, application_path):
    os.system('taskkill /IM nkeaps* /F /T')
    time.sleep(1)
    os.startfile(application_path)

    self.click_image([f'{self.K_IMG_PAHT}\\start_01.PNG', f'{self.K_IMG_PAHT}\\start_02.PNG'], '없음', 0.5, 3, False)
    time.sleep(1)
    self.click_image([f'{self.K_IMG_PAHT}\\start_01.PNG', f'{self.K_IMG_PAHT}\\start_02.PNG'], '없음', 0.5, 1, False)
    time.sleep(3)

def main():
  pass