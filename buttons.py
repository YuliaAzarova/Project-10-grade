from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

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