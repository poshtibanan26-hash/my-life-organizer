import json
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

KV = """
BoxLayout:
    orientation: "vertical"
    padding: 15
    spacing: 10

    Label:
        text: "[b]MY LIFE ORGANIZER[/b]"
        markup: True
        font_size: "24sp"
        size_hint_y: None
        height: "55dp"

    Label:
        text: "Your life, your priorities"
        size_hint_y: None
        height: "30dp"

    TextInput:
        id: task_input
        hint_text: "Write a task..."
        multiline: False
        size_hint_y: None
        height: "48dp"

    Button:
        text: "Add New Task"
        size_hint_y: None
        height: "48dp"
        on_release: app.add_task()

    Label:
        text: "MY TASKS"
        size_hint_y: None
        height: "35dp"

    ScrollView:
        do_scroll_x: False

        GridLayout:
            id: task_list
            cols: 1
            spacing: 8
            size_hint_y: None
            height: self.minimum_height
"""

class LifeOrganizer(App):

    def build(self):
        self.title = "My Life Organizer"
        self.file_path = os.path.join(
            self.user_data_dir, "tasks.json"
        )

        self.tasks = []
        self.root_widget = Builder.load_string(KV)
        self.load_tasks()
        self.refresh_tasks()

        return self.root_widget

    def load_tasks(self):
        if os.path.exists(self.file_path):
            try:
                with open(
                    self.file_path, "r", encoding="utf-8"
                ) as file:
                    self.tasks = json.load(file)
            except (ValueError, OSError):
                self.tasks = []

    def save_tasks(self):
        os.makedirs(self.user_data_dir, exist_ok=True)

        with open(
            self.file_path, "w", encoding="utf-8"
        ) as file:
            json.dump(
                self.tasks, file, ensure_ascii=False,
                indent=2
            )

    def add_task(self):
        field = self.root_widget.ids.task_input
        text = field.text.strip()

        if not text:
            return

        self.tasks.append({
            "text": text,
            "done": False
        })

        field.text = ""
        self.save_tasks()
        self.refresh_tasks()

    def toggle_task(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.save_tasks()
        self.refresh_tasks()

    def delete_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()
        self.refresh_tasks()

    def refresh_tasks(self):
        task_list = self.root_widget.ids.task_list
        task_list.clear_widgets()

        for index, task in enumerate(self.tasks):
            row = BoxLayout(
                size_hint_y=None,
                height="55dp",
                spacing=5
            )

            status = "✓ " if task["done"] else ""
            label = Label(
                text=status + task["text"],
                halign="left",
                valign="middle"
            )
            label.bind(
                size=lambda instance, size:
                setattr(instance, "text_size", size)
            )

            done_button = Button(
                text="Undo" if task["done"] else "Done",
                size_hint_x=None,
                width="75dp"
            )
            done_button.bind(
                on_release=lambda btn, i=index:
                self.toggle_task(i)
            )

            delete_button = Button(
                text="Delete",
                size_hint_x=None,
                width="75dp"
            )
            delete_button.bind(
                on_release=lambda btn, i=index:
                self.delete_task(i)
            )

            row.add_widget(label)
            row.add_widget(done_button)
            row.add_widget(delete_button)

            task_list.add_widget(row)


if __name__ == "__main__":
    LifeOrganizer().run()
