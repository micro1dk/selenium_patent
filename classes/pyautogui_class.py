import time
import pyautogui

class PyautoGUI:
  def __init__(self):
    pass

  def wait_image_visible(self, png, delay, timeout):
    """
    png: str 또는 list 형식
    png와 일치하는 요소가 보일 때 까지 기다린다.
    성공여부와 엘리먼트를 Tuple로 반환
    """
    t = 0
    while True:
      if isinstance(png, str):
        element = pyautogui.locateOnScreen(png)
        if element:
          return True, element

      if isinstance(png, list):
        for p in png:
          element = pyautogui.locateOnScreen(p)
          if element:
            return True, element
      time.sleep(delay)
      t += delay
      if t >= timeout:
        return False, None

  def wait_image_invisible(self, png, delay, timeout):
    def exc():
      try:
        if str(type(png)) == "<class 'list'>":
          for p in png:  
            element = pyautogui.locateOnScreen(p)
            if element:
              return False
        elif str(type(png)) == "<class 'str'>":
          element = pyautogui.locateOnScreen(png)
          if element:
            return False
        return True
      except Exception as e:
        # print(e)
        return False

    t = 0
    while t < timeout:
      success = exc()
      if success:
        return True
      time.sleep(delay)
      t += delay
    return False
  
  def click_image(self, png, err_msg, delay, timeout, raise_error):
    """
    요소가 보이기까지 기다린 후
    있으면 클릭
    없으면 에러를 발생시킴
    """
    success, element = self.wait_image_visible(png, delay, timeout)
    # print(f'{png}있는가? {success}')
    time.sleep(0.3)
    if success:
      pyautogui.click(element)
      return True
.
    if raise_error:
      raise Exception('이미지 클릭실패 : ' + err_msg)
    return False

  def move_mouse(self, png, err, delay, timeout):
    """
    요소위로 마우스를 올리기만 함
    있으면 True
    없으면 FAlse를 반환
    """
    success, element = self.wait_image_visible(png, delay, timeout)
    time.sleep(0.3)
    if success:
      pyautogui.moveTo(element)
      return True

    if raise_error:
      raise Exception(err_msg)
    return False
