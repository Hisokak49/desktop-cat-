import random
import time
import math


class AnimationManager:

    def __init__(self):

        self.frame = 0

        # =========================
        # BLINKING
        # =========================

        self.blinking = False

        self.blink_end = 0

        self.blink_progress = 0

        self.next_blink = (
            time.time()
            + random.randint(2, 6)
        )

        # =========================
        # WALKING
        # =========================

        self.walk_offset = 0

        # =========================
        # TAIL
        # =========================

        self.tail_offset = 0

        self.tail_height = 0

        # =========================
        # TYPING
        # =========================

        self.typing_offset = 0

        # =========================
        # BODY
        # =========================

        self.breath_offset = 0

        self.body_squash = 0

        # =========================
        # EARS
        # =========================

        self.ear_wiggle = 0

        # =========================
        # SLEEP
        # =========================

        self.sleep_float = 0

        # =========================
        # FACE
        # =========================

        self.whisker_offset = 0

        self.head_tilt = 0

        # =========================
        # ZOOMIES
        # =========================

        self.zoom_speed_lines = 0

    # =====================================
    # MAIN UPDATE
    # =====================================

    def update(self):

        now = time.time()

        # =========================
        # BLINKING
        # =========================

        if now >= self.next_blink:

            self.blinking = True

            self.blink_end = now + 0.15

            self.next_blink = (
                now
                + random.randint(2, 6)
            )

        if self.blinking:

            remaining = (
                self.blink_end - now
            )

            self.blink_progress = max(
                0,
                remaining / 0.15
            )

            if now >= self.blink_end:

                self.blinking = False

                self.blink_progress = 0

        # =========================
        # FRAME COUNTER
        # =========================

        self.frame += 1

        # =========================
        # WALK BOUNCE
        # =========================

        self.walk_offset = (
            (self.frame // 10) % 2
        )

        # =========================
        # TAIL SWING
        # =========================

        self.tail_offset = (
            (self.frame // 6) % 7
        ) - 3

        # =========================
        # TAIL HEIGHT
        # =========================

        self.tail_height = (
            math.sin(
                self.frame * 0.12
            ) * 8
        )

        # =========================
        # TYPING PAWS
        # =========================

        self.typing_offset = (
            (self.frame // 3) % 4
        )

        # =========================
        # BREATHING
        # =========================

        self.breath_offset = (
            math.sin(
                self.frame * 0.08
            ) * 2
        )

        # =========================
        # BODY SQUASH
        # =========================

        self.body_squash = (
            math.sin(
                self.frame * 0.10
            ) * 2
        )

        # =========================
        # EAR TWITCH
        # =========================

        self.ear_wiggle = (
            math.sin(
                self.frame * 0.15
            ) * 3
        )

        # =========================
        # SLEEP FLOAT
        # =========================

        self.sleep_float = (
            math.sin(
                self.frame * 0.05
            ) * 3
        )

        # =========================
        # WHISKERS
        # =========================

        self.whisker_offset = (
            math.sin(
                self.frame * 0.25
            ) * 2
        )

        # =========================
        # HEAD TILT
        # =========================

        self.head_tilt = (
            math.sin(
                self.frame * 0.04
            ) * 2
        )

        # =========================
        # ZOOMIES SPEED LINES
        # =========================

        self.zoom_speed_lines = (
            (self.frame // 2) % 5
        )

    # =====================================
    # BLINK
    # =====================================

    def is_blinking(self):

        return self.blinking

    def get_blink_progress(self):

        return self.blink_progress

    # =====================================
    # WALK
    # =====================================

    def get_walk_offset(self):

        return self.walk_offset

    # =====================================
    # TAIL
    # =====================================

    def get_tail_offset(self):

        return self.tail_offset

    def get_tail_height(self):

        return self.tail_height

    # =====================================
    # TYPING
    # =====================================

    def get_typing_offset(self):

        return self.typing_offset

    # =====================================
    # BODY
    # =====================================

    def get_breath_offset(self):

        return self.breath_offset

    def get_body_squash(self):

        return self.body_squash

    # =====================================
    # EARS
    # =====================================

    def get_ear_wiggle(self):

        return self.ear_wiggle

    # =====================================
    # SLEEP
    # =====================================

    def get_sleep_float(self):

        return self.sleep_float

    # =====================================
    # FACE
    # =====================================

    def get_whisker_offset(self):

        return self.whisker_offset

    def get_head_tilt(self):

        return self.head_tilt

    # =====================================
    # ZOOMIES
    # =====================================

    def get_zoom_speed_lines(self):

        return self.zoom_speed_lines