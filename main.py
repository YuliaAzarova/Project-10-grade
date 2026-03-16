from pygments.styles.dracula import background
from kivy.config import Config
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

class BarGraphApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)


        spinner_values = ('Сортировка пузырьком', 'Сортировка слиянием', 'Сортировка вставками',
                    'Быстрая сортировка', 'Сортировка выбором', 'Сортировка расческой')
        current_value = spinner_values[0]
        self.spinner = Spinner(
            text=current_value,
            values=spinner_values,
            size_hint=(0.6, None),
            size=(1, 100),
            pos_hint={'center_x': 0.3, 'center_y': 0.5})
        self.spinner.bind(text=self.on_spinner_select)
        layout.add_widget(self.spinner)



        self.status_label = Label(text=self.spinner.text,
                            size_hint=(1, None),
                            height=150,
                            font_size='35sp',
                            color="#E0FFFF")
        layout.add_widget(self.status_label)



        diagram_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(1, 2))
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
                        background_color="#1E90FF") # зеленый
        self.button_shuffle = Button(text='Перемешать',
                                  font_size='15sp',
                                  size_hint=(1, None),
                                  on_press=self.on_press_shuffle,
                                  background_color="#1E90FF")
        buttons_layout.add_widget(self.button_sort)
        buttons_layout.add_widget(self.button_shuffle)

        self.steps_layout = BoxLayout(
            orientation='horizontal',
            spacing=20, size_hint=(1, None))
        self.button_steps = Button(text='Запустить шаги',
                         font_size='15sp',
                        on_press=self.on_press_steps,
                        background_color="#00BFFF") # синий
        self.steps_layout.add_widget(self.button_steps)
        buttons_layout.add_widget(self.steps_layout)

        layout.add_widget(buttons_layout)



        self.animation_steps = []
        self.anim_index = 0
        self.anim_event = None



        self.steps_count = 0
        self.steps = [(i, j) for i in range(len(self.data)) for j in range(0, i) ]
        return layout



    def on_spinner_select(self, spinner, value):
        self.status_label.text = value

    def set_animation_steps(self, to_sort):
        if self.status_label.text == "Сортировка пузырьком":
            self.animation_steps = sorts.bubble_sort_steps(to_sort)
        elif self.status_label.text == "Сортировка вставками":
            self.animation_steps = sorts.insert_sort_steps(to_sort)
        elif self.status_label.text == "Сортировка слиянием":
            self.animation_steps = sorts.merge_sort_steps(to_sort)
        elif self.status_label.text == "Быстрая сортировка":
            self.animation_steps = sorts.quick_sort_steps(to_sort)
        elif self.status_label.text == "Сортировка выбором":
            self.animation_steps = sorts.select_sort_steps(to_sort)
        elif self.status_label.text == "Сортировка расческой":
            self.animation_steps = sorts.comb_sort_steps(to_sort)



    def on_press_sort(self, instance):
        if instance.text == "Сбросить сортировку":
            self.bars_widget.reset()
            self.anim_index *= 0
            self.set_animation_steps(self.bars_widget.original_values.copy())

            instance.text = "Запустить сортировку"


            if hasattr(self, 'st_forward'):
                self.st_forward.disabled = False
                self.st_back.disabled = True
            return

        self.bars_widget.animating = True

        if self.anim_index > 0:
            to_sort = self.bars_widget.values.copy()
        else:
            to_sort = self.bars_widget.original_values.copy()

        self.set_animation_steps(to_sort)

        self.bars_widget.animate(self.animation_steps, self.status_label.text)
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
        self.set_animation_steps(self.bars_widget.original_values.copy())

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
                                 background_color="#4169E1",
                                      disabled=True)
        self.st_forward = Button(text='Шаг вперед',
                             font_size='15sp',
                             size_hint=(1, 0.9),
                                height=50,
                            on_press=self.on_press_s_forward,
                                    background_color="#4169E1")
        self.st_forward.disabled = False
        self.st_back.disabled = True


        button_layout = BoxLayout(orientation='horizontal', spacing=20)

        button_layout.add_widget(self.st_back)
        button_layout.add_widget(self.st_forward)
        self.steps_layout.add_widget(button_layout)

        self.button_sort.text = "Запустить сортировку"

        self.anim_index *= 0
        self.set_animation_steps(self.bars_widget.original_values.copy())



    def on_press_s_back(self, instance):
        if getattr(self.bars_widget, "busy", False):
            return

        self.anim_index -= 1
        swap = self.animation_steps[self.anim_index]
        self.bars_widget.step(swap, self.status_label.text)

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
        self.bars_widget.step(swap, self.status_label.text)
        self.anim_index += 1

        if self.anim_index >= len(self.animation_steps):
            instance.disabled = True
            self.button_sort.text = "Сбросить сортировку"
            self.st_back.disabled = True
            return


if __name__ == '__main__':
    BarGraphApp().run()