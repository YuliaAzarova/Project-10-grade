import bubble_sort, buttons
from kivy.config import Config
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '900')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy_garden.graph import Graph, BarPlot
from kivy.utils import get_color_from_hex as rgb
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from pygments.styles.dracula import background
from kivy.clock import Clock


class BarGraphApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20)



        # выбор сортировки
        self.spinner = Spinner(
            text='Сортировка пузырьком',
            values=('Сортировка пузырьком', 'Сортировка слиянием', 'Сортировка вставками'),
            size_hint=(0.6, None),
            size=(1, 100),
            pos_hint={'center_x': 0.3, 'center_y': 0.5},
            # background_color=[0, 1, 1, 1]
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



        # диаграмма
        self.graph = Graph(
            size_hint_y=3,
            size_hint_x=1,
            x_ticks_minor=1, x_ticks_major=0.5, # основные и вспомогательные деления
            y_ticks_major=10, y_ticks_minor=2, # основные деления и деления внутри делений
            y_grid_label=True, x_grid_label=True, # наличие подписей делений
            padding=10, # отступ
            x_grid=True, y_grid=True, # наличие сетки по x, y
            xmin=-0.5, xmax=10, # координаты
            ymin=0, ymax=100)
        layout.add_widget(self.graph) # добавляем график
        self.data = [
            (0, 85),
            (1, 40),
            (2, 95),
            (3, 60),
            (4, 20),
            (5, 10),
            (6, 15),
            (7, 5),
            (8, 50),
            (9, 100),
        ] # столбцы x и y
        self.plot_bar = BarPlot(color=rgb('#AFEEEE'), bar_width=50) # ширина столбца
        self.plot_bar.points = self.data # параметры столбцов
        self.graph.add_plot(self.plot_bar) # нарисовка



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
        self.button_steps = Button(text='Запустить по шагам',
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
            self.reset()
            if self.button_steps.disabled:
                self.st_forward.text = "Шаг вперед"
                self.st_forward.disabled = False
            instance.text = "Запустить сортировку"
            return


        self.animation_steps = bubble_sort.bubble_sort_steps(self.data)
        print(len(self.animation_steps))
        self.anim_index = 0
        self.anim_event = Clock.schedule_interval(self.animate, 0.05)

        self.steps_count = len(self.steps)
        if self.button_steps.text != "Сбросить сортировку":
            instance.text = "Сбросить сортировку"
        else:
            self.button_steps.disabled = False
            instance.disabled = True

            if self.button_steps.disabled:
                self.st_forward.disabled = True
                self.st_forward.text = "Конец сортировки"
                self.st_back.disabled = False
# +-

    def on_press_steps(self, instance):
        if instance.text == "Запустить по шагам":
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


            button_layout = BoxLayout(orientation='horizontal',
                                      spacing=20)

            button_layout.add_widget(self.st_back)
            button_layout.add_widget(self.st_forward)
            self.buttons_container.add_widget(button_layout)
            instance.text = "Сбросить сортировку"
            instance.disabled = True
        else:
            self.plot_bar.points = self.data
            self.graph.add_plot(self.plot_bar)
            self.steps_count = 0
            self.button_sort.disabled = False
            instance.disabled = True
            if self.button_steps.disabled:
                self.st_forward.text = "Шаг вперед"
                self.st_forward.disabled = False
# +-

    def on_press_s_back(self, instance):
        self.steps_count -= 1
        if self.steps_count == 0:
            instance.disabled = True
        self.st_forward.disabled = False
        self.st_forward.text = "Шаг вперед"


    def on_press_s_forward(self, instance):
        self.steps_count += 1
        self.st_back.disabled = False
        instance.text = "Шаг вперед"
        if self.steps_count >= len(self.steps):
            instance.disabled = True
            instance.text = "Конец сортировки"
            self.button_sort.text = "Сбросить сортировку"

    def animate(self, dt):
        if self.anim_index >= len(self.animation_steps): # проверка сколько шагов сделано
            self.anim_event.cancel()
            return

        self.plot_bar.points = self.animation_steps[self.anim_index] # анимация

        self.anim_index += 1

    def reset(self):
        if self.anim_event:
            self.anim_event.cancel()

        self.plot_bar.points = self.data
        self.anim_index = 0

if __name__ == '__main__':
    BarGraphApp().run()