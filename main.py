from pygments.styles.dracula import background
from kivy.config import Config
from kivy.graphics import Color, Rectangle
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '900')

import sorts
from random import randint
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from widget import BarsWidget
from kivy.uix.spinner import SpinnerOption

class CustomSpinnerOption(SpinnerOption):
    font_name = 'Mulish-Italic-VariableFont_wght.ttf'
    background_normal = ''
    background_color = (0.02, 0.60, 0.75, 1)

class BarGraphApp(App):
    def build(self):
        self.font = 'Mulish-VariableFont_wght.ttf'
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        with layout.canvas.before:
            Color(0.06, 0.09, 0.16, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self.update_rect, pos=self.update_rect)

        self.spinner_values = ('Сортировка пузырьком',
                               'Шейкерная сортировка',
                               'Сортировка вставками',
                               'Сортировка выбором',
                               'Гномья сортировка',
                               'Быстрая сортировка',
                               'Сортировка слиянием',
                               'Сортировка Шелла',
                               'Сортировка расческой',
                               'Случайная сортировка', )
        self.speeds = {'Сортировка пузырьком': 'O(n^2)',
                       'Шейкерная сортировка': 'O(n^2)',
                       'Сортировка вставками': 'O(n^2)',
                       'Сортировка выбором': 'O(n^2)',
                       'Гномья сортировка': 'O(n)',
                       'Быстрая сортировка': 'O(n log n)',
                       'Сортировка слиянием': 'O(n log n)',
                       'Сортировка Шелла': 'O(n^(3/2))',
                       'Сортировка расческой': 'O(n log n)',
                       'Случайная сортировка': 'O(0)'}
        current_value = self.spinner_values[0]

        self.spinner = Spinner(
            text=current_value,
            values=self.spinner_values[1:],
            size_hint=(0.8, 0.5),
            size=(1, 100),
            font_name=self.font,
            font_size='20sp',
            background_normal='',
            background_color=(0.02, 0.50, 0.85, 1),
            option_cls=CustomSpinnerOption,
            pos_hint={'center_x': 0.3, 'center_y': 0.5})
        self.spinner.bind(text=self.on_spinner_select)
        layout.add_widget(self.spinner)



        self.status_label = Label(
            text=f"Сложность сортировки: {self.speeds[self.spinner.text]}",
            size_hint=(1, None),
            height=100,
            font_size='25sp',
            bold=True,
            font_name=self.font,
            color="#38BDF8"
        )
        layout.add_widget(self.status_label)



        diagram_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(1, 1.9))
        self.data = []
        for i in range(10):
            self.data.append(randint(0, 100))
        self.bars_widget = BarsWidget(self.data)
        diagram_layout.add_widget(self.bars_widget)
        layout.add_widget(diagram_layout)



        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=20, size_hint_y=2)

        self.button_sort = Button(text='Запустить сортировку',
                        font_size='15sp',
                        size_hint=(1, None),
                        on_press=self.on_press_sort,
                        font_name=self.font,
                        background_normal='',
                        background_color=(0.02, 0.50, 0.85, 1))
        self.button_shuffle = Button(text='Перемешать',
                        font_size='15sp',
                        size_hint=(1, None),
                        on_press=self.on_press_shuffle,
                        font_name=self.font,
                        background_normal='',
                        background_color=(0.02, 0.50, 0.85, 1))
        buttons_layout.add_widget(self.button_sort)
        buttons_layout.add_widget(self.button_shuffle)



        self.steps_layout = BoxLayout(
            orientation='horizontal',
            spacing=20, size_hint=(1, None))
        self.button_steps = Button(text='Запустить шаги',
                        font_size='15sp',
                        on_press=self.on_press_steps,
                        font_name=self.font,
                        background_normal='',
                        background_color=(0.02, 0.60, 0.75, 1))
        self.steps_layout.add_widget(self.button_steps)
        buttons_layout.add_widget(self.steps_layout)

        layout.add_widget(buttons_layout)



        self.animation_steps = []
        self.anim_index = 0
        self.anim_event = None



        self.steps_count = 0
        self.steps = [(i, j) for i in range(len(self.data)) for j in range(0, i) ]
        return layout



    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def set_animation_steps(self):
        if self.anim_index > 0:
            to_sort = self.bars_widget.values.copy()
        else:
            to_sort = self.bars_widget.original_values.copy()
        if self.spinner.text == "Сортировка пузырьком":
            self.button_shuffle.disabled = False
            self.animation_steps = sorts.bubble_sort_steps(to_sort)
        elif self.spinner.text == "Сортировка вставками":
            self.button_shuffle.disabled = False
            self.animation_steps = sorts.insert_sort_steps(to_sort)
        elif self.spinner.text == "Сортировка слиянием":
            self.button_shuffle.disabled = False
            self.animation_steps = sorts.merge_sort_steps(to_sort)
        elif self.spinner.text == "Быстрая сортировка":
            self.button_shuffle.disabled = False
            self.animation_steps = sorts.quick_sort_steps(to_sort)
        elif self.spinner.text == "Сортировка выбором":
            self.button_shuffle.disabled = False
            self.animation_steps = sorts.select_sort_steps(to_sort)
        elif self.spinner.text == "Сортировка расческой":
            self.button_shuffle.disabled = False
            self.animation_steps = sorts.comb_sort_steps(to_sort)
        elif self.spinner.text == "Сортировка Шелла":
            self.button_shuffle.disabled = False
            self.animation_steps = sorts.shell_sort_steps(to_sort)
        elif self.spinner.text == "Шейкерная сортировка":
            self.button_shuffle.disabled = False
            self.animation_steps = sorts.shaker_sort_steps(to_sort)
        elif self.spinner.text == "Гномья сортировка":
            self.button_shuffle.disabled = False
            self.animation_steps = sorts.gnome_sort_steps(to_sort)
        elif self.spinner.text == "Случайная сортировка":
            new_data = self.bars_widget.values.copy()
            for i in range(len(new_data)):
                new_data[i] = randint(0, 100)
            self.bars_widget.original_values = new_data.copy()
            self.bars_widget.values = new_data.copy()

            self.bars_widget.draw_bars()
            self.button_shuffle.disabled = True
            if hasattr(self, 'st_forward'):
                self.st_forward.disabled = True
                self.st_back.disabled = True
            self.animation_steps = ()

    def on_spinner_select(self, spinner, value):
        self.status_label.text = f"Сложность сортировки: {self.speeds[value]}"
        spinner_values = []
        for i in range(0, len(self.spinner_values)):
            if self.spinner_values[i] != value:
                spinner_values.append(self.spinner_values[i])
        spinner.values = spinner_values

        self.set_animation_steps()


    def on_press_sort(self, instance):
        if instance.text == "Сбросить сортировку":
            self.bars_widget.reset()
            self.anim_index *= 0
            self.set_animation_steps()

            instance.text = "Запустить сортировку"


            if hasattr(self, 'st_forward') and self.spinner.text != "Случайная сортировка":
                self.st_forward.disabled = False
                self.st_back.disabled = True
            return

        self.bars_widget.animating = True

        self.set_animation_steps()

        self.bars_widget.animate(self.animation_steps, self.spinner.text)
        instance.text = "Сбросить сортировку"
        if hasattr(self, 'st_forward'):
            self.st_forward.disabled = True
            self.st_back.disabled = True

    def on_press_shuffle(self, instance):
        self.bars_widget.animating = False
        self.anim_index *= 0

        new_data = self.bars_widget.values.copy()
        for i in range(len(new_data)):
            new_data[i] = randint(0, 100)
        self.bars_widget.original_values = new_data.copy()
        self.bars_widget.values = new_data.copy()

        self.bars_widget.draw_bars()
        self.button_sort.text = "Запустить сортировку"
        self.set_animation_steps()

        if hasattr(self, 'st_forward'):
            self.st_forward.disabled = False
            self.st_back.disabled = True


    def on_press_steps(self, instance):
        self.bars_widget.reset()
        self.anim_index *= 0
        self.bars_widget.animating = False
        self.steps_layout.clear_widgets()

        self.st_back = Button(text='Шаг назад',
                            font_size='15sp',
                            size_hint=(1, 0.9),
                            on_press=self.on_press_s_back,
                            font_name=self.font,
                            background_normal='',
                            background_color=(0.02, 0.42, 0.80, 1),
                            disabled=True)
        self.st_forward = Button(text='Шаг вперед',
                            font_size='15sp',
                            size_hint=(1, 0.9),
                            height=50,
                            on_press=self.on_press_s_forward,
                            font_name=self.font,
                            background_normal='',
                            background_color=(0.02, 0.42, 0.80, 1))
        self.st_forward.disabled = False
        self.st_back.disabled = True


        button_layout = BoxLayout(orientation='horizontal', spacing=20)

        button_layout.add_widget(self.st_back)
        button_layout.add_widget(self.st_forward)
        self.steps_layout.add_widget(button_layout)

        self.button_sort.text = "Запустить сортировку"

        self.anim_index *= 0
        self.set_animation_steps()



    def on_press_s_back(self, instance):
        if getattr(self.bars_widget, "busy", False):
            return

        self.anim_index -= 1
        swap = self.animation_steps[self.anim_index]
        self.bars_widget.step(swap, self.spinner.text)

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
        self.bars_widget.step(swap, self.spinner.text)
        self.anim_index += 1

        if self.anim_index >= len(self.animation_steps):
            instance.disabled = True
            self.button_sort.text = "Сбросить сортировку"
            self.st_back.disabled = True
            return


if __name__ == '__main__':
    BarGraphApp().run()