import time


class ReminderManager:

    def __init__(self):

        # =========================
        # WATER
        # =========================

        self.water_interval = 60 * 60
        self.last_water = time.time()

        # =========================
        # STRETCH
        # =========================

        self.stretch_interval = 45 * 60
        self.last_stretch = time.time()

        # =========================
        # POMODORO
        # =========================

        self.work_minutes = 25
        self.break_minutes = 5
        self.long_break_minutes = 15

        self.running = False
        self.on_break = False

        self.session_start = 0

        self.pomodoro_count = 0

        # =========================
        # EVENT QUEUE
        # =========================

        self.pending_events = []

    # =====================================
    # WATER
    # =====================================

    def should_drink_water(self):

        return (
            time.time() - self.last_water
            >= self.water_interval
        )

    def water_done(self):

        self.last_water = time.time()

    # =====================================
    # STRETCH
    # =====================================

    def should_stretch(self):

        return (
            time.time() - self.last_stretch
            >= self.stretch_interval
        )

    def stretch_done(self):

        self.last_stretch = time.time()

    # =====================================
    # POMODORO
    # =====================================

    def start_pomodoro(self):

        self.running = True
        self.on_break = False

        self.session_start = time.time()

        self.pending_events.append(
            "work_started"
        )

    def stop_pomodoro(self):

        self.running = False

        self.pending_events.append(
            "pomodoro_stopped"
        )

    def reset_pomodoro(self):

        self.running = False
        self.on_break = False

        self.pomodoro_count = 0
        self.session_start = 0

        self.pending_events.append(
            "pomodoro_reset"
        )

    # =====================================
    # MAIN UPDATE
    # =====================================

    def update(self):

        self.check_reminders()

        if not self.running:
            return

        elapsed = (
            time.time()
            - self.session_start
        )

        # -------------------------
        # WORK SESSION
        # -------------------------

        if not self.on_break:

            if elapsed >= (
                self.work_minutes * 60
            ):

                self.on_break = True

                self.session_start = (
                    time.time()
                )

                self.pomodoro_count += 1

                if (
                    self.pomodoro_count % 4
                    == 0
                ):

                    self.pending_events.append(
                        "long_break"
                    )

                else:

                    self.pending_events.append(
                        "break"
                    )

        # -------------------------
        # BREAK SESSION
        # -------------------------

        else:

            break_length = (

                self.long_break_minutes

                if self.pomodoro_count % 4 == 0

                else self.break_minutes

            )

            if elapsed >= (
                break_length * 60
            ):

                self.on_break = False

                self.session_start = (
                    time.time()
                )

                self.pending_events.append(
                    "work"
                )

    # =====================================
    # REMINDER CHECKS
    # =====================================

    def check_reminders(self):

        if self.should_drink_water():

            self.water_done()

            self.pending_events.append(
                "water"
            )

        if self.should_stretch():

            self.stretch_done()

            self.pending_events.append(
                "stretch"
            )

    # =====================================
    # EVENT SYSTEM
    # =====================================

    def has_events(self):

        return (
            len(self.pending_events)
            > 0
        )

    def get_next_event(self):

        if not self.pending_events:
            return None

        return self.pending_events.pop(0)

    # =====================================
    # STATUS
    # =====================================

    def get_status(self):

        if not self.running:
            return "stopped"

        if self.on_break:
            return "break"

        return "work"

    def is_running(self):

        return self.running

    def is_on_break(self):

        return self.on_break

    # =====================================
    # TIMER
    # =====================================

    def get_remaining_seconds(self):

        if not self.running:
            return 0

        elapsed = (
            time.time()
            - self.session_start
        )

        if self.on_break:

            target = (

                self.long_break_minutes * 60

                if self.pomodoro_count % 4 == 0

                else self.break_minutes * 60

            )

        else:

            target = (
                self.work_minutes * 60
            )

        return max(
            0,
            int(target - elapsed)
        )

    def get_timer_text(self):

        seconds = (
            self.get_remaining_seconds()
        )

        mins = seconds // 60
        secs = seconds % 60

        return (
            f"{mins:02}:{secs:02}"
        )

    # =====================================
    # STATS
    # =====================================

    def get_pomodoro_count(self):

        return self.pomodoro_count

    # =====================================
    # DEBUG
    # =====================================

    def get_debug_info(self):

        return {

            "running":
                self.running,

            "on_break":
                self.on_break,

            "pomodoros":
                self.pomodoro_count,

            "status":
                self.get_status(),

            "remaining":
                self.get_timer_text(),

            "queued_events":
                len(
                    self.pending_events
                )
        }