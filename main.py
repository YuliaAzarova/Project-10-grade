from pygments.styles.dracula import background
from kivy.config import Config
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '900')

import sorts
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from pygments.styles.dracula import background
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
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

        self.anim_event = None
        self.animating = False

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

        bar1["color"].rgba = (1, 0.3, 0.3, 1)
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


class BarGraphApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # выбор сортировки
        self.spinner = Spinner(
            text='Сортировка пузырьком',
            values=('Сортировка пузырьком', 'Сортировка слиянием', 'Сортировка вставками'),
            size_hint=(0.6, None),
            size=(1, 100),
            pos_hint={'center_x': 0.3, 'center_y': 0.5}
        )
        self.spinner.bind(text=self.on_spinner_select)
        layout.add_widget(self.spinner)



        # название выбранной сортировки
        self.status_label = Label(text='Сортировка пузырьком',
                            size_hint=(1, None),
                            height=150,
                            font_size='35sp',
                            color="#E0FFFF")
        layout.add_widget(self.status_label)

        self.data = [85, 40, 95, 60, 20, 10, 15, 5, 50, 100]
        self.bars_widget = BarsWidget(self.data)
        layout.add_widget(self.bars_widget)

        # кнопки
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.buttons_container = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.8)

        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=20, size_hint_y=2)
        self.button_sort = Button(text='Запустить сортировку',
                        font_size='15sp',
                        size_hint=(1, None),
                        on_press=self.on_press_sort,
                        background_color="#1E90FF")
        self.button_steps = Button(text='Запустить шаги',
                         font_size='15sp',
                         size_hint=(1, None),
                        on_press=self.on_press_steps,
                        background_color="#00BFFF") # синий
        buttons_layout.add_widget(self.button_sort)
        buttons_layout.add_widget(self.button_steps)

        self.buttons_container.add_widget(buttons_layout)
        self.scroll_view.add_widget(self.buttons_container)
        layout.add_widget(self.scroll_view)



        self.animation_steps = [] # шаги запоминать
        self.anim_index = 0 # считать шаги
        self.anim_event = None # чекать



        self.steps_count = 0
        self.steps = [(i, j) for i in range(len(self.data)) for j in range(0, i) ]
        return layout

    def on_spinner_select(self, spinner, value):
        self.status_label.text = value
# +



    def on_press_sort(self, instance):
        if instance.text == "Сбросить сортировку":
            self.bars_widget.reset()
            self.anim_index = 0

            instance.text = "Запустить сортировку"


            if hasattr(self, 'st_forward'):
                self.st_forward.disabled = False
                self.st_back.disabled = True
            return


        self.bars_widget.animating = True

        if self.status_label.text == "Сортировка пузырьком":
            self.bars_widget.animating = True
            self.animation_steps = sorts.bubble_sort_steps(self.bars_widget.values.copy())
        elif self.status_label.text == "Сортировка вставками":
            self.bars_widget.animating = True
            self.animation_steps = sorts.insert_sort_steps(self.bars_widget.values.copy())
        elif self.status_label.text == "Сортировка слиянием":
            pass

        self.bars_widget.animate(self.animation_steps)
        instance.text = "Сбросить сортировку"
        if hasattr(self, 'st_forward'):
            self.st_forward.disabled = True
            self.st_back.disabled = True


    def on_press_steps(self, instance):
        self.anim_index = 0
        self.bars_widget.animating = False
        self.st_back = Button(text='Шаг назад',
                            font_size='15sp',
                                size_hint=(1, 0.9),
                                on_press=self.on_press_s_back,
                                 background_color="#4169E1",
                                      disabled=True)
        self.st_forward = Button(text='Шаг вперед',
                             font_size='15sp',
                             size_hint=(1, 0.9),
                                height=50,
                            on_press=self.on_press_s_forward,
                                    background_color="#4169E1")
        if self.button_sort.text == "Сбросить сортировку":
            self.st_forward.disabled= True
            self.st_back.disabled = False


        button_layout = BoxLayout(orientation='horizontal',
                                      spacing=20)

        button_layout.add_widget(self.st_back)
        button_layout.add_widget(self.st_forward)
        self.buttons_container.add_widget(button_layout)

        instance.text = "Идет сортировка"
        instance.disabled = True

        self.anim_index = 0
        if self.status_label.text == "Сортировка пузырьком":
            self.animation_steps = sorts.bubble_sort_steps(self.bars_widget.values.copy())
        elif self.status_label.text == "Сортировка вставками":
            self.animation_steps = sorts.insert_sort_steps(self.bars_widget.values.copy())




    def on_press_s_back(self, instance):
        if getattr(self.bars_widget, "busy", False):
            return

        self.anim_index -= 1
        swap = self.animation_steps[self.anim_index]
        self.bars_widget.step(swap)

        self.st_forward.disabled = False
        self.st_forward.text = "Шаг вперед"
        self.button_sort.text = "Запустить сортировку"

        if self.anim_index <= 0:
            instance.disabled = True
            return


    def on_press_s_forward(self, instance):
        if getattr(self.bars_widget, "busy", False):
            return

        self.st_back.disabled = False
        swap = self.animation_steps[self.anim_index]
        self.anim_index += 1
        self.bars_widget.step(swap)

        if self.anim_index >= len(self.animation_steps):
            instance.disabled = True
            self.button_sort.text = "Сбросить сортировку"
            return

def smth():
    pass


if __name__ == '__main__':
    BarGraphApp().run()