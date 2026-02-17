from pygments.styles.dracula import background
from kivy.config import Config
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '900')

import sorts
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from widget import BarsWidget


class BarGraphApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

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



        self.animation_steps = []
        self.anim_index = 0
        self.anim_event = None



        self.steps_count = 0
        self.steps = [(i, j) for i in range(len(self.data)) for j in range(0, i) ]
        return layout

    def on_spinner_select(self, spinner, value):
        self.status_label.text = value



    def on_press_sort(self, instance):
        if instance.text == "Сбросить сортировку":
            self.bars_widget.reset()
            self.anim_index *= 0
            if self.status_label.text == "Сортировка пузырьком":
                self.animation_steps = sorts.bubble_sort_steps(self.bars_widget.original_values.copy())
            elif self.status_label.text == "Сортировка вставками":
                self.animation_steps = sorts.insert_sort_steps(self.bars_widget.original_values.copy())

            instance.text = "Запустить сортировку"


            if hasattr(self, 'st_forward'):
                self.st_forward.disabled = False
                self.st_back.disabled = True
            return

        self.bars_widget.animating = True

        if self.status_label.text == "Сортировка пузырьком":
            self.bars_widget.animating = True
            if self.anim_index > 0:
                self.animation_steps = sorts.bubble_sort_steps(self.bars_widget.values.copy())
            else:
                self.animation_steps = sorts.bubble_sort_steps(self.bars_widget.original_values.copy())
        elif self.status_label.text == "Сортировка вставками":
            self.bars_widget.animating = True
            if self.anim_index > 0:
                self.animation_steps = sorts.insert_sort_steps(self.bars_widget.values.copy())
            else:
                self.animation_steps = sorts.insert_sort_steps(self.bars_widget.original_values.copy())
        elif self.status_label.text == "Сортировка слиянием":
            pass

        self.bars_widget.animate(self.animation_steps)
        instance.text = "Сбросить сортировку"
        if hasattr(self, 'st_forward'):
            self.st_forward.disabled = True
            self.st_back.disabled = True


    def on_press_steps(self, instance):
        self.bars_widget.reset()
        self.anim_index *= 0
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
        if self.anim_index > 0:
            self.st_forward.disabled= False
            self.st_back.disabled = False
        else:
            self.st_forward.disabled = False
            self.st_back.disabled = True


        button_layout = BoxLayout(orientation='horizontal', spacing=20)

        button_layout.add_widget(self.st_back)
        button_layout.add_widget(self.st_forward)
        self.buttons_container.add_widget(button_layout)

        instance.text = "Идет сортировка"
        instance.disabled = True

        self.anim_index *= 0
        if self.status_label.text == "Сортировка пузырьком":
            self.animation_steps = sorts.bubble_sort_steps(self.bars_widget.original_values.copy())
        elif self.status_label.text == "Сортировка вставками":
            self.animation_steps = sorts.insert_sort_steps(self.bars_widget.original_values.copy())




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
        self.bars_widget.step(swap)
        self.anim_index += 1

        if self.anim_index >= len(self.animation_steps):
            instance.disabled = True
            self.button_sort.text = "Сбросить сортировку"
            self.st_back.disabled = True
            return


if __name__ == '__main__':
    BarGraphApp().run()
