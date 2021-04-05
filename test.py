import pyautogui
import pyperclip

pyautogui.moveTo(361, 203)
pyautogui.dragTo(407, 229, 0.5 ,button='left')
pyautogui.hotkey('ctrl', 'c') # 드래그된 내용 복사하기
t = pyperclip.paste() # 클립보드에 저장된 데이터 할당하기
