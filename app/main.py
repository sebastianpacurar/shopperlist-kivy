import re

from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition, SwapTransition
from kivymd.uix.list import MDListItemHeadlineText
from kivymd.uix.screen import MDScreen

import app.components.components
from app.components.components import *
from app.utils import constants as const

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


class MainScreen(MDScreen):
    pass


class MyKivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_stack = []
        self.sm = None
        self.top_bar = None
        self.nav_drawer = None
        self.user = {}

    def build(self):
        self.theme_cls.primary_palette = 'Lightblue'
        self.theme_cls.theme_style = 'Light'

    def on_start(self):
        self.nav_drawer = self.root.ids.nav_drawer
        self.sm = self.root.ids.scr_manager
        self.top_bar = self.root.ids.top_bar
        self.auto_login()
        super().on_start()

    def auto_login(self):
        data = db.user_auto_login()
        if len(data) > 0:
            self.user = data
            self.top_bar.disabled = False
            self.change_screen_and_update_bar(const.COLLECTION_SCR)
        else:
            self.change_screen(const.USER_MANAGER_SCREEN)

    def show_dialog(self, *args):
        content = args[0]
        dialog = MyDialog(MDDialogContentContainer(content), size_hint_x=.95)

        match type(content):
            case app.components.components.AddShoppingListContent:
                dialog.confirm = lambda x=content.ids.text_field: self.perform_shop_list_add(dialog, x)
                dialog.headline = 'New List'
                dialog.accept_txt = 'Add List'
            case app.components.components.RenameShoppingListContent:
                dialog.confirm = lambda x=content.ids.text_field: self.update_list_name(dialog, x, content.list_id)
                dialog.headline = 'Rename List'
                dialog.accept_txt = 'Update List'
        dialog.open()

    def update_list_name(self, *args):
        dialog = args[0]
        shop_list_name = args[1].text
        list_id = args[2]
        db_result = db.update_shop_list_name(shop_list_name, list_id)
        msg = 'List name cannot be empty'
        if len(shop_list_name) > 0:
            if db_result:
                msg = f'{shop_list_name} updated!'
                dialog.dismiss()
        MySnackbar(msg, db_result)

    def perform_shop_list_add(self, *args):
        dialog = args[0]
        shop_list_name = args[1].text
        db_result, msg = 0, "List can't be empty!"
        if len(shop_list_name) > 0:
            db_result = db.add_shopping_list(shop_list_name, self.user['id'])
            msg = f'{shop_list_name} created'
            dialog.dismiss()
        MySnackbar(msg, db_result)

    # TODO: debug this some more
    def toggle_bottom(self, *args):
        sheet = self.root.ids.bottom_sheet
        sheet.set_state('toggle')
        if sheet.state == 'close':
            handle = self.root.ids.handle
            list_content = self.root.ids.content_list
            handle.title = args[0]
            list_content.add_widget(MDListItem(
                MDListItemHeadlineText(text='Rename'),
                on_release=lambda _: (
                    self.show_dialog(RenameShoppingListContent(list_id=args[1])),
                    sheet.set_state('close')),
            ))
            list_content.add_widget(MDListItem(
                MDListItemHeadlineText(text='Delete'),
                on_release=lambda x: print(x),
            ))

    def clean_sheet(self):
        handle = self.root.ids.handle
        list_content = self.root.ids.content_list
        handle.text = ''
        list_content.clear_widgets()

    def open_navbar(self, *args):
        self.nav_drawer.set_state('open')

    def update_top_bar(self):
        nav_user_txt = self.root.ids.nav_user_name
        nav_email_txt = self.root.ids.nav_email
        nav_user_txt.text = self.get_user_name()
        nav_email_txt.text = self.get_user_email()

        left_btn = self.root.ids.top_bar_left_btn
        right_btn = self.root.ids.top_bar_right_btn
        top_bar_title = self.root.ids.top_bar_name

        match self.sm.current:
            case const.MULTI_PROD_SCR:
                top_bar_title.text = 'Products'
                left_btn.icon = 'menu'
                right_btn.icon = 'dots-horizontal-circle-outline'
                left_btn.on_release = lambda btn=left_btn: self.open_navbar(btn)
                right_btn.on_release = lambda btn=right_btn: DropdownHandler().toggle(btn)
                right_btn.disabled = False
            case const.COLLECTION_SCR:
                top_bar_title.text = 'Collections'
                left_btn.icon = 'menu'
                right_btn.icon = 'plus-thick'
                left_btn.on_release = lambda btn=left_btn: self.open_navbar(btn)
                right_btn.on_release = lambda btn=right_btn: self.show_dialog(AddShoppingListContent())
                right_btn.disabled = False
            case const.LIST_SCR:
                top_bar_title.text = 'Shopping List'
                left_btn.icon = 'arrow-left'
                left_btn.on_release = lambda btn=left_btn: self.navigate_back(btn)
                right_btn.on_release = lambda: self.show_dialog()
                right_btn.disabled = False
            case const.ADD_PROD_SCR:
                top_bar_title.text = 'Add product'
                left_btn.icon = 'arrow-left'
                right_btn.icon = ''
                left_btn.on_release = lambda btn=left_btn: self.navigate_back(btn)
                right_btn.disabled = True
            case const.ADD_DATA_SCR:
                top_bar_title.text = 'Add data'
                left_btn.icon = 'arrow-left'
                right_btn.icon = ''
                left_btn.on_release = lambda btn=left_btn: self.navigate_back(btn)
                right_btn.disabled = True
            case const.PROD_SCR:
                left_btn.icon = 'arrow-left'
                left_btn.on_release = lambda btn=left_btn: self.navigate_back(btn)
                right_btn.icon = ''
                right_btn.disabled = True

    def change_screen(self, screen_name):
        self.screen_stack.append(screen_name)
        self.sm.transition.direction = 'left'
        self.sm.current = self.screen_stack[-1]

    def navigate_back(self, *args):
        self.screen_stack = self.screen_stack[:-1]
        self.sm.transition.direction = 'right'
        self.sm.current = self.screen_stack[-1]
        self.update_top_bar()

    def change_screen_and_update_bar(self, screen_name):
        self.change_screen(screen_name)
        self.update_top_bar()

    def change_login_app_screen(self, screen_name):
        self.sm.transition = SwapTransition()
        self.change_screen(screen_name)
        self.sm.transition = SlideTransition()
        self.update_top_bar()

    def change_screen_to_prod_scr(self, product_id):
        prod_screen = self.sm.get_screen(const.PROD_SCR)
        prod_screen.incoming_prod_id = product_id
        self.change_screen(const.PROD_SCR)
        self.update_top_bar()

    def change_screen_to_list_scr(self, list_id):
        list_screen = self.sm.get_screen(const.LIST_SCR)
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
        self.nav_drawer.set_state('close')
        self.top_bar.disabled = True
        self.sm.transition = SwapTransition()
        self.change_screen(const.USER_MANAGER_SCREEN)
        self.sm.transition = SlideTransition()

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
