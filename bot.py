#!/bin/env python3
# on 08 Jan 2022
import datetime
import os
import time

import pyautogui

pyautogui.FAILSAFE = False

# Init firefox with this size
# firefox -P "bomb2" -width 527 -height 447

GAME_URL = "https://app.bombcrypto.io/webgl/index.html"
EVERY_N_TIMES_OUT_HEROES_WORK = 3

CONFIG = {
    # minutes
    "sleep_time": 70,
    "refresh_map_time": 20,
    # minutes
    "refresh_map": 2,
    "profiles": [
        {
            "name": "bomb1",
            "refresh": (96, 90, 'left'),
            "login_metamask": (401, 626, 'left'),
            "connect_wallet": (256, 355, 'left'),
            "btn_heroes": (464, 406, 'left'),
            "btn_close_heroes": (288, 195, 'left'),
            "btn_work_all": (219, 220, 'left'),
            "btn_back_initial": (43, 155, 'left'),
            "btn_teasure_hunt": (264, 288, 'left'),
            "first_heroe": (110, 240, 'left'),
            "out_heroes": [
                {
                    "class": "super legend",
                    "scroll_length": -28,
                    "btn_rest": (248, 241, 'left')
                }
            ]
        }
    ]
}

def print_time(text=None, minutes=None):
    now = datetime.datetime.now()
    if minutes:
        now = now + datetime.timedelta(minutes=minutes)
    print(f"{text} {now.strftime('%H:%M:%S')}")


def push_button(message: str = None, coord: tuple = None, sleep: int = None, retry: bool = True):
    print_time(text=f"{message}")

    # try 2 times
    pyautogui.mouseDown(*coord)
    pyautogui.mouseUp(*coord)
    time.sleep(1)
    if retry:
        pyautogui.mouseDown(*coord)
        pyautogui.mouseUp(*coord)

    if sleep:
        time.sleep(sleep)

def scroll_to(message: str = None, scroll_length: int = None):
    print_time(text=f"{message}")
    pyautogui.scroll(scroll_length)
    time.sleep(2)

def rest_out_heroes(
    message: str = None, 
    profile: dict = None, 
    interaction: int = None
):
    if interaction % EVERY_N_TIMES_OUT_HEROES_WORK == 0:
        return
    print_time(text=f"{message}")
    for heroe in profile.get('out_heroes'):
        push_button(
            message = f"Select the first heroe",
            coord = profile["first_heroe"],
            sleep = 1
        )

        scroll_to(
            message = f"Scroll to heroe {heroe['class']}", 
            scroll_length = heroe["scroll_length"]
        )

        push_button(
            message = f"Rest heroe {heroe['class']}",
            coord = heroe["btn_rest"],
            sleep = 1,
            retry = False
        )

        scroll_to(
            message = "Scroll to top of list",
            scroll_length = 50
        )

def run():
    while True:
        start_date = datetime.datetime.now()
        interaction = 0
        for profile in CONFIG['profiles']:
            print_time(text=f"Start JOB {profile['name']}")

            push_button(
                message=f"Refresh PAGE {profile['name']}",
                coord=profile["refresh"],
                sleep=12
            )

            push_button(
                message="Connect wallet",
                coord=profile["connect_wallet"],
                sleep=12
            )

            push_button(
                message="Login Metamask",
                coord=profile["login_metamask"],
                sleep=30
            )

            push_button(
                message="Hero select",
                coord=profile["btn_heroes"],
                sleep=4
            )

            push_button(
                message="Go to Work",
                coord=profile["btn_work_all"],
                sleep=3
            )

            rest_out_heroes(
                message = "Rest out heroes",
                profile = profile,
                interaction = interaction
            )

            push_button(
                message="Close Hero Select",
                coord=profile["btn_close_heroes"],
                sleep=3
            )

            push_button(
                message="Treasure hunt",
                coord=profile["btn_teasure_hunt"],
                sleep=5
            )

        while True:
            print_time("Next Interaction on", minutes=CONFIG['refresh_map'])
            time.sleep(CONFIG['refresh_map'] * 60)
            for profile in CONFIG['profiles']:
                push_button(
                    message=f"Refresh Position {profile['name']}",
                    coord=profile["btn_back_initial"],
                    sleep=5
                )

                push_button(
                    message="Back to the game",
                    coord=profile["btn_teasure_hunt"],
                    sleep=1
                )

            sleep_time = CONFIG['sleep_time']
            refresh_map_time = CONFIG['refresh_map_time']
            now = datetime.datetime.now()
            if now >= (
                    start_date + datetime.timedelta(minutes=refresh_map_time)):
                print_time("Sleep until", minutes=sleep_time)
                time.sleep(sleep_time * 60)
                interaction += 1
                break


if __name__ == '__main__':
    run()