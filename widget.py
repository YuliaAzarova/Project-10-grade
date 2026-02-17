from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.animation import Animation
from kivy.clock import Clock


class BarsWidget(Widget):
    def __init__(self, values, **kwargs):
        super().__init__(**kwargs)
        self.values = values
        self.original_values = values.copy()
        self.bars = []
        self.history = []

        self.bar_width = 70
        self.spacing = 10
        self.max_value = max(values)

        self.bind(size=self.draw_bars)

        self.anim_index = 0

        self.anim_event = None
        self.animating = False
        self.busy = False

    def draw_bars(self, *args):
        self.canvas.clear()
        self.bars.clear()

        height_scale = (self.height) / self.max_value * 1.4
        total_width = (len(self.values) * self.bar_width +
                       (len(self.values) - 1) * self.spacing)
        start_x = self.x + (self.width - total_width) / 2
        self.y = 430

        with self.canvas:
            for i, value in enumerate(self.values):
                color = Color(1, .5, 0, 1)
                rect = Rectangle(
                    pos=(start_x + i * (self.bar_width + self.spacing), self.y),
                    size=(self.bar_width, value * height_scale)
                )
                self.bars.append({
                    "rect": rect,
                    "color": color
                })

    def step(self, swap):
        if not swap:
            return
        i, j = swap
        self.animation(i, j)

    def reset_colors(self, i, j):
        if i < len(self.bars) and j < len(self.bars):
            self.bars[i]["color"].rgba = (1, .5, 0, 1)
            self.bars[j]["color"].rgba = (1, .5, 0, 1)

    def animation(self, i, j, duration=0.27):
        bar1 = self.bars[i]
        bar2 = self.bars[j]

        bar1["color"].rgba = (0.3, 1, 0.3, 1)
        bar2["color"].rgba = (1, 0.3, 0.3, 1)

        rect1 = bar1["rect"]
        rect2 = bar2["rect"]

        x1 = rect1.pos[0]
        x2 = rect2.pos[0]

        y1 = rect1.pos[1]
        y2 = rect2.pos[1]

        anim1 = Animation(pos=(x2, y1), duration=duration)
        anim2 = Animation(pos=(x1, y2), duration=duration)

        anim1.start(rect1)
        anim2.start(rect2)

        Clock.schedule_once(
        lambda dt: self.reset_colors(i, j),
            0.3)

        self.bars[i], self.bars[j] = self.bars[j], self.bars[i]
        self.values[i], self.values[j] = self.values[j], self.values[i]
        Clock.schedule_once(lambda dt: setattr(self, "busy", False), duration)
        self.busy = True

    def animate(self, swaps, index=0):
        if not self.animating:
            return

        if index == len(swaps):
            return

        i, j = swaps[index]
        self.animation(i, j)

        self.anim_event = Clock.schedule_once(
            lambda dt: self.animate(swaps, index + 1),
            0.3
        )

    def reset(self):
        self.animating = False

        if self.anim_event:
            self.anim_event.cancel()
            self.anim_event = None

        for rect in self.bars:
            Animation.cancel_all(rect["rect"])
        self.values = self.original_values.copy()
        self.draw_bars()