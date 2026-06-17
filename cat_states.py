from enum import Enum


class CatState(Enum):

    # =========================
    # NORMAL
    # =========================

    IDLE = "idle"

    FOLLOW = "follow"

    WATCH = "watch"

    THINKING = "thinking"

    # =========================
    # PRODUCTIVITY
    # =========================

    TYPING = "typing"

    POMODORO = "pomodoro"

    BREAK = "break"

    # =========================
    # PLAY
    # =========================

    PLAY = "play"

    ZOOMIES = "zoomies"

    # =========================
    # REST
    # =========================

    SLEEP = "sleep"

    STRETCH = "stretch"