import json
import re
import webbrowser
import unicodedata

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

Window.clearcolor = (0.08, 0.09, 0.12, 1)


def normalize(text):
    text = text.casefold().replace("ı", "i")
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def to_seconds(timestamp):
    h, m, s = timestamp.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + int(float(s))


class SearchApp(App):
    def build(self):
        self.title = "Sahil + Seval ❤️"

        with open("subtitles.json", encoding="utf-8") as f:
            self.subtitles = json.load(f)

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        root.add_widget(Label(
            text="[b]Sahil + Seval ❤️[/b]\nReşad Halife video axtarışı",
            markup=True,
            font_size=22,
            size_hint_y=None,
            height=75
        ))

        self.search_input = TextInput(
            hint_text="Axtarılacaq sözü yazın...",
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size=18
        )
        self.search_input.bind(on_text_validate=self.search)
        root.add_widget(self.search_input)

        btn = Button(
            text="AXTAR",
            size_hint_y=None,
            height=50
        )
        btn.bind(on_press=self.search)
        root.add_widget(btn)

        self.status = Label(
            text="",
            size_hint_y=None,
            height=35
        )
        root.add_widget(self.status)

        self.results = GridLayout(
            cols=1,
            spacing=8,
            size_hint_y=None
        )
        self.results.bind(
            minimum_height=self.results.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.results)
        root.add_widget(scroll)

        self.status.text = f"{len(self.subtitles)} mətn parçası bazada"
        self.message("Axtarış üçün söz daxil edin.")

        return root

    def message(self, text):
        self.results.clear_widgets()
        self.results.add_widget(Label(
            text=text,
            size_hint_y=None,
            height=80,
            halign="center",
            valign="middle"
        ))

    def search(self, instance):
        word = normalize(self.search_input.text.strip())

        if not word:
            self.message("Axtarılacaq sözü yazın.")
            return

        self.results.clear_widgets()
        count = 0

        for item in self.subtitles:
            original_text = item.get("text", "")

            if word not in normalize(original_text):
                continue

            seconds = to_seconds(item["start"])
            count += 1

            card = BoxLayout(
                orientation="vertical",
                padding=8,
                spacing=5,
                size_hint_y=None,
                height=145
            )

            card.add_widget(Label(
                text=item.get("title", ""),
                size_hint_y=None,
                height=38,
                font_size=14
            ))

            card.add_widget(Label(
                text=original_text,
                size_hint_y=None,
                height=55,
                font_size=14
            ))

            link = (
                "https://www.youtube.com/watch?v="
                + item["id"] + "&t=" + str(seconds) + "s"
            )

            open_btn = Button(
                text="Videonu " + item["start"] + " vaxtından aç",
                size_hint_y=None,
                height=40
            )

            open_btn.bind(
                on_press=lambda _, url=link: webbrowser.open(url)
            )

            card.add_widget(open_btn)
            self.results.add_widget(card)

        if count == 0:
            self.message("Bu söz mətn bazasında tapılmadı.")
            self.status.text = "Nəticə yoxdur"
        else:
            self.status.text = f"{count} nəticə tapıldı"


if __name__ == "__main__":
    SearchApp().run()
