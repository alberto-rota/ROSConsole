#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool

from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, Label
from textual.reactive import reactive

class ButtonText(Static):
    
    text = reactive("Not Pressed")
    
    def toggle(self):
        topics = rospy.get_published_topics()
        self.text=str(topics)
        # if self.text == "Pressed": self.text = "Not Pressed"
        # else: self.text = "Pressed"
        
    def watch_text(self, newtext: str) -> None:
        self.update(self.text)
        
class SimplePanel(App):
    CSS_PATH = "layout.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.button.variant="success"
        textwidget = self.query_one(ButtonText)
        textwidget.toggle()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Update",id="b",variant="error",classes="button")
        yield ButtonText("Not Pressed",classes="box")
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    
    app = SimplePanel()
    rospy.init_node('console', anonymous=True)
    app.run()
