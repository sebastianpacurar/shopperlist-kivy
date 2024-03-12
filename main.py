from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition, SwapTransition
from kivymd.uix.screen import MDScreen

import app.components.components
from app.components.components import *
from app.utils import constants as const
from db import operations as ops
from setup.setup_sqlite import setup_sqlite_db

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


class MainScreen(MDScreen):
    pass


class MyKivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_sqlite_db()
        self.screen_stack = []
        self.sm = None
        self.top_bar = None
        self.nav_drawer = None
        self.bottom = None
        self.user = {}

    def build(self):
        self.theme_cls.primary_palette = 'Lightblue'
        self.theme_cls.theme_style = 'Light'

    def on_start(self):
        self.nav_drawer = self.root.ids.nav_drawer
        self.sm = self.root.ids.scr_manager
        self.top_bar = self.root.ids.top_bar
        self.bottom = self.root.ids.bottom_sheet
        self.auto_login()
        super().on_start()

    def auto_login(self):
        data = db.user_auto_login()
        if len(data) > 0:
            self.user = data
            self.top_bar.disabled = False
            self.change_screen_and_update_bar(const.COLLECTION_SCR)
        else:
            self.change_screen(const.USER_MANAGER_SCR)

    def show_dialog(self, *args):
        content = args[0]
        dialog = DynamicDialog(MDDialogContentContainer(content))
        match type(content):
            case app.components.components.AddShoppingListContent:
                field = content.ids.text_field
                dialog.confirm = lambda f=field: ops.perform_list_add(dialog, f, self.user['id'])
                dialog.headline = 'New List'
                dialog.accept_txt = 'Add'
                dialog.cancel_txt = 'Cancel'
            case app.components.components.RenameShoppingListContent:
                field = content.ids.text_field
                dialog.confirm = lambda f=field: ops.perform_update_list_name(dialog, f, args[1])
                dialog.headline = 'Rename List'
                dialog.accept_txt = 'Update'
                dialog.cancel_txt = 'Cancel'
            case app.components.components.DeleteShoppingListContent:
                dialog.confirm = lambda: ops.perform_delete_list(dialog, args[1], args[2])
                dialog.headline = 'Delete List'
                dialog.supporting = 'Are you sure you want to delete list?'
                dialog.accept_txt = 'Yes'
                dialog.cancel_txt = 'No'
            case app.components.components.RenameCategoryContent:
                field = content.ids.text_field
                dialog.confirm = lambda f=field: ops.perform_update_category_name(dialog, f, args[1])
                dialog.headline = 'Rename Category'
                dialog.accept_txt = 'Update'
                dialog.cancel_txt = 'Cancel'
            case app.components.components.DeleteCategoryContent:
                dialog.confirm = lambda: ops.perform_delete_category(dialog, args[1], args[2])
                dialog.headline = 'Delete Category'
                dialog.supporting = 'Are you sure you want to delete Category?'
                dialog.accept_txt = 'Yes'
                dialog.cancel_txt = 'No'
            case app.components.components.RenameUnitContent:
                field = content.ids.text_field
                dialog.confirm = lambda f=field: ops.perform_update_unit_name(dialog, f, args[1])
                dialog.headline = 'Rename Unit'
                dialog.accept_txt = 'Update'
                dialog.cancel_txt = 'Cancel'
            case app.components.components.DeleteUnitContent:
                dialog.confirm = lambda: ops.perform_delete_unit(dialog, args[1], args[2])
                dialog.headline = 'Delete Unit'
                dialog.supporting = 'Are you sure you want to delete Unit?'
                dialog.accept_txt = 'Yes'
                dialog.cancel_txt = 'No'
            case app.components.components.RemoveProductFromListContent:
                dialog.confirm = lambda: ops.perform_list_item_remove(dialog, args[1], args[2])
                dialog.headline = 'Remove Item from List'
                dialog.supporting = 'Are you sure you want to remove item?'
                dialog.accept_txt = 'Yes'
                dialog.cancel_txt = 'No'
        dialog.open()

    def toggle_bottom(self, *args):
        if self.bottom.state == 'close':
            self.bottom.set_state('toggle')
            self.bottom.enable_swiping = True
            handle = self.root.ids.handle
            list_content = self.root.ids.content_list
            handle.title = args[0]
            for widget in args[-1]:
                list_content.add_widget(widget)

    def clean_bottom_sheet(self):
        self.bottom.enable_swiping = False
        self.root.ids.handle.text = ''
        self.root.ids.content_list.clear_widgets()

    def open_navbar(self, *args):
        self.nav_drawer.set_state('open')

    def close_bottom(self, *args):
        self.bottom.set_state('close')

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
                right_btn.on_release = lambda btn=right_btn: DropdownMenu().drop(btn)
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
                right_btn.on_release = lambda: self.change_screen_and_update_bar(const.ADD_TO_LIST_SCR)
                right_btn.icon = 'plus-thick'
                right_btn.disabled = False
            case const.ADD_PROD_SCR:
                top_bar_title.text = 'Add product'
                left_btn.icon = 'arrow-left'
                right_btn.icon = ''
                left_btn.on_release = lambda btn=left_btn: self.navigate_back(btn)
                right_btn.disabled = True
            case const.MANAGE_DATA_SCR:
                top_bar_title.text = 'Manage Data'
                left_btn.icon = 'arrow-left'
                right_btn.icon = ''
                left_btn.on_release = lambda btn=left_btn: self.navigate_back(btn)
                right_btn.disabled = True
            case const.PROD_SCR:
                left_btn.icon = 'arrow-left'
                left_btn.on_release = lambda btn=left_btn: self.navigate_back(btn)
                right_btn.icon = ''
                right_btn.disabled = True
            case const.SINGLE_CATEGORY_SCR:
                top_bar_title.text = 'Category'
                left_btn.icon = 'arrow-left'
                left_btn.on_release = lambda btn=left_btn: self.navigate_back(btn)
                right_btn.icon = ''
                right_btn.disabled = True
            case const.SINGLE_UNIT_SCR:
                top_bar_title.text = 'Unit'
                left_btn.icon = 'arrow-left'
                left_btn.on_release = lambda btn=left_btn: self.navigate_back(btn)
                right_btn.icon = ''
                right_btn.disabled = True
            case const.ADD_TO_LIST_SCR:
                top_bar_title.text = 'Add to List'
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

    def change_screen_to_category_scr(self, category_id):
        self.sm.get_screen(const.SINGLE_CATEGORY_SCR).incoming_category_id = category_id
        self.change_screen(const.SINGLE_CATEGORY_SCR)
        self.update_top_bar()

    def change_screen_to_unit_scr(self, unit_id):
        self.sm.get_screen(const.SINGLE_UNIT_SCR).incoming_unit_id = unit_id
        self.change_screen(const.SINGLE_UNIT_SCR)
        self.update_top_bar()

    def change_login_app_screen(self, screen_name):
        self.sm.transition = SwapTransition()
        self.change_screen(screen_name)
        self.sm.transition = SlideTransition()
        self.update_top_bar()

    def change_screen_to_prod_scr(self, product_id):
        self.sm.get_screen(const.PROD_SCR).incoming_prod_id = product_id
        self.change_screen(const.PROD_SCR)
        self.update_top_bar()

    def change_screen_to_list_scr(self, list_id):
        self.sm.get_screen(const.LIST_SCR).list_id = list_id
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
        self.change_screen(const.USER_MANAGER_SCR)
        self.sm.get_screen(const.USER_MANAGER_SCR).init_login_screen()
        self.sm.transition = SlideTransition()


if __name__ == '__main__':
    Window.size = (360, 640)
    MyKivyApp().run()
