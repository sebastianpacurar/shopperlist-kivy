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
        self.root.ids.speed_dial.data = self.data
        self.get_lists()

    def change_to_add_screen(self, option):
        self.root.ids.speed_dial.close_stack()
        sm = self.root.ids.scr_manager
        if option.icon == 'food-drumstick':
            sm.current = 'add_prod_scr'
        else:
            sm.current = 'add_list_scr'

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
        try:
            list_id = args[0].id.split('_')[1]
            data = self.db.get_shop_list(list_id)
            sm = self.root.ids.scr_manager
            sm.current = 'list_content_scr'
            list_content_items = self.root.ids.list_content_items
            list_content_items.clear_widgets()  # Clear previous list items
            for entry in data:
                item = SwipeToDeleteItem(text=entry[1])
                list_content_items.add_widget(item)
        except Exception as e:
            print(f"Error in get_list: {str(e)}")


if __name__ == '__main__':
    MyKivyApp().run()
