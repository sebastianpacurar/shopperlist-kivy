from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem, OneLineAvatarListItem, ImageLeftWidget, IRightBodyTouch
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import MDSnackbar

from app.Database import Database


class MainScreen(MDScreen):
    pass


class ProductsScreen(MDScreen):
    pass


class CollectionScreen(MDScreen):
    pass


class ListScreen(MDScreen):
    pass


class ContentNavigationDrawer(MDScrollView):
    pass


class AddShoppingListContent(MDBoxLayout):
    pass


class ShopListProduct(MDScrollView):
    text = StringProperty()
    # img = ObjectProperty()


class MySnackbar(MDSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty('15sp')


class MyKivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.snackbar = None
        self.data = None
        self.prev_screen = None
        self.db = Database()

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.theme_style = 'Light'

    def on_start(self):
        self.prev_screen = self.root.ids.scr_manager.current_screen.name
        self.update_top_bar()
        self.get_lists()

    def show_dialog(self):
        content = AddShoppingListContent()

        if not self.dialog:
            self.dialog = MDDialog(
                type='custom',
                content_cls=content,
                on_dismiss=lambda _: self.clearDialog(),
                buttons=[
                    MDFlatButton(
                        text='Add',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda _: self.perform_shop_list_add(),
                    ),
                    MDFlatButton(
                        text='Cancel',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.error_color,
                        on_release=lambda _: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()

    def clearDialog(self):
        self.dialog = None

    def perform_shop_list_add(self):
        shop_list_name = self.dialog.content_cls.ids.shop_list_name_text.text
        self.db.add_shopping_list(shop_list_name)
        self.dialog.dismiss()
        self.show_snackbar()

    def show_snackbar(self):
        self.snackbar = MySnackbar(
            text='Success',
            icon='information',
        )
        self.snackbar.buttons = [MDFlatButton(
            text='OK',
            on_release=lambda _: self.snackbar.dismiss)]
        self.snackbar.open()

    def update_top_bar(self):
        top_bar = self.root.ids.top_bar
        sm = self.root.ids.scr_manager
        nav_drawer = self.root.ids.nav_drawer
        if sm.current in ['prod_scr', 'collection_scr']:
            top_bar.left_action_items = [['menu', lambda _: nav_drawer.set_state('open')]]
        else:
            top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]

        if sm.current == 'collection_scr':
            top_bar.right_action_items = [['plus-thick', lambda _: self.show_dialog()]]
        elif sm.current == 'list_content_scr':
            top_bar.right_action_items = [['plus-thick', lambda _: print('show dialog for add item in list')]]

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
        self.update_top_bar()

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
        show_list_items = self.root.ids.collection_id

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

        list_content_items = self.root.ids.list_content_items
        list_content_items.clear_widgets()

        for entry in data:
            item = OneLineAvatarListItem(
                ImageLeftWidget(
                    source=entry[4]
                ),
                text=entry[1],
                _no_ripple_effect=True
            )
            list_content_items.add_widget(item)

        self.change_screen('list_content_scr')


if __name__ == '__main__':
    MyKivyApp().run()
