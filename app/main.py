import re

from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from app.components.components import *
from app.utils import constants as const

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


class MainScreen(MDScreen):
    pass


class MyKivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = {}
        self.screen_stack = []
        self.dialog = None
        self.drop = DropdownHandler()

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Orange'
        self.theme_cls.theme_style = 'Light'

    def on_start(self):
        self.auto_login()

    def auto_login(self):
        data = db.user_auto_login()
        if len(data) > 0:
            self.user = data
            self.root.ids.top_bar.disabled = False
            self.change_screen_and_update_bar(const.MULTI_PROD_SCR)
        else:
            self.change_screen(const.USER_MANAGER_SCREEN)

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
        db_result, msg = 0, "List can't be empty!"
        if len(shop_list_name) > 0:
            db_result = db.add_shopping_list(shop_list_name, self.user['id'])
            msg = f'{shop_list_name} created'
            self.dialog.dismiss()
        MySnackbar(msg, db_result)

    def update_top_bar(self):
        top_bar = self.root.ids.top_bar
        sm = self.root.ids.scr_manager
        nav_drawer = self.root.ids.nav_drawer
        nav_drawer_header = self.root.ids.nav_drawer_header

        # hack to prevent header from crashing
        nav_drawer_header.title = self.get_user_name()
        nav_drawer_header.text = self.get_user_email()

        match sm.current:
            case const.MULTI_PROD_SCR:
                top_bar.title = 'Products'
                top_bar.left_action_items = [['menu', lambda _: nav_drawer.set_state('open')]]
                top_bar.right_action_items = [
                    ['dots-horizontal-circle-outline', lambda x: self.drop.toggle(x)]]
            case const.COLLECTION_SCR:
                top_bar.title = 'Collections'
                top_bar.left_action_items = [['menu', lambda _: nav_drawer.set_state('open')]]
                top_bar.right_action_items = [['plus-thick', lambda _: self.show_dialog()]]
            case const.LIST_SCR:
                top_bar.title = 'Shopping List'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = [['plus-thick', lambda _: print('show dialog for add item in list')]]
            case const.ADD_PROD_SCR:
                top_bar.title = 'Add product'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = []
            case const.ADD_DATA_SCR:
                top_bar.title = 'Add data'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = []
            case const.PROD_SCR:
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = []
            case const.USER_MANAGER_SCREEN:
                top_bar.left_action_items = []
                top_bar.right_action_items = []

    def change_screen(self, screen_name):
        self.screen_stack.append(screen_name)
        sm = self.root.ids.scr_manager
        sm.transition.direction = 'left'
        sm.current = self.screen_stack[-1]

    def navigate_back(self):
        self.screen_stack = self.screen_stack[:-1]
        sm = self.root.ids.scr_manager
        sm.transition.direction = 'right'
        sm.current = self.screen_stack[-1]
        self.update_top_bar()

    def change_screen_and_update_bar(self, screen_name):
        self.change_screen(screen_name)
        self.update_top_bar()

    def change_screen_to_prod_scr(self, product_id):
        prod_screen = self.root.ids.scr_manager.get_screen(const.PROD_SCR)
        prod_screen.prod_id = product_id
        self.change_screen(const.PROD_SCR)
        self.update_top_bar()

    def change_screen_to_list_scr(self, list_id):
        list_screen = self.root.ids.scr_manager.get_screen(const.LIST_SCR)
        list_screen.list_id = list_id
        self.change_screen(const.LIST_SCR)
        self.update_top_bar()

    def set_app_user(self, user_data):
        self.user = user_data

    def get_user_name(self):
        return self.user['name']

    def get_user_email(self):
        return self.user['email']

    def unset_app_user(self):
        db.user_logout(self.user['name'])
        self.user = {}
        self.root.ids.nav_drawer.set_state('close')
        self.root.ids.top_bar.disabled = True
        self.change_screen(const.USER_MANAGER_SCREEN)

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
