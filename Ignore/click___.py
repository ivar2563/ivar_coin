import pyautogui
import time
width, height = pyautogui.size()

x = 0
while x != 100:
    pyautogui.click(width/2, height/2)
    x += 1
