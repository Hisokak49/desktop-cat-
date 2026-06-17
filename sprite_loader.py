class PixelSprite:

    def __init__(
        self,
        frames,
        color="#ff9f1c"
    ):

        self.frames = frames

        self.color = color

    # =====================================
    # FRAMES
    # =====================================

    def get_frame(
        self,
        frame_index=0
    ):

        if not self.frames:
            return []

        return self.frames[
            frame_index % len(self.frames)
        ]

    def frame_count(self):

        return len(self.frames)

    # =====================================
    # DRAW
    # =====================================

    def draw(
        self,
        canvas,
        x,
        y,
        frame_index=0,
        scale=6
    ):

        frame = self.get_frame(
            frame_index
        )

        for row_i, row in enumerate(frame):

            for col_i, pixel in enumerate(row):

                if pixel != "1":
                    continue

                px = (
                    x +
                    col_i * scale
                )

                py = (
                    y +
                    row_i * scale
                )

                canvas.create_rectangle(
                    px,
                    py,
                    px + scale,
                    py + scale,
                    fill=self.color,
                    outline=""
                )


# =====================================
# SPRITE MANAGER
# =====================================

class SpriteManager:

    def __init__(self):

        self.sprites = {}

    # =====================================
    # REGISTER
    # =====================================

    def register(
        self,
        name,
        frames,
        color="#ff9f1c"
    ):

        self.sprites[name] = (
            PixelSprite(
                frames,
                color
            )
        )

    # =====================================
    # ACCESS
    # =====================================

    def get(self, name):

        return self.sprites.get(
            name
        )

    def exists(self, name):

        return (
            name
            in self.sprites
        )

    def names(self):

        return list(
            self.sprites.keys()
        )

    # =====================================
    # DRAW
    # =====================================

    def draw(
        self,
        name,
        canvas,
        x,
        y,
        frame_index=0,
        scale=6
    ):

        sprite = self.get(name)

        if sprite is None:
            return

        sprite.draw(
            canvas,
            x,
            y,
            frame_index,
            scale
        )