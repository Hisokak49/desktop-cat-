import random
import time


class SpeechManager:

    def __init__(self):

        self.text = ""
        self.end_time = 0

        self.last_random_thought = time.time()

        # configurable later via config.py
        self.thought_interval = 20
        self.thought_chance = 0.25

        # ==========================
        # IDLE
        # ==========================

        self.idle_thoughts = [
            "hello human",
            "feed me",
            "pet me",
            "nap time",
            "where fish?",
            "mouse detected",
            "tail.exe running",
            "i love bugs",
            "today feels nice",
            "purrr"
        ]

        # ==========================
        # TYPING
        # ==========================

        self.typing_thoughts = [
            "keep coding!",
            "nice typing!",
            "debugging again?",
            "ship it!",
            "python detected",
            "wow fast fingers",
            "clean code = happy cat",
            "human focused"
        ]

        # ==========================
        # SLEEP
        # ==========================

        self.sleep_thoughts = [
            "zzz...",
            "dreaming...",
            "so sleepy...",
            "nap mode",
            "do not disturb"
        ]

        # ==========================
        # ZOOMIES
        # ==========================

        self.zoomies_thoughts = [
            "ZOOOOM!",
            "NYOOOOM!",
            "I AM SPEED",
            "catch me!",
            "maximum velocity!"
        ]

        # ==========================
        # PLAY
        # ==========================

        self.play_thoughts = [
            "toy detected!",
            "mine!",
            "play time!",
            "got it!",
            "fish!!!",
            "mouse acquired"
        ]

        # ==========================
        # WATCH
        # ==========================

        self.watch_thoughts = [
            "what are you doing?",
            "i see you",
            "interesting...",
            "watching...",
            "hmmm..."
        ]

        # ==========================
        # PRODUCTIVITY
        # ==========================

        self.productivity_thoughts = [
            "focus mode",
            "deep work activated",
            "one step at a time",
            "small progress counts",
            "keep going"
        ]

    # ====================================
    # CORE
    # ====================================

    def say(self, text, duration=3):

        self.text = text
        self.end_time = time.time() + duration

    def clear(self):

        self.text = ""
        self.end_time = 0

    def is_showing(self):

        return time.time() < self.end_time

    def get_text(self):

        if self.is_showing():
            return self.text

        return ""

    # ====================================
    # RANDOM THOUGHTS
    # ====================================

    def update_random_thoughts(self):

        now = time.time()

        if now - self.last_random_thought < self.thought_interval:
            return

        self.last_random_thought = now

        if random.random() > self.thought_chance:
            return

        self.say(
            random.choice(
                self.idle_thoughts
            ),
            duration=4
        )

    # ====================================
    # STATE REACTIONS
    # ====================================

    def typing_message(self):

        self.say(
            random.choice(
                self.typing_thoughts
            ),
            duration=3
        )

    def sleep_message(self):

        self.say(
            random.choice(
                self.sleep_thoughts
            ),
            duration=4
        )

    def zoomies_message(self):

        self.say(
            random.choice(
                self.zoomies_thoughts
            ),
            duration=2
        )

    def play_message(self):

        self.say(
            random.choice(
                self.play_thoughts
            ),
            duration=3
        )

    def watch_message(self):

        self.say(
            random.choice(
                self.watch_thoughts
            ),
            duration=3
        )

    def productivity_message(self):

        self.say(
            random.choice(
                self.productivity_thoughts
            ),
            duration=3
        )

    # ====================================
    # REMINDERS
    # ====================================

    def water_reminder(self):

        self.say(
            "drink water!",
            duration=5
        )

    def stretch_reminder(self):

        self.say(
            "stretch time!",
            duration=5
        )

    def break_reminder(self):

        self.say(
            "take a break!",
            duration=5
        )

    def work_reminder(self):

        self.say(
            "back to work!",
            duration=5
        )

    # ====================================
    # TOYS
    # ====================================

    def toy_found(self):

        self.say(
            "toy spotted!",
            duration=3
        )

    def toy_caught(self):

        self.say(
            "got it!",
            duration=3
        )

    # ====================================
    # CODING
    # ====================================

    def bug_detected(self):

        self.say(
            "probably a typo",
            duration=4
        )

    def build_success(self):

        self.say(
            "it works!",
            duration=4
        )

    def coding_focus(self):

        self.say(
            "focus mode",
            duration=3
        )

    def fast_typing(self):

        self.say(
            "speed typing!",
            duration=3
        )

    # ====================================
    # DEBUG
    # ====================================

    def get_debug_info(self):

        return {
            "showing": self.is_showing(),
            "text": self.get_text(),
            "time_left": max(
                0,
                round(
                    self.end_time - time.time(),
                    2
                )
            )
        }