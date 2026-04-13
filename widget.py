from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.animation import Animation
from kivy.clock import Clock


class BarsWidget(Widget):
    def __init__(self, values, **kwargs):
        super().__init__(**kwargs)
        self.values = values.copy()
        self.original_values = values.copy()
        self.bars = []
        self.history = []

        self.bar_width = 70
        self.spacing = 10
        self.max_value = max(values)

        self.bind(size=self.draw_bars)

        self.anim_index = 0
        self.extra_ind = 0
        self.duration = 0.3

        self.anim_event = None
        self.animating = False
        self.busy = False

    def draw_bars(self, *args):
        self.canvas.clear()
        self.bars.clear()

        height_scale = (self.height) / self.max_value * 1.17
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
                    "color": color,
                    "value": value
                })

    def step(self, swap, sort):
        if not swap:
            return
        i, j = swap[0], swap[1]
        if len(swap) > 3:
            self.animation(i, j, sort, left=swap[2], right=swap[3], delta_time=0.03)
        elif len(swap) > 2:
            self.animation(i, j, sort, ind=swap[2], delta_time=0.03)
        else:
            self.animation(i, j, sort, delta_time=0.03)

    def reset_colors(self, i, j):
        if i < len(self.bars) and j < len(self.bars):
            for k in range(i, j+1):
                self.bars[k]["color"].rgba = (1, .5, 0, 1)

    def animation(self, i, j, sort, delta_time, left=None, right=None, ind=None, duration=None):
        if not duration:
            duration = self.duration
        if sort == "Сортировка пузырьком":
            bar1 = self.bars[i]
            bar2 = self.bars[j]
            bar1["color"].rgba = (0.3, 1, 0.3, 1)
            bar2["color"].rgba = (1, 0.3, 0.3, 1)
            reset_i, reset_j = i, j

        elif sort == "Сортировка вставками":
            if j > self.extra_ind:
                self.extra_ind = j
            bars = self.bars.copy()
            for k in range( len(bars[:self.extra_ind]) + 1 ):
                bars[k]["color"].rgba = (0.3, 1, 0.3, 1)
            reset_i, reset_j = 0, len(bars)-1
            bars[j]["color"].rgba = (1, 0.3, 0.3, 1)
            bar1 = bars[i]
            bar2 = bars[j]

        elif sort == "Сортировка слиянием":
            for k in range(left, right):
                self.bars[k]["color"].rgba = (1, 0.3, 0.3, 1)
            bar1 = self.bars[i]
            bar2 = self.bars[j]
            bar2["color"].rgba = (0.3, 1, 0.3, 1)
            reset_i, reset_j = 0, len(self.bars)-1

        elif sort == "Быстрая сортировка":
            bar1 = self.bars[i]
            bar2 = self.bars[j]
            bar1["color"].rgba = (0.3, 1, 0.3, 1)
            bar2["color"].rgba = (1, 0.3, 0.3, 1)
            self.bars[ind]["color"].rgba = (0.6, 0.2, 1, 1)
            reset_i, reset_j = min(i, j, ind), max(i, j, ind)

        elif sort == "Сортировка выбором":
            for k in range(ind):
                self.bars[k]["color"].rgba = (1, 0.3, 0.3, 1)
            bar1 = self.bars[i]
            bar2 = self.bars[j]
            bar1["color"].rgba = (0.3, 1, 0.3, 1)
            reset_i, reset_j = 0, len(self.bars)-1

        elif sort == "Сортировка расческой":
            bar1 = self.bars[i]
            bar2 = self.bars[j]
            if left == 1:
                right = 0
            for k in range(right, len(self.bars), left):
                self.bars[k]["color"].rgba = (1, 0.3, 0.3, 1)
            delta_time *= 3
            bar1["color"].rgba = (0.3, 1, 0.3, 1)
            bar2["color"].rgba = (0.3, 1, 0.3, 1)
            reset_i, reset_j = 0, len(self.bars)-1

        elif sort == "Сортировка Шелла":
            bar1 = self.bars[i]
            bar2 = self.bars[j]
            for k in range(0, len(self.bars), ind):
                self.bars[k]["color"].rgba = (1, 0.3, 0.3, 1)
            delta_time *= 3
            bar1["color"].rgba = (0.3, 1, 0.3, 1)
            bar2["color"].rgba = (0.3, 1, 0.3, 1)
            reset_i, reset_j = 0, len(self.bars) - 1

        elif sort == "Шейкерная сортировка":
            bar1 = self.bars[i]
            bar2 = self.bars[j]
            delta_time *= 3
            bar1["color"].rgba = (0.3, 1, 0.3, 1)
            bar2["color"].rgba = (1, 0.3, 0.3, 1)
            if ind == 0:
                reset_i, reset_j = i, j
            else:
                reset_i, reset_j = j, i

        elif sort == "Гномья сортировка":
            if j > self.extra_ind:
                self.extra_ind = j
            bars = self.bars.copy()
            for k in range( len(bars[:self.extra_ind]) + 1 ):
                bars[k]["color"].rgba = (0.3, 1, 0.3, 1)
            reset_i, reset_j = 0, len(bars)-1
            bars[j]["color"].rgba = (1, 0.3, 0.3, 1)
            bar1 = bars[i]
            bar2 = bars[j]

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
        lambda dt: self.reset_colors(reset_i, reset_j),
            duration + delta_time)

        self.bars[i], self.bars[j] = self.bars[j], self.bars[i]
        self.values[i], self.values[j] = self.values[j], self.values[i]
        Clock.schedule_once(lambda dt: setattr(self, "busy", False), duration)
        self.busy = True

    def animate(self, swaps, sort, index=0, duration=0.3, delta_time=0.03):
        if not self.animating:
            return

        if index == len(swaps):
            return

        i, j = swaps[index][0], swaps[index][1]
        if sort == "Сортировка расческой" or sort == "Сортировка Шелла":
            duration = 1
            delta_time = 0.5
        if len(swaps[index]) == 4:
            self.animation(i, j, sort, delta_time=delta_time, left=swaps[index][2], right=swaps[index][3])
        elif len(swaps[index]) == 3:
            self.animation(i, j, sort, delta_time=delta_time, ind=swaps[index][2])
        else:
            self.animation(i, j, sort, delta_time=delta_time)

        self.anim_event = Clock.schedule_once(
            lambda dt: self.animate(swaps, sort, index + 1),
            duration+delta_time
        )


    def reset(self):
        self.extra_ind = 0
        self.animating = False

        if self.anim_event:
            self.anim_event.cancel()
            self.anim_event = None

        for rect in self.bars:
            Animation.cancel_all(rect["rect"])
        self.values = self.original_values.copy()
        self.draw_bars()