import keybow
import time
import requests
from .led_blink import LedManager

url = "https://maker.ifttt.com/trigger/{event}/with/key/kPkzZq6J5qeEP5I6zkVnFlh2YTjjvYwwQ90_-ze97RP".format(
    event='emotion_update')

led_man = LedManager()

def make_request(emotion, index):
    data = {
        'value1': emotion
    }

    requests.post(url, json=data)


@keybow.on()
def handle_key(index, state):
    print("{}: Key {} has been {}".format(
        time.time(),
        index,
        'pressed' if state else 'released'))

    if state:
        keybow.set_led(index, 125, 0, 255)
        led_man.flash_waiting(index)
    else:
        keybow.set_led(index, 0, 0, 0)


def main():
    while True:
        keybow.show()
        time.sleep(1.0 / 60.0)


if __name__ == "__main__":
    main()
