#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from textual.containers import Container
from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, Label
from textual.reactive import reactive

class TopicButton(Static):
    
    def compose(self) -> ComposeResult:
        yield Button()
    
    def update_topics(self):
        pass
        
    def watch_text(self, newtext: str) -> None:
        self.update(self.text)
        
class SimplePanel(App):
    CSS_PATH = "layout.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.button.variant="success"
        textwidget = self.query_one(TopicButton)
        textwidget.update_topics()
        topics = rospy.get_published_topics()
        self.text=str(topics)
        for tn,t in enumerate(topics):
            topicbutton = Button(str(t[0]),id="topic"+str(tn))
            self.query_one("#topicbutton").mount(topicbutton)
            topicbutton.scroll_visible()


    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Update",id="b",variant="error",classes="button")
        yield TopicButton("Not Pressed",classes="box")
        yield Container(id="topicbutton")
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    
    app = SimplePanel()
    rospy.init_node('console', anonymous=True)
    app.run()
