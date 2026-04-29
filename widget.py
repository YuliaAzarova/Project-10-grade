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

        current_delta = delta_time
        if sort in ["Сортировка Шелла", "Сортировка расческой", "Шейкерная сортировка"]:
            current_delta = delta_time * 3
        elif sort == "Блинная сортировка":
            current_delta = delta_time * 2

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
            gap = ind
            start_index = i % gap
            for k in range(start_index, len(self.bars), gap):
                self.bars[k]["color"].rgba = (1, 0.3, 0.3, 1)
            bar1, bar2 = self.bars[i], self.bars[j]
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



        elif sort == "Блинная сортировка":
            for k in range(ind + 1):
                self.bars[k]["color"].rgba = (1, 0.3, 0.3, 1)
            bar1, bar2 = self.bars[i], self.bars[j]
            bar1["color"].rgba = (0.3, 1, 0.3, 1)
            bar2["color"].rgba = (0.3, 1, 0.3, 1)
            reset_i, reset_j = 0, len(self.bars) - 1

        total_step_time = duration + current_delta

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
            total_step_time
        )

        self.bars[i], self.bars[j] = self.bars[j], self.bars[i]
        self.values[i], self.values[j] = self.values[j], self.values[i]
        Clock.schedule_once(lambda dt: setattr(self, "busy", False), duration)
        self.busy = True

    def animate(self, swaps, sort, index=0, duration=0.3, delta_time=0.03):
        if not self.animating or index >= len(swaps):
            if index >= len(swaps):
                self.animating = False
            return

        current_duration = duration
        current_delta = delta_time

        if sort in ["Сортировка расческой", "Сортировка Шелла"]:
            current_duration = 0.7
            current_delta = 0.5
            next_call_delay = current_duration + (current_delta * 3)
        elif sort == "Блинная сортировка":
            current_duration = 0.5
            current_delta = 0.3
            next_call_delay = current_duration + (current_delta * 2)
        else:
            next_call_delay = current_duration + current_delta

        swap = swaps[index]
        i, j = swap[0], swap[1]

        if len(swap) == 4:
            self.animation(i, j, sort, current_delta, left=swap[2], right=swap[3], duration=current_duration)
        elif len(swap) == 3:
            self.animation(i, j, sort, current_delta, ind=swap[2], duration=current_duration)
        else:
            self.animation(i, j, sort, current_delta, duration=current_duration)

        self.anim_event = Clock.schedule_once(
            lambda dt: self.animate(swaps, sort, index + 1, duration, delta_time),
            next_call_delay
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