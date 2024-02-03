from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from app.Database import Database


class MainScreen(MDScreen):
    pass


class ProductsScreen(MDScreen):
    pass


class ListsScreen(MDScreen):
    pass


class ListScreen(MDScreen):
    pass


class ContentNavigationDrawer(MDScrollView):
    pass


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()


class MyKivyApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
        self.prev_screen = None
        self.db = Database()

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Light"

    def on_start(self):
        self.data = {
            "lists": [
                "format-list-numbered",
                "on_release", lambda x: self.change_to_add_screen(x)
            ],
            "products": [
                "food-drumstick",
                "on_release", lambda x: self.change_to_add_screen(x)
            ],
        }
        self.prev_screen = self.root.ids.scr_manager.current_screen.name
        self.update_top_bar()
        self.root.ids.speed_dial.data = self.data
        self.get_lists()

    def change_to_add_screen(self, option):
        self.root.ids.speed_dial.close_stack()
        if option.icon == 'food-drumstick':
            self.change_screen('add_prod_scr')
        else:
            self.change_screen('add_list_scr')

    def update_top_bar(self):
        top_bar = self.root.ids.top_bar
        sm = self.root.ids.scr_manager
        nav_drawer = self.root.ids.nav_drawer
        if sm.current in ['prod_scr', 'list_scr']:
            top_bar.left_action_items = [['menu', lambda _: nav_drawer.set_state('open')]]
        else:
            top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]

    def navigate_back(self):
        sm = self.root.ids.scr_manager
        sm.current = self.prev_screen
        sm.transition.direction = 'right'
        self.update_top_bar()

    def change_screen(self, screen_name):
        sm = self.root.ids.scr_manager
        self.prev_screen = sm.current_screen.name
        sm.transition.direction = 'left'
        sm.current = screen_name

    # issue here
    def get_products(self):
        data = self.db.get_all_products()
        prod_items = self.root.ids.prod_items

        if len(prod_items.children) > 0:
            prod_items.clear_widgets()

        # for entry in data:
        #     name = entry[1]
        #     price = entry[2]
        #     stamp = entry[2].strftime("%Y-%m-%d %I:%M %p")
        #     item = TwoLineListItem(
        #         text=entry[1],
        #         secondary_text=stamp,
        #     )
        #
        #     prod_items.add_widget(item)

    def get_lists(self):
        data = self.db.get_shop_lists()
        show_list_items = self.root.ids.shop_list_items

        if len(show_list_items.children) > 0:
            show_list_items.clear_widgets()

        for entry in data:
            stamp = entry[2].strftime("%Y-%m-%d %I:%M %p")
            item = TwoLineListItem(
                id=f'e_{entry[0]}',
                text=entry[1],
                secondary_text=stamp,
                on_release=lambda x: self.get_list(x)
            )

            show_list_items.add_widget(item)

    def get_list(self, *args):
        list_id = args[0].id.split('_')[1]
        data = self.db.get_shop_list(list_id)
        self.change_screen('list_content_scr')

        list_content_items = self.root.ids.list_content_items
        list_content_items.clear_widgets()  # Clear previous list items
        for entry in data:
            item = SwipeToDeleteItem(text=entry[1])
            list_content_items.add_widget(item)

        self.update_top_bar()


if __name__ == '__main__':
    MyKivyApp().run()
