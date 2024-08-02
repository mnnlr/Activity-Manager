from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineIconListItem
from kivymd.icon_definitions import md_icons

Builder.load_string(
    '''
<IconItem@OneLineIconListItem>
    IconLeftWidget:
        icon: root.icon

    MDLabel:
        text: root.text
        halign: 'center'

<PreviousMDIcons>
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)

        BoxLayout:
            adaptive_height: True

            MDIconButton:
                icon: 'magnify'
                pos_hint: {'center_y': .5}

            MDTextField:
                id: search_field
                hint_text: 'Search icon'
                on_text: root.set_list_md_icons(self.text, True)

        RecycleView:
            id: rv
            viewclass: 'IconItem'
            key_viewclass: 'viewclass'
            key_size: 'height'

            RecycleBoxLayout:
                padding: dp(10), dp(10), 0, dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
'''
)


class IconItem(OneLineIconListItem):
    icon = StringProperty()
    text = StringProperty()


class PreviousMDIcons(MDScreen):
    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {
                    "viewclass": "IconItem",
                    "icon": name_icon,
                    "text": name_icon,
                }
            )

        self.ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)


class MainApp(MDApp):
    def build(self):
        return PreviousMDIcons()

    def on_start(self):
        self.root.set_list_md_icons()


if __name__ == '__main__':
    MainApp().run()
