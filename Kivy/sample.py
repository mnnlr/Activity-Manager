from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

class ProfileCard(MDCard):
    name = StringProperty("Deepak")
    designation = StringProperty("Software Engineer")
    address = StringProperty("Kakinada")
    phone_number = StringProperty("9131043168")
    email = StringProperty("ootaladeepak128@gmail.com")

class AwesomeApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file('sample.kv')

    def on_card_click(self):
        print("Card Clicked: Displaying the table")
        
        # Update the label text
        self.root.ids.widget.text = "Attendance"

        # Create the table
        table = MDDataTable(
            size_hint=(1, None),
            height=dp(330),
            rows_num=15,
            check=True,
            column_data=[
                ("First Name", dp(40)),
                ("Last Name", dp(40)),
                ("Email Address", dp(40)),
                ("Phone Number", dp(40))
            ],
            row_data=[
                ("John", "Elder", "john@codemy.com", "(123) 456-7891"),
                ("Mary", "Elder", "mary@codemy.com", "(123) 456-1123"),
                ("Alice", "Smith", "alice@example.com", "(987) 654-3210"),
                ("Bob", "Brown", "bob@example.com", "(555) 123-4567"),
                ("John", "Elder", "john@codemy.com", "(123) 456-7891"),
                ("Mary", "Elder", "mary@codemy.com", "(123) 456-1123"),
                ("Alice", "Smith", "alice@example.com", "(987) 654-3210"),
                ("Bob", "Brown", "bob@example.com", "(555) 123-4567"),
                ("John", "Elder", "john@codemy.com", "(123) 456-7891"),
                ("Mary", "Elfber", "mary@codemy.com", "(123) 456-1123"),
                ("Alice", "Smith", "alice@exadgmple.com", "(987) 654-3210"),
                ("Bob", "Brown", "bob@example.com", "(555) 123-4567"),
                ("John", "Eldecbr", "john@codecbmy.com", "(123) 456-7891"),
                ("Mary", "Elder", "mary@codemy.com", "(123) 456-1123"),
                ("Alice", "Smith", "alice@exampcvcle.com", "(987) 654-3210"),
                ("Bob", "Brown", "bob@example.com", "(555) 123-4567"),
            ]
        )

        # Clear any existing widgets in the scroll container and add the table
        self.root.ids.scroll_container.clear_widgets()
        self.root.ids.scroll_container.add_widget(table)

if __name__ == '__main__':
    AwesomeApp().run()
