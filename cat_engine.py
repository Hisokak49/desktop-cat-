import tkinter as tk
import random
import math
import time

from cat_states import CatState
from animations import AnimationManager
from mouse_tracker import MouseTracker
from keyboard_tracker import KeyboardTracker
from speech import SpeechManager
from reminders import ReminderManager
from toys import ToyManager
from sprite_loader import PixelSprite

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    FOLLOW_SPEED,
    SLEEP_AFTER_SECONDS
)
from config import CAT_COLOR, CAT_OUTLINE
from config import PIXEL_SCALE
from config import (
    WANDER_X_RANGE,
    WANDER_Y_RANGE,
    WANDER_MIN_SECONDS,
    WANDER_MAX_SECONDS,
    ROAM_NEXT_MIN,
    ROAM_NEXT_MAX,
    ROAM_ACTIVE_MIN,
    ROAM_ACTIVE_MAX,
    ROAM_PROBABILITY,
    HIDE_MOUSE_THRESHOLD,
    UNHIDE_MOUSE_THRESHOLD,
    HIDE_DURATION_MIN,
    HIDE_DURATION_MAX,
    TOY_CHASE_DISTANCE,
    TOY_CATCH_DISTANCE,
    PET_CLICK_RADIUS,
    CHASE_SPEED_MULTIPLIER
)
from config import (
    ENABLE_HIDING,
    SMOOTHING_FACTOR,
    MAX_VELOCITY
)

# =====================================
# PIXEL SPRITES
# =====================================

CAT_IDLE = [

"00000111111100000",
"00011111111111000",
"00111111111111100",
"01111111111111110",
"01111011111011110",
"11111111111111111",
"11111111111111111",
"11111111111111111",
"01111111111111110",
"00111111111111100",
"00011111111111000"

]

CAT_SLEEP = [

"00000111111100000",
"00011111111111000",
"00111111111111100",
"01110000000011110",
"01111111111111110",
"11111111111111111",
"11111111111111111",
"01111111111111110",
"00111111111111100"

]

CAT_TYPING = [

"00000111111100000",
"00011111111111000",
"00111111111111100",
"01111111111111110",
"01111011111011110",
"11111111111111111",
"11111111111111111",
"11111111111111111",
"01111111111111110",
"00111111111111100",
"00011000000110000"

]


class CatEngine:

    def __init__(self, root):

        self.root = root

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg="green",
            highlightthickness=0
        )

        self.canvas.pack()

        self.cat_x = random.randint(100, 1000)
        self.cat_y = random.randint(100, 600)

        self.state = CatState.IDLE

        self.anim = AnimationManager()

        self.mouse_tracker = MouseTracker()
        self.mouse_tracker.start()

        self.keyboard_tracker = KeyboardTracker()
        self.keyboard_tracker.start()

        self.mood = "happy"

        self.speech_manager = SpeechManager()
        self.reminder_manager = ReminderManager()
        self.toy_manager = ToyManager()

        self.speech = ""
        self.speech_until = 0

        self.next_zoomies = (
            time.time()
            + random.randint(30, 60)
        )

        self.last_thought = time.time()

        # wander offsets so the cat doesn't perfectly track the cursor
        self.wander_offset_x = 0
        self.wander_offset_y = 0
        self.next_wander = time.time() + random.uniform(
            WANDER_MIN_SECONDS,
            WANDER_MAX_SECONDS
        )
        # roaming targets so the cat moves on its own often
        self.roam_target_x = self.cat_x
        self.roam_target_y = self.cat_y
        self.next_roam = time.time() + random.uniform(
            ROAM_NEXT_MIN,
            ROAM_NEXT_MAX
        )
        self.roam_active_until = 0
        self.roam_probability = ROAM_PROBABILITY
        # hide state (when mouse goes to bottom of screen)
        self.hidden = False
        self.hidden_until = 0

        # velocity for smooth movement
        self.vx = 0.0
        self.vy = 0.0

        self.update()

    # =====================================
    # SPEECH
    # =====================================

    def say(self, text, duration=3):
        # delegate to SpeechManager for consistent message handling
        try:
            self.speech_manager.say(text, duration)
        except Exception:
            # fallback to local vars if speech_manager not available
            self.speech = text
            self.speech_until = time.time() + duration

    # =====================================
    # PIXEL DRAWING
    # =====================================

    def draw_sprite(
        self,
        sprite,
        x,
        y,
        scale=6,
        color="#ff9f1c"
    ):

        for row_i, row in enumerate(sprite):

            for col_i, pixel in enumerate(row):

                if pixel == "1":

                    px = (
                        x +
                        col_i * scale
                    )

                    py = (
                        y +
                        row_i * scale
                    )

                    self.canvas.create_rectangle(
                        px,
                        py,
                        px + scale,
                        py + scale,
                        fill=color,
                        outline=""
                    )
    # =====================================
    # STATE MACHINE
    # =====================================

    def update_state(self):

        now = time.time()

        mx, my = self.mouse_tracker.get_position()

        distance = math.hypot(
            mx - self.cat_x,
            my - self.cat_y
        )

        # typing
        if self.keyboard_tracker.is_typing():

            if self.state != CatState.TYPING:

                if random.random() < 0.3:

                    self.say(
                        random.choice([
                            "keep coding!",
                            "nice typing!",
                            "human busy...",
                            "click clack!"
                        ])
                    )

            self.state = CatState.TYPING
            return

        # hide when mouse goes off-screen/bottom (simple heuristic)
        # hide/unhide (disabled when ENABLE_HIDING is False)
        if ENABLE_HIDING:

            if my > (WINDOW_HEIGHT - HIDE_MOUSE_THRESHOLD) and not self.hidden:

                if random.random() < 0.6:

                    self.hidden = True
                    self.hidden_until = (
                        time.time()
                        + random.uniform(
                            HIDE_DURATION_MIN,
                            HIDE_DURATION_MAX
                        )
                    )

                    self.say("hide...")

            if self.hidden and my < (WINDOW_HEIGHT - UNHIDE_MOUSE_THRESHOLD):

                self.hidden = False
                self.say("peek!")
                return

        # sleep
        if (
            self.mouse_tracker.get_idle_time()
            > SLEEP_AFTER_SECONDS
        ):

            if self.state != CatState.SLEEP:

                self.say("zzz...")

            self.state = CatState.SLEEP
            return

        # zoomies
        if now >= self.next_zoomies:

            self.state = CatState.ZOOMIES

            self.say("ZOOOOM!")

            self.next_zoomies = (
                now +
                random.randint(40, 90)
            )

            return

        # curiosity
        if distance < 150:

            self.state = CatState.WATCH
            return

        # follow
        self.state = CatState.FOLLOW

    # =====================================
    # MOODS
    # =====================================

    def update_mood(self):

        if self.state == CatState.SLEEP:

            self.mood = "sleepy"

        elif self.state == CatState.TYPING:

            self.mood = "focused"

        elif self.state == CatState.WATCH:

            self.mood = "curious"

        elif self.state == CatState.ZOOMIES:

            self.mood = "crazy"

        else:

            self.mood = "happy"

    # =====================================
    # RANDOM THOUGHTS
    # =====================================

    def random_thoughts(self):

        now = time.time()

        if now - self.last_thought < 20:
            return

        self.last_thought = now

        if random.random() > 0.25:
            return

        thoughts = [

            "feed me",
            "what is code?",
            "mouse detected",
            "nap time",
            "hello human",
            "i am watching",
            "pet me",
            "stretching...",
            "tail.exe running",
            "where fish?"
        ]

        self.say(
            random.choice(thoughts),
            duration=4
        )

    # =====================================
    # MOVEMENT
    # =====================================

    def move_cat(self):

        mx, my = (
            self.mouse_tracker
            .get_position()
        )

        # sleeping
        if self.state == CatState.SLEEP:
            return

        # zoomies
        if self.state == CatState.ZOOMIES:

            angle = random.random() * (
                math.pi * 2
            )

            self.cat_x += (
                math.cos(angle) * 12
            )

            self.cat_y += (
                math.sin(angle) * 12
            )

            return

        # watching
        if self.state == CatState.WATCH:

            return

        # following / roaming behavior with autonomous roaming mode (smooth velocity)
        now = time.time()

        # refresh roam target occasionally
        if now >= self.next_roam:
            self.roam_target_x = random.uniform(0, self.root.winfo_screenwidth() - WINDOW_WIDTH)
            self.roam_target_y = random.uniform(0, self.root.winfo_screenheight() - WINDOW_HEIGHT)
            self.roam_active_until = now + random.uniform(ROAM_ACTIVE_MIN, ROAM_ACTIVE_MAX)
            self.next_roam = now + random.uniform(ROAM_NEXT_MIN, ROAM_NEXT_MAX)

        # decide whether to roam or follow the mouse
        is_roaming = False
        if now < self.roam_active_until and random.random() < self.roam_probability:
            is_roaming = True

        if is_roaming:
            target_x = self.roam_target_x
            target_y = self.roam_target_y

            # if we're very close to the roam target, end roaming early
            if math.hypot(target_x - self.cat_x, target_y - self.cat_y) < 8:
                self.roam_active_until = 0

            base_speed = FOLLOW_SPEED * 0.6

        else:
            # follow the mouse but with wander so it's not perfect
            if now >= self.next_wander:
                self.wander_offset_x = random.uniform(-WANDER_X_RANGE, WANDER_X_RANGE)
                self.wander_offset_y = random.uniform(-WANDER_Y_RANGE, WANDER_Y_RANGE)
                self.next_wander = now + random.uniform(WANDER_MIN_SECONDS, WANDER_MAX_SECONDS)

            target_x = mx + self.wander_offset_x
            target_y = my + self.wander_offset_y

            base_speed = FOLLOW_SPEED * 1.0

        # speed reaction to quick mouse motion
        if self.mouse_tracker.should_chase():
            base_speed *= CHASE_SPEED_MULTIPLIER

        # desired velocity towards target
        desired_vx = (target_x - self.cat_x) * base_speed
        desired_vy = (target_y - self.cat_y) * base_speed

        # clamp desired velocity
        speed_mag = math.hypot(desired_vx, desired_vy)
        if speed_mag > MAX_VELOCITY:
            factor = MAX_VELOCITY / speed_mag
            desired_vx *= factor
            desired_vy *= factor

        # smooth current velocity toward desired velocity
        self.vx += (desired_vx - self.vx) * SMOOTHING_FACTOR
        self.vy += (desired_vy - self.vy) * SMOOTHING_FACTOR

        # update position
        self.cat_x += self.vx
        self.cat_y += self.vy

    # =====================================
    # WINDOW BOUNDS
    # =====================================

    def keep_inside_screen(self):

        self.cat_x = max(
            0,
            min(
                self.cat_x,
                self.root.winfo_screenwidth()
                - WINDOW_WIDTH
            )
        )

        self.cat_y = max(
            0,
            min(
                self.cat_y,
                self.root.winfo_screenheight()
                - WINDOW_HEIGHT
            )
        )

    # =====================================
    # UPDATE LOGIC
    # =====================================

    def logic_update(self):
        now = time.time()

        self.update_state()

        self.update_mood()

        self.random_thoughts()

        # update SpeechManager random thoughts
        try:
            self.speech_manager.update_random_thoughts()
        except Exception:
            pass

        # update toys
        self.toy_manager.update()

        # if there's a nearby toy, bias roaming toward it so the cat plays
        nearest_toy = self.toy_manager.get_nearest_toy(
            self.cat_x,
            self.cat_y
        )

        if nearest_toy is not None:

            dist = nearest_toy.distance_to(
                self.cat_x,
                self.cat_y
            )

            if dist < TOY_CHASE_DISTANCE:
                # chase the toy
                self.roam_target_x = nearest_toy.x
                self.roam_target_y = nearest_toy.y
                self.roam_active_until = now + 5.0
                self.roam_probability = 0.95

                # if very close, catch it
                if dist < TOY_CATCH_DISTANCE:
                    self.toy_manager.catch_toy(nearest_toy)
                    self.say("got it!", 2)

        # petting: if user clicks near the cat, react positively
        mx, my = self.mouse_tracker.get_position()
        click_dist = math.hypot(
            mx - self.cat_x,
            my - self.cat_y
        )

        if self.mouse_tracker.is_left_clicking() and click_dist < 80:
            self.mood = "happy"
            self.say("purr...", 2)
            # pause roaming briefly
            self.roam_active_until = now + 2.0

        # check reminders
        reminder = self.reminder_manager.check_reminders()

        if reminder == "water":
            self.say("drink water!", 5)

        elif reminder == "stretch":
            self.say("stretch time!", 5)

        # hide/disappear behavior: if mouse goes to bottom of screen, hide window
        if ENABLE_HIDING:
            screen_h = self.root.winfo_screenheight()

            # if mouse is very low on screen, go hide off-screen for a bit
            if (not self.hidden) and my > (screen_h - HIDE_MOUSE_THRESHOLD):
                self.hidden = True
                self.hidden_until = now + random.uniform(HIDE_DURATION_MIN, HIDE_DURATION_MAX)
                self.say("hiding...", 2)

            if self.hidden:
                # unhide if time passed or mouse moved away from bottom
                if now >= self.hidden_until or my < (screen_h - UNHIDE_MOUSE_THRESHOLD):
                    self.hidden = False
                    self.say("peek!", 1)

        # finally move cat according to current behavior
        self.move_cat()

        self.keep_inside_screen()
    # =====================================
    # DRAW SPEECH BUBBLE
    # =====================================

    def draw_speech(self):
        text = ""
        try:
            text = self.speech_manager.get_text()
        except Exception:
            text = self.speech if hasattr(self, "speech") else ""

        if not text:
            return

        self.canvas.create_rectangle(
            10,
            5,
            WINDOW_WIDTH - 10,
            35,
            fill="white",
            outline="black"
        )

        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            20,
            text=text,
            fill="black",
            font=("Arial", 10, "bold")
        )

    # =====================================
    # DRAW PIXEL CAT
    # =====================================

    def draw_cat(self):

        self.canvas.delete("all")

        bounce = self.anim.get_walk_offset()

        breath = self.anim.get_breath_offset()

        sleep_float = (
            self.anim.get_sleep_float()
        )

        head_tilt = self.anim.get_head_tilt()

        body_squash = self.anim.get_body_squash()

        typing_offset = self.anim.get_typing_offset()

        blinking = self.anim.is_blinking()

        # choose sprite

        sprite = CAT_IDLE

        if self.state == CatState.SLEEP:

            sprite = CAT_SLEEP

        elif self.state == CatState.TYPING:

            sprite = CAT_TYPING

        # sleeping animation

        offset_y = 25 + body_squash

        if self.state == CatState.SLEEP:

            offset_y += sleep_float

        else:

            offset_y += bounce

        # =================================
        # PIXEL BODY (draw pixel-art torso + legs behind head)
        # We'll draw a small pixel-sprite body underneath the head sprite
        # so the overall look matches the pixel-art style from your image.
        # =================================

        # body sprites (17 columns wide to match head width)
        # sharper, smaller torso (still 17 cols to align under head)
        BODY_IDLE = [
            "00000000000000000",
            "00000111111000000",
            "00001111111100000",
            "00001111111100000",
            "00001111111100000",
            "00000111111000000",
            "00000011100000000"
        ]

        BODY_SLEEP = [
            "00000000000000000",
            "00000111111000000",
            "00001111111100000",
            "00001111111100000",
            "00001111111100000",
            "00000111111000000",
            "00000011000000000"
        ]

        BODY_TYPING = [
            "00000000000000000",
            "00000111111000000",
            "00001111111100000",
            "00001111111100000",
            "00000111111000000",
            "00000110011000000",
            "00000011000000000"
        ]

        scale = PIXEL_SCALE

        # colors
        BODY_COLOR = "#000000"  # black body as requested
        PAW_COLOR = CAT_COLOR
        NOSE_COLOR = "white"

        # where to place the body: slightly below the head sprite
        head_h = len(sprite) * scale
        body_y = offset_y + head_h - (scale * 2)

        body_sprite = BODY_IDLE

        if self.state == CatState.SLEEP:
            body_sprite = BODY_SLEEP
        elif self.state == CatState.TYPING:
            body_sprite = BODY_TYPING

        # draw body (behind the head) in body color
        self.draw_sprite(
            body_sprite,
            40,
            body_y,
            scale=scale,
            color=BODY_COLOR
        )

        # overlay hind legs in paw color (pixel-aligned)
        hind_left_x = 40 + 3 * scale
        hind_right_x = 40 + 11 * scale
        hind_y = body_y + (4 * scale)

        self.canvas.create_rectangle(
            hind_left_x,
            hind_y,
            hind_left_x + (2 * scale),
            hind_y + (2 * scale),
            fill=PAW_COLOR,
            outline=""
        )

        self.canvas.create_rectangle(
            hind_right_x,
            hind_y,
            hind_right_x + (2 * scale),
            hind_y + (2 * scale),
            fill=PAW_COLOR,
            outline=""
        )

        # front legs: smaller, sharp rectangles placed under chest
        front_left_x = 40 + 4 * scale
        front_right_x = 40 + 9 * scale
        front_leg_top = body_y + (2 * scale)
        front_leg_bottom = body_y + (5 * scale)

        self.canvas.create_rectangle(
            front_left_x,
            front_leg_top,
            front_left_x + (2 * scale),
            front_leg_bottom,
            fill=PAW_COLOR,
            outline=""
        )

        self.canvas.create_rectangle(
            front_right_x,
            front_leg_top,
            front_right_x + (2 * scale),
            front_leg_bottom,
            fill=PAW_COLOR,
            outline=""
        )

        # draw head/sprite on top of body (head uses body color for black cat)
        self.draw_sprite(
            sprite,
            40,
            offset_y,
            scale=scale,
            color=BODY_COLOR
        )

        # draw nose (centered under eyes)
        head_width = len(sprite[0]) * scale
        nose_x = 40 + head_width // 2
        nose_y = offset_y + (len(sprite) - 3) * scale

        self.canvas.create_oval(
            nose_x - scale,
            nose_y - (scale // 2),
            nose_x + scale,
            nose_y + (scale // 2),
            fill=NOSE_COLOR,
            outline=""
        )

        # =================================
        # TAIL
        # =================================

        tail_x = 145

        tail_y = 85

        tail_side = (
            self.anim.get_tail_offset()
        )

        tail_height = (
            self.anim.get_tail_height()
        )

        self.canvas.create_line(
            tail_x,
            tail_y,
            tail_x + 30 + tail_side,
            tail_y - 20 - tail_height,
            width=8,
            smooth=True,
            fill=BODY_COLOR
        )

        # =================================
        # BREATHING BODY EFFECT
        # =================================

        # subtle shadow under body (sharp rectangle rather than oval)
        shadow_top = body_y + (len(body_sprite) * scale)
        self.canvas.create_rectangle(
            60,
            shadow_top,
            120,
            shadow_top + 4,
            fill="#101010",
            outline=""
        )

        # =================================
        # EAR TWITCH
        # =================================

        ear = (
            self.anim.get_ear_wiggle()
        )

        self.canvas.create_line(
            65,
            35,
            60 - ear,
            20 - ear,
            width=4,
            fill="#ff9f1c"
        )

        self.canvas.create_line(
            125,
            35,
            130 + ear,
            20 - ear,
            width=4,
            fill="#ff9f1c"
        )

        # =================================
        # WHISKERS
        # =================================

        whisk = (
            self.anim.get_whisker_offset()
        )

        self.canvas.create_line(
            55,
            75 + head_tilt,
            20 - whisk,
            70,
            fill="white"
        )

        self.canvas.create_line(
            55,
            82 + head_tilt,
            20 - whisk,
            86,
            fill="white"
        )

        self.canvas.create_line(
            125,
            75 + head_tilt,
            160 + whisk,
            70,
            fill="white"
        )

        self.canvas.create_line(
            125,
            82 + head_tilt,
            160 + whisk,
            86,
            fill="white"
        )

        # =================================
        # EYES
        # =================================

        if self.state == CatState.SLEEP:

            self.canvas.create_line(
                75,
                65,
                85,
                65,
                width=2
            )

            self.canvas.create_line(
                105,
                65,
                115,
                65,
                width=2
            )

        elif blinking:

            self.canvas.create_line(
                75,
                65,
                85,
                65,
                width=2
            )

            self.canvas.create_line(
                105,
                65,
                115,
                65,
                width=2
            )

        else:

            eye = "lime"

            if self.mood == "focused":
                eye = "cyan"

            elif self.mood == "crazy":
                eye = "orange"

            elif self.mood == "curious":
                eye = "yellow"

            self.canvas.create_oval(
                75,
                60,
                85,
                70,
                fill=eye
            )

            self.canvas.create_oval(
                105,
                60,
                115,
                70,
                fill=eye
            )

        # =================================
        # TYPING PAWS
        # =================================

        if self.state == CatState.TYPING:

            paw_y = 118 + typing_offset

            self.canvas.create_line(
                75,
                paw_y,
                95,
                paw_y + 4,
                width=4,
                fill="#ff9f1c"
            )

            self.canvas.create_line(
                105,
                paw_y + 4,
                125,
                paw_y,
                width=4,
                fill="#ff9f1c"
            )

        # =================================
        # FRONT PAWS (in front of sprite)
        # Animate slightly with typing and breathing
        # =================================

        paw_base_y = 118 + int(body_squash)

        if self.state == CatState.TYPING:

            paw_y = 118 + typing_offset

            self.canvas.create_oval(
                70,
                paw_y,
                94,
                paw_y + 12,
                fill=PAW_COLOR,
                outline=""
            )

            self.canvas.create_oval(
                104,
                paw_y,
                128,
                paw_y + 12,
                fill=PAW_COLOR,
                outline=""
            )

        elif self.state == CatState.SLEEP:

            # tucked paws when sleeping
            self.canvas.create_oval(
                80,
                paw_base_y + 6,
                98,
                paw_base_y + 16,
                fill=PAW_COLOR,
                outline=""
            )

            self.canvas.create_oval(
                102,
                paw_base_y + 6,
                120,
                paw_base_y + 16,
                fill=PAW_COLOR,
                outline=""
            )

        else:

            # resting front paws
            self.canvas.create_oval(
                70,
                paw_base_y,
                92,
                paw_base_y + 12,
                fill=PAW_COLOR,
                outline=""
            )

            self.canvas.create_oval(
                106,
                paw_base_y,
                128,
                paw_base_y + 12,
                fill=PAW_COLOR,
                outline=""
            )

        # =================================
        # ZZZ
        # =================================

        if self.state == CatState.SLEEP:

            self.canvas.create_text(
                160,
                25,
                text="Z z z",
                fill="white",
                font=("Arial", 12, "bold")
            )

        # =================================
        # ZOOMIES SPEED LINES
        # =================================

        if self.state == CatState.ZOOMIES:

            count = (
                self.anim
                .get_zoom_speed_lines()
            )

            for i in range(count):

                self.canvas.create_line(
                    10,
                    40 + i * 20,
                    35,
                    40 + i * 20,
                    fill="white",
                    width=2
                )

            for i in range(3):

                self.canvas.create_oval(
                    160 + i * 10,
                    40 + i * 8,
                    165 + i * 10,
                    45 + i * 8,
                    fill="white",
                    outline=""
                )

        # =================================
        # TOYS
        # =================================

        for toy in self.toy_manager.get_toys():
            self.canvas.create_oval(
                toy.x, toy.y,
                toy.x + toy.size,
                toy.y + toy.size,
                fill="red",
                outline=""
            )

        # =================================
        # MOOD LABEL
        # =================================

        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT - 15,
            text=f"{self.state.value} | {self.mood}",
            fill="white",
            font=("Arial", 10)
        )

        self.draw_speech()

    # =====================================
    # MAIN UPDATE LOOP
    # =====================================

    def update(self):

        self.anim.update()

        self.logic_update()

        self.draw_cat()

        # If hiding is enabled and hidden, move the window off-screen; otherwise position at cat coords
        if ENABLE_HIDING and self.hidden:
            screen_h = self.root.winfo_screenheight()
            # position off-screen below the visible area
            self.root.geometry(
                f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}" +
                f"+{int(self.cat_x)}+{int(screen_h + 300)}"
            )
        else:
            self.root.geometry(
                f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}" +
                f"+{int(self.cat_x)}+{int(self.cat_y)}"
            )

        self.root.after(
            int(1000 / FPS),
            self.update
        )