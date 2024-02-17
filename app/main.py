import os
import re

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from app.components.components import *

placeholder_img = os.path.join(os.getcwd(), '..', 'images', 'placeholder_image.png')
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


class MyKivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.prev_screen = None
        self.drop = DropdownHandler(self)
        self.user = {}

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.theme_style = 'Light'

    def on_start(self):
        self.prev_screen = self.root.ids.scr_manager.current_screen.name
        self.auto_login()

    def auto_login(self):
        data = db.user_auto_login()
        if len(data) > 0:
            self.user = data
            self.init_landing_screen()
        else:
            self.change_screen('usr_manager_scr')

    def init_landing_screen(self):
        self.change_screen('products_list_scr')

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

    # TODO: think of a better way to deal with this
    def perform_shop_list_add(self):
        shop_list_name = self.dialog.content_cls.ids.shop_list_name_text.text
        db_result = db.add_shopping_list(shop_list_name, self.user['id'])
        self.dialog.dismiss()
        MySnackbar(db_result)

    def update_top_bar(self):
        top_bar = self.root.ids.top_bar
        sm = self.root.ids.scr_manager
        nav_drawer = self.root.ids.nav_drawer
        nav_drawer_header = self.root.ids.nav_drawer_header

        # hack to prevent header from crashing
        nav_drawer_header.title = self.get_user_name() if self.user else ''
        nav_drawer_header.text = self.get_user_email() if self.user else ''

        match sm.current:
            case 'products_list_scr':
                top_bar.title = 'Products'
                top_bar.left_action_items = [['menu', lambda _: nav_drawer.set_state('open')]]
                top_bar.right_action_items = [
                    ['dots-horizontal-circle-outline', lambda x: self.drop.toggle(x)]]
            case 'collection_scr':
                top_bar.title = 'Collections'
                top_bar.left_action_items = [['menu', lambda _: nav_drawer.set_state('open')]]
                top_bar.right_action_items = [['plus-thick', lambda _: self.show_dialog()]]
            case 'list_content_scr':
                top_bar.title = 'Shopping List'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = [['plus-thick', lambda _: print('show dialog for add item in list')]]
            case 'add_prod_scr':
                top_bar.title = 'Add product'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = []
            case 'add_category_scr':
                top_bar.title = 'Add Category'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = []
            case 'add_unit_scr':
                top_bar.title = 'Add Category'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = []

    def navigate_back(self):
        sm = self.root.ids.scr_manager
        sm.current = self.prev_screen
        sm.transition.direction = 'right'
        self.update_top_bar()

    def display_list_products(self, *args):
        self.change_screen('list_content_scr')
        rv_data = []
        for entry in db.get_shop_list(args[0]):
            item_data = {
                'text': entry[1],
                'img_path': entry[4],
                '_no_ripple_effect': True,
            }
            rv_data.append(item_data)

        self.root.ids.rv_list_content.data = rv_data

    def change_screen(self, screen_name):
        sm = self.root.ids.scr_manager
        self.prev_screen = sm.current_screen.name
        sm.transition.direction = 'left'
        sm.current = screen_name
        self.update_top_bar()

    def set_app_user(self, user_data):
        self.user = user_data

    def get_user_name(self):
        return self.user['name']

    def get_user_email(self):
        return self.user['email']

    def unset_app_user(self):
        nav_drawer = self.root.ids.nav_drawer
        db.user_logout(self.user['name'])
        self.user = {}
        nav_drawer.set_state('close')
        self.change_screen('usr_manager_scr')

    def validate_text_field(self, widget):
        is_email = widget.hint_text.lower() == 'email'
        if len(widget.text) == 0:
            widget.helper_text = 'Cannot be empty'
            widget.error = True
        elif is_email and not re.match(email_regex, widget.text):
            widget.helper_text = 'Not a valid email'
            widget.error = True
        else:
            widget.helper_text = ''
            widget.error = False


if __name__ == '__main__':
    Window.size = (360, 640)
    MyKivyApp().run()
