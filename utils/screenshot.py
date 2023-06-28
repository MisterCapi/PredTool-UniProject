import time

import pyautogui


def get_game_screenshot():
    # Get the coordinates of the application window
    app_window = pyautogui.getWindowsWithTitle('Predecessor')[0]

    # Get the coordinates of the top-left corner of the application window
    app_x, app_y = app_window.topleft

    # Get the width and height of the application window
    app_width, app_height = app_window.size

    # Take a screenshot of the application window
    screenshot = pyautogui.screenshot(region=(app_x, app_y, app_width, app_height))

    # Save the screenshot to a file
    screen_path = 'screenshot.png'
    screenshot.save(screen_path)
    return screen_path


if __name__ == '__main__':
    time.sleep(5)
    get_game_screenshot()
