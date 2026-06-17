from pynput import keyboard
import threading
import time


class KeyboardTracker:

    def __init__(self):

        self.typing = False

        self.last_key_time = time.time()

        self.total_keys = 0

        self.keys_last_second = 0

        self.last_second_reset = time.time()

        self.current_streak = 0

        self.longest_streak = 0

        self.last_key = None

        self.listener = keyboard.Listener(
            on_press=self.on_press
        )

    # -------------------------
    # START
    # -------------------------

    def start(self):

        threading.Thread(
            target=self.listener.start,
            daemon=True
        ).start()

    # -------------------------
    # KEY PRESS
    # -------------------------

    def on_press(self, key):

        self.typing = True

        self.last_key_time = time.time()

        self.total_keys += 1

        self.keys_last_second += 1

        self.current_streak += 1

        if self.current_streak > self.longest_streak:

            self.longest_streak = (
                self.current_streak
            )

        try:

            self.last_key = key.char

        except:

            self.last_key = str(key)

    # -------------------------
    # UPDATE
    # -------------------------

    def update(self):

        now = time.time()

        # stop typing

        if now - self.last_key_time > 1:

            self.typing = False

            self.current_streak = 0

        # reset KPS counter

        if now - self.last_second_reset > 1:

            self.keys_last_second = 0

            self.last_second_reset = now

    # -------------------------
    # BASIC
    # -------------------------

    def is_typing(self):

        self.update()

        return self.typing

    def get_idle_time(self):

        return (
            time.time()
            - self.last_key_time
        )

    # -------------------------
    # STATS
    # -------------------------

    def get_total_keys(self):

        return self.total_keys

    def get_last_key(self):

        return self.last_key

    def get_keys_per_second(self):

        self.update()

        return self.keys_last_second

    def get_current_streak(self):

        return self.current_streak

    def get_longest_streak(self):

        return self.longest_streak

    # -------------------------
    # SMART DETECTION
    # -------------------------

    def is_fast_typing(self):

        return (
            self.keys_last_second >= 5
        )

    def is_coding_mode(self):

        if not self.typing:
            return False

        return (
            self.keys_last_second >= 3
        )

    def is_afk(self):

        return (
            self.get_idle_time() > 60
        )

    # -------------------------
    # DEBUG
    # -------------------------

    def get_stats(self):

        return {

            "typing": self.typing,

            "total_keys": self.total_keys,

            "keys_per_second":
                self.keys_last_second,

            "current_streak":
                self.current_streak,

            "longest_streak":
                self.longest_streak,

            "last_key":
                self.last_key,

            "idle_time":
                round(
                    self.get_idle_time(),
                    2
                )

        }