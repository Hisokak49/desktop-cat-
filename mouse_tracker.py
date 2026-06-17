from pynput import mouse
import threading
import time
import math


class MouseTracker:

    def __init__(self):

        self.x = 0
        self.y = 0

        self.prev_x = 0
        self.prev_y = 0

        self.speed = 0

        self.left_click = False
        self.right_click = False

        self.scroll_count = 0

        self.dragging = False

        self.total_clicks = 0

        self.last_activity = time.time()

        self.last_move_time = time.time()

        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )

    # ---------------------
    # START
    # ---------------------

    def start(self):

        threading.Thread(
            target=self.listener.start,
            daemon=True
        ).start()

    # ---------------------
    # MOVE
    # ---------------------

    def on_move(self, x, y):

        dx = x - self.x
        dy = y - self.y

        self.speed = math.sqrt(
            dx * dx +
            dy * dy
        )

        self.prev_x = self.x
        self.prev_y = self.y

        self.x = x
        self.y = y

        self.last_move_time = time.time()

        self.last_activity = time.time()

        if self.left_click:
            self.dragging = True
        else:
            self.dragging = False

    # ---------------------
    # CLICK
    # ---------------------

    def on_click(
        self,
        x,
        y,
        button,
        pressed
    ):

        if button == mouse.Button.left:

            self.left_click = pressed

        if button == mouse.Button.right:

            self.right_click = pressed

        if pressed:

            self.total_clicks += 1

        self.last_activity = time.time()

    # ---------------------
    # SCROLL
    # ---------------------

    def on_scroll(
        self,
        x,
        y,
        dx,
        dy
    ):

        self.scroll_count += 1

        self.last_activity = time.time()

    # ---------------------
    # POSITION
    # ---------------------

    def get_position(self):

        return self.x, self.y

    def get_previous_position(self):

        return (
            self.prev_x,
            self.prev_y
        )

    # ---------------------
    # SPEED
    # ---------------------

    def get_speed(self):

        return self.speed

    def is_mouse_moving_fast(self):

        return self.speed > 50

    def is_mouse_moving(self):

        return (
            time.time()
            - self.last_move_time
            < 0.2
        )

    # ---------------------
    # CLICKS
    # ---------------------

    def is_left_clicking(self):

        return self.left_click

    def is_right_clicking(self):

        return self.right_click

    def get_total_clicks(self):

        return self.total_clicks

    # ---------------------
    # DRAGGING
    # ---------------------

    def is_dragging(self):

        return self.dragging

    # ---------------------
    # SCROLLING
    # ---------------------

    def get_scroll_count(self):

        return self.scroll_count

    # ---------------------
    # IDLE
    # ---------------------

    def get_idle_time(self):

        return (
            time.time()
            - self.last_activity
        )

    def is_afk(self):

        return (
            self.get_idle_time()
            > 60
        )

    # ---------------------
    # CHASE MODE
    # ---------------------

    def should_chase(self):

        return (
            self.speed > 80
        )

    # ---------------------
    # DEBUG
    # ---------------------

    def get_stats(self):

        return {

            "x": self.x,
            "y": self.y,

            "speed": round(
                self.speed,
                2
            ),

            "left_click":
                self.left_click,

            "right_click":
                self.right_click,

            "dragging":
                self.dragging,

            "clicks":
                self.total_clicks,

            "scrolls":
                self.scroll_count,

            "idle_time":
                round(
                    self.get_idle_time(),
                    2
                )
        }