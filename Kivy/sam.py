from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar  


KV = '''
BoxLayout:
    orientation: 'vertical'
    
    MDTopAppBar:  # Changed from MDToolbar to MDTopAppBar
        title: "Button to Card Example"
        elevation: 10

    BoxLayout:
        size_hint_y: None
        height: dp(50)
        padding: dp(10)
        spacing: dp(10)
        
        MDRaisedButton:
            text: "Card 1"
            on_release: app.show_card(1)

        MDRaisedButton:
            text: "Card 2"
            on_release: app.show_card(2)

        MDRaisedButton:
            text: "Card 3"
            on_release: app.show_card(3)

        MDRaisedButton:
            text: "Card 4"
            on_release: app.show_card(4)

    BoxLayout:
        id: card_container
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
'''

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def show_card(self, card_number):
        # Clear previous cards
        card_container = self.root.ids.card_container
        card_container.clear_widgets()
        
        # Create and add the appropriate card based on button click
        card = MDCard(
            size_hint=(1, None),
            height="200dp",
            padding="10dp",
            orientation="vertical",
            md_bg_color=(1, 1, 1, 1)
        )

        card_content = f"This is content for Card {card_number}"
        
        card.add_widget(
            MDLabel(
                text=card_content,
                halign="center",
                theme_text_color="Secondary",
                font_style="H6"
            )
        )

        card_container.add_widget(card)

# Run the app
MainApp().run()
