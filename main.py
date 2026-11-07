import json
import os
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class SahilSevalApp(App):
    def build(self):
        self.title = "Sahil + Seval ❤️"
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = Label(
            text="Reşad Xəlifə - Video Axtarış", 
            size_hint_y=None, 
            height=50, 
            font_size=18,
            bold=True
        )
        root.add_widget(header)
        
        search_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.search_input = TextInput(
            hint_text="Axtarılacaq söz və ya cümlə yazın...", 
            multiline=False,
            font_size=16,
            halign='left'
        )
        self.search_input.bind(on_text_validate=self.perform_search)
        
        search_button = Button(
            text="Axtar", 
            size_hint_x=None, 
            width=100,
            background_color=(0.1, 0.5, 0.8, 1)
        )
        search_button.bind(on_press=self.perform_search)
        
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        root.add_widget(search_layout)
        
        self.results_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.results_layout)
        root.add_widget(scroll)
        
        self.load_data()
        return root

    def load_data(self):
        self.subtitles = {}
        self.videos = {}
        if os.path.exists("subtitles.json"):
            try:
                with open("subtitles.json", "r", encoding="utf-8") as f:
                    self.subtitles = json.load(f)
            except Exception as e:
                print(f"Subtitles oxunma xətası: {e}")
        if os.path.exists("videos.json"):
            try:
                with open("videos.json", "r", encoding="utf-8") as f:
                    self.videos = json.load(f)
            except Exception as e:
                print(f"Videos oxunma xətası: {e}")

    def perform_search(self, instance):
        query = self.search_input.text.strip().lower()
        self.results_layout.clear_widgets()
        
        if not query:
            no_input_lbl = Label(text="Zəhmət olmasa axtarış üçün söz daxil edin.", size_hint_y=None, height=40)
            self.results_layout.add_widget(no_input_lbl)
            return
            
        results_count = 0
        for video_id, fragments in self.subtitles.items():
            if isinstance(fragments, list):
                for frag in fragments:
                    text = frag.get("text", "")
                    if query in text.lower():
                        start_time = frag.get("start", 0)
                        video_info = self.videos.get(video_id, f"Video ID: {video_id}")
                        if isinstance(video_info, dict):
                            video_title = video_info.get("title", video_id)
                        else:
                            video_title = str(video_info)
                            
                        results_count += 1
                        card = BoxLayout(orientation='vertical', size_hint_y=None, height=110, padding=5, spacing=5)
                        time_str = self.format_time(start_time)
                        snippet_text = f"📹 {video_title}\n⏱ Dəqiqə: {time_str}\n💬 \"{text}\""
                        
                        info_label = Label(text=snippet_text, size_hint_y=None, height=70, halign='left', valign='middle')
                        info_label.bind(size=lambda s, w: setattr(s, 'text_size', (w[0] - 10, None)))
                        
                        open_btn = Button(text="▶ YouTube-da Aç", size_hint_y=None, height=35, background_color=(0.8, 0.2, 0.2, 1))
                        open_btn.bind(on_press=lambda x, vid=video_id, sec=start_time: self.open_youtube(vid, sec))
                        
                        card.add_widget(info_label)
                        card.add_widget(open_btn)
                        self.results_layout.add_widget(card)
                        
        if results_count == 0:
            not_found_lbl = Label(text="Axtarışınıza uyğun nəticə tapılmadı.", size_hint_y=None, height=40)
            self.results_layout.add_widget(not_found_lbl)

    def format_time(self, seconds):
        sec = int(seconds)
        m = sec // 60
        s = sec % 60
        return f"{m:02d}:{s:02d} ({sec}-ci saniyə)"

    def open_youtube(self, video_id, seconds):
        url = f"https://www.youtube.com/watch?v={video_id}&t={int(seconds)}s"
        webbrowser.open(url)

if __name__ == "__main__":
    SahilSevalApp().run()
