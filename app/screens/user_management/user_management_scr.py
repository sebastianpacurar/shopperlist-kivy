from kivy.clock import Clock
from kivy.properties import DictProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from app.components.components import db, SimpleSnackbar
from app.utils import constants as const


class UserManagerScreen(MDScreen):
    top_bar = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.tabs = None
        self.bind(on_kv_post=self.init_login_screen)

    def set_definitions(self, *args):
        self.sm = self.ids.signin_signup_manager
        self.tabs = self.ids.tabs

    def init_login_screen(self, *args):
        self.set_definitions()
        self.top_bar.disabled = True
        Clock.schedule_once(self.switch_to_first_tab, .025)

    def switch_to_first_tab(self, dt):
        login_tab = self.tabs.get_tabs_list()[-1]
        self.ids.tabs.switch_tab(instance=login_tab)

    def switch_scr(self, *args):
        tab_item = args[1]
        if tab_item.children[0].text == 'Log in':
            curr = const.LOGIN_SCR
        else:
            curr = const.REGISTER_SCR
        if self.sm.current != curr:
            match curr:
                case const.LOGIN_SCR:
                    self.sm.transition.direction = 'right'
                    self.sm.current = const.LOGIN_SCR
                case const.REGISTER_SCR:
                    self.sm.transition.direction = 'left'
                    self.sm.current = const.REGISTER_SCR


class LoginScr(MDScreen):
    top_bar = ObjectProperty()
    user_data = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_app = MDApp.get_running_app()
        self.enter_user = None
        self.enter_pass = None
        self.bind(on_kv_post=self.set_definitions)

    def set_definitions(self, *args):
        self.enter_user = self.ids.enter_user
        self.enter_pass = self.ids.enter_pass

    def perform_login(self):
        if self.validate_sign_in(self.enter_user, self.enter_pass.text_value):
            self.main_app.set_app_user(self.user_data)
            self.main_app.change_login_app_screen(const.COLLECTION_SCR)

    def validate_sign_in(self, user, password):
        entry = [user.text.strip(), password]
        if any([len(x) == 0 for x in entry]):
            SimpleSnackbar(text='There are errors in the fields', color=const.RGB_ERROR)
            return False
        else:
            self.user_data = db.get_login_user(entry[0], entry[1])
            self.top_bar.disabled = False
            return len(self.user_data) > 0


class RegisterScr(MDScreen):
    top_bar = ObjectProperty()
    user_data = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_app = MDApp.get_running_app()
        self.created_email = None
        self.created_user = None
        self.created_pass = None
        self.bind(on_kv_post=self.set_definitions)

    def set_definitions(self, *args):
        self.created_user = self.ids.create_user
        self.created_email = self.ids.create_email
        self.created_pass = self.ids.create_pass

    def perform_register(self):
        if self.validate_sign_up(self.created_user, self.created_email, self.created_pass.text_value):
            self.main_app.set_app_user(self.user_data)
            self.main_app.change_login_app_screen(const.COLLECTION_SCR)

    def validate_sign_up(self, user, email, password):
        entry = [user.text.strip(), email.text.strip(), password]
        if any([len(x) == 0 for x in entry]):
            SimpleSnackbar(text='There are errors in the fields', color=const.RGB_ERROR)
            return False
        else:
            self.user_data = db.add_user(entry[0], entry[1], entry[2])
            self.top_bar.disabled = False
            return len(self.user_data) > 0
