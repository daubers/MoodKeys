import threading
import time
import keybow

LED_WAITING_FOR_RESPONSE = (125, 0, 255)
LED_RESPONSE_GOOD = (0, 255, 0)
LED_RESPONSE_FAIL = (255, 0, 0)
LED_OFF = (0, 0, 0)


default_state = {
    'op': None,
    'color': (0, 0, 0),
    'mode': 'idle'
}


class Flash(threading.Thread):
    def __init__(self, index, color, *args, **kwargs):
        threading.Thread.__init__(self, *args[2:], **kwargs)
        self.index = index
        self.color = color
        print(self.color, self.index)
        self._on = False
        self.running = False

    def run(self) -> None:
        self.running = True

        while self.running:
            if not self._on:
                keybow.set_led(self.index, *self.color)
                self._on = True
            else:
                keybow.set_led(self.index, *LED_OFF)
                self._on = False
            time.sleep(0.25)

    def stop(self):
        self.running = False
        keybow.set_led(self.index, *LED_OFF)


class LedManager(object):
    def __init__(self, *args, **kwargs):
        super(LedManager).__init__(*args, **kwargs)
        self.led_states = [default_state.copy() for i in range(0, 12)]
        keybow.clear()


    def flash_waiting(self, index):
        print(self.led_states[index])
        if self.led_states[index]['mode'] == 'idle':
            self.led_states[index]['mode'] = 'waiting'
            self.led_states[index]['op'] = Flash(index, LED_WAITING_FOR_RESPONSE)
            self.led_states[index]['op'].start()