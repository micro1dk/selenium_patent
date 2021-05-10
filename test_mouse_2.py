import pyautogui
import time

time.sleep(5)

elmnt = pyautogui.locateOnScreen('./test.PNG')
pyautogui.click(elmnt)