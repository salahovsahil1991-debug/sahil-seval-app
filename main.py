import os, json, re, webbrowser
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

Window.clearcolor = (0.08, 0.09, 0.12, 1)

class SearchApp(App):
    def build(self):
        self.title = "Sahil + Seval ❤️"
        with open("videos.json", encoding="utf-8") as f:
            self.videos = json.load(f)

        root = BoxLayout(orientation="vertical", padding=12, spacing=10)

        root.add_widget(Label(
            text="[b]Sahil + Seval ❤️[/b]\nReşad Halife video axtarışı",
            markup=True, font_size=22, size_hint_y=None, height=75
        ))

        self.search_input = TextInput(
            hint_text="Söz yazın: Allah, tövbə, Quran...",
            multiline=False, size_hint_y=None, height=50,
            font_size=18
        )
        self.search_input.bind(on_text_validate=self.search)
        root.add_widget(self.search_input)

        btn = Button(text="AXTAR", size_hint_y=None, height=50)
        btn.bind(on_press=self.search)
        root.add_widget(btn)

        self.status = Label(text="", size_hint_y=None, height=35)
        root.add_widget(self.status)

        self.results = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.results.bind(minimum_height=self.results.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.results)
        root.add_widget(scroll)

        self.message("Axtarış üçün söz daxil edin.")
        self.status.text = f"{len(self.videos)} video siyahıda"
        return root

    def message(self, text):
        self.results.clear_widgets()
        self.results.add_widget(Label(
            text=text, size_hint_y=None, height=80,
            halign="center", valign="middle"
        ))

    def search(self, instance):
        word = self.search_input.text.strip().casefold()
        if not word:
            self.message("Axtarılacaq sözü yazın.")
            return

        self.results.clear_widgets()
        count = 0

        for video in self.videos:
            path = os.path.join("transcripts", video["id"] + ".srt")
            if not os.path.exists(path):
                continue

            with open(path, encoding="utf-8-sig") as f:
                content = f.read()

            blocks = re.split(r"\n\s*\n", content.strip())

            for block in blocks:
                lines = block.splitlines()
                time_line = next((x for x in lines if "-->" in x), None)
                if not time_line:
                    continue

                text = " ".join(
                    x for x in lines
                    if "-->" not in x and not x.strip().isdigit()
                ).strip()

                if word not in text.casefold():
                    continue

                start = time_line.split("-->")[0].strip()
                h, m, s = start.replace(",", ".").split(":")
                seconds = int(h)*3600 + int(m)*60 + int(float(s))
                count += 1

                card = BoxLayout(
                    orientation="vertical", padding=8, spacing=5,
                    size_hint_y=None, height=125
                )
                card.add_widget(Label(
                    text=video["title"], size_hint_y=None,
                    height=38, font_size=14
                ))
                card.add_widget(Label(
                    text=text, size_hint_y=None, height=42,
                    font_size=13
                ))

                link = (
                    f"https://www.youtube.com/watch?v="
                    f"{video['id']}&t={seconds}s"
                )
                open_btn = Button(
                    text=f"Videonu {m}:{int(float(s)):02d} vaxtından aç",
                    size_hint_y=None, height=38
                )
                open_btn.bind(
                    on_press=lambda _, url=link: webbrowser.open(url)
                )
                card.add_widget(open_btn)
                self.results.add_widget(card)

        if count == 0:
            self.message(
                "Nəticə tapılmadı.\n"
                "Əvvəlcə videoların transkripsiyaları əlavə edilməlidir."
            )
        else:
            self.status.text = f"{count} nəticə tapıldı"

if __name__ == "__main__":
    SearchApp().run()
