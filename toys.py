import random
import time
import math


# =====================================
# TOY
# =====================================

class Toy:

    def __init__(
        self,
        toy_type,
        x,
        y
    ):

        self.type = toy_type

        self.x = x
        self.y = y

        self.spawn_time = time.time()

        self.lifetime = random.randint(
            25,
            45
        )

        self.size = random.randint(
            8,
            14
        )

        self.vx = random.uniform(
            -2,
            2
        )

        self.vy = random.uniform(
            -2,
            2
        )

        self.rotation = 0

    # =====================================
    # UPDATE
    # =====================================

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vx *= 0.98
        self.vy *= 0.98

        self.rotation += 3

    # =====================================
    # AGE
    # =====================================

    def age(self):

        return (
            time.time()
            - self.spawn_time
        )

    # =====================================
    # EXPIRED
    # =====================================

    def expired(self):

        return (
            self.age()
            > self.lifetime
        )

    # =====================================
    # DISTANCE
    # =====================================

    def distance_to(
        self,
        x,
        y
    ):

        return math.hypot(
            self.x - x,
            self.y - y
        )


# =====================================
# TOY MANAGER
# =====================================

class ToyManager:

    def __init__(self):

        self.toys = []

        self.last_spawn = time.time()

        self.spawn_interval = 20

        self.play_score = 0

        self.total_toys_spawned = 0
        self.total_toys_caught = 0

        self.pending_events = []

        self.types = [

            "mouse",
            "fish",
            "ball",
            "feather",
            "yarn"

        ]

    # =====================================
    # UPDATE
    # =====================================

    def update(self):

        now = time.time()

        # -------------------------
        # AUTO SPAWN
        # -------------------------

        if (
            now - self.last_spawn
            >= self.spawn_interval
        ):

            self.spawn_random_toy()

            self.last_spawn = now

        # -------------------------
        # UPDATE TOYS
        # -------------------------

        alive = []

        for toy in self.toys:

            toy.update()

            if not toy.expired():

                alive.append(toy)

            else:

                self.pending_events.append(
                    "toy_expired"
                )

        self.toys = alive

    # =====================================
    # SPAWN
    # =====================================

    def spawn_random_toy(self):

        toy = Toy(

            random.choice(
                self.types
            ),

            random.randint(
                40,
                170
            ),

            random.randint(
                50,
                130
            )

        )

        self.toys.append(toy)

        self.total_toys_spawned += 1

        self.pending_events.append(
            "toy_spawned"
        )

        return toy

    def spawn_toy(
        self,
        toy_type,
        x,
        y
    ):

        toy = Toy(
            toy_type,
            x,
            y
        )

        self.toys.append(toy)

        self.total_toys_spawned += 1

        self.pending_events.append(
            "toy_spawned"
        )

        return toy

    # =====================================
    # CHASE LOGIC
    # =====================================

    def has_toys(self):

        return len(self.toys) > 0

    def get_nearest_toy(
        self,
        cat_x,
        cat_y
    ):

        if not self.toys:
            return None

        return min(

            self.toys,

            key=lambda toy:

            toy.distance_to(
                cat_x,
                cat_y
            )

        )

    def toy_in_range(
        self,
        cat_x,
        cat_y,
        distance=25
    ):

        toy = self.get_nearest_toy(
            cat_x,
            cat_y
        )

        if not toy:
            return None

        if (

            toy.distance_to(
                cat_x,
                cat_y
            )

            <= distance

        ):

            return toy

        return None

    # =====================================
    # CATCH
    # =====================================

    def catch_toy(self, toy):

        if toy is None:
            return False

        if toy not in self.toys:
            return False

        self.toys.remove(toy)

        self.play_score += 1

        self.total_toys_caught += 1

        self.pending_events.append(
            "toy_caught"
        )

        return True

    # =====================================
    # EVENTS
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
    # ACCESS
    # =====================================

    def get_toys(self):

        return self.toys

    def toy_count(self):

        return len(self.toys)

    def clear_all(self):

        self.toys.clear()

    # =====================================
    # STATS
    # =====================================

    def get_play_score(self):

        return self.play_score

    def get_total_spawned(self):

        return self.total_toys_spawned

    def get_total_caught(self):

        return self.total_toys_caught

    # =====================================
    # DEBUG
    # =====================================

    def get_debug_info(self):

        return {

            "active_toys":
                len(self.toys),

            "score":
                self.play_score,

            "spawned":
                self.total_toys_spawned,

            "caught":
                self.total_toys_caught,

            "events":
                len(
                    self.pending_events
                ),

            "next_spawn":

                round(

                    max(

                        0,

                        self.spawn_interval

                        -

                        (
                            time.time()
                            -
                            self.last_spawn
                        )

                    ),

                    1

                )
        }