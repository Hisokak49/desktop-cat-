# ==========================================
# WINDOW
# ==========================================

WINDOW_WIDTH = 220
WINDOW_HEIGHT = 180

FPS = 30

ALWAYS_ON_TOP = True

TRANSPARENT_COLOR = "green"

# ==========================================
# CAT
# ==========================================

CAT_NAME = "Mochi"

CAT_COLOR = "#ff9f1c"
CAT_OUTLINE = "#cc7a00"

CAT_EYE_COLOR = "lime"

PIXEL_SCALE = 6

# ==========================================
# START POSITION
# ==========================================

CAT_START_MIN_X = 100
CAT_START_MAX_X = 1200

CAT_START_MIN_Y = 100
CAT_START_MAX_Y = 700

# ==========================================
# FOLLOWING
# ==========================================

FOLLOW_SPEED = 0.04

WATCH_DISTANCE = 150

WAKE_DISTANCE = 40

# ==========================================
# RUNNING / ZOOMIES
# ==========================================

RUN_SPEED = 0.08

ZOOMIES_SPEED = 12

ZOOMIES_MIN_SECONDS = 30
ZOOMIES_MAX_SECONDS = 90

ZOOMIES_DURATION = 5

ENABLE_ZOOMIES = True

# ==========================================
# SLEEP
# ==========================================

SLEEP_AFTER_SECONDS = 30

SLEEP_FLOAT_SPEED = 0.05
SLEEP_FLOAT_AMOUNT = 3

# ==========================================
# BLINK
# ==========================================

BLINK_MIN_SECONDS = 2
BLINK_MAX_SECONDS = 6

BLINK_DURATION = 0.15

# ==========================================
# BODY
# ==========================================

BREATH_SPEED = 0.08
BREATH_AMOUNT = 2

BODY_SQUASH_SPEED = 0.10
BODY_SQUASH_AMOUNT = 2

# ==========================================
# EARS
# ==========================================

EAR_TWITCH_SPEED = 0.15
EAR_TWITCH_AMOUNT = 3

# ==========================================
# TAIL
# ==========================================

TAIL_SWING_SPEED = 0.12
TAIL_SWING_AMOUNT = 3

TAIL_HEIGHT_SPEED = 0.12
TAIL_HEIGHT_AMOUNT = 8

# ==========================================
# WHISKERS
# ==========================================

WHISKER_SPEED = 0.25
WHISKER_AMOUNT = 2

# ==========================================
# HEAD
# ==========================================

HEAD_TILT_SPEED = 0.04
HEAD_TILT_AMOUNT = 2

# ==========================================
# PAWS
# ==========================================

TYPING_PAW_SPEED = 4

WALK_BOUNCE_SPEED = 10

# ==========================================
# THOUGHTS
# ==========================================

THOUGHT_INTERVAL = 20

THOUGHT_CHANCE = 0.25

THOUGHTS = [

    "feed me",
    "hello human",
    "nap time",
    "mouse detected",
    "i love bugs",
    "keep coding",
    "where fish",
    "pet me",
    "tail.exe running",
    "what is python"

]

# ==========================================
# SPEECH
# ==========================================

ENABLE_SPEECH = True

MAX_BUBBLE_TIME = 4

# ==========================================
# TOYS
# ==========================================

ENABLE_TOYS = True

TOY_SPAWN_INTERVAL = 20

TOY_LIFETIME_MIN = 25
TOY_LIFETIME_MAX = 45

PLAY_DURATION = 10

# ==========================================
# PRODUCTIVITY
# ==========================================

POMODORO_ENABLED = True

WORK_MINUTES = 25

BREAK_MINUTES = 5

LONG_BREAK_MINUTES = 15

# ==========================================
# REMINDERS
# ==========================================

ENABLE_WATER_REMINDER = True

WATER_INTERVAL = 60 * 60

ENABLE_STRETCH_REMINDER = True

STRETCH_INTERVAL = 45 * 60

# ==========================================
# CODING ASSISTANT
# ==========================================

ENABLE_CODING_MODE = True

ENABLE_TYPING_REACTIONS = True

ENABLE_VSCODE_DETECTION = False

# ==========================================
# AUDIO
# ==========================================

ENABLE_MEOWS = False

MEOW_VOLUME = 0.5

# ==========================================
# DEBUG
# ==========================================

DEBUG_MODE = False

SHOW_STATE = True
SHOW_MOOD = True
SHOW_FPS = False

SHOW_TOY_COUNT = True
SHOW_POMODORO = True
SHOW_PLAY_SCORE = True

# ==========================================
# AUTONOMY / ROAMING
# ==========================================

# Wander (when following mouse)
WANDER_X_RANGE = 80
WANDER_Y_RANGE = 50
WANDER_MIN_SECONDS = 1.5
WANDER_MAX_SECONDS = 5.0

# Roaming behavior
ROAM_NEXT_MIN = 3.0
ROAM_NEXT_MAX = 9.0
ROAM_ACTIVE_MIN = 2.0
ROAM_ACTIVE_MAX = 6.0
ROAM_PROBABILITY = 0.75

# Hide / disappear behavior
HIDE_MOUSE_THRESHOLD = 40
UNHIDE_MOUSE_THRESHOLD = 150
HIDE_DURATION_MIN = 3.0
HIDE_DURATION_MAX = 10.0

# Interaction ranges
TOY_CHASE_DISTANCE = 220
TOY_CATCH_DISTANCE = 18
PET_CLICK_RADIUS = 80

# Reaction multipliers
CHASE_SPEED_MULTIPLIER = 1.8

# Disable disappearing by default (set True to re-enable)
ENABLE_HIDING = False

# Smooth motion parameters
SMOOTHING_FACTOR = 0.08
MAX_VELOCITY = 18.0