import pyautogui


class GUIController:

    def click(self, x, y):
        pyautogui.click(x, y)
        return {"action": "click", "x": x, "y": y}

    def type(self, text):
        pyautogui.write(text)
        return {"action": "type", "text": text}