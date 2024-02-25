from kivy.properties import StringProperty, DictProperty, ObjectProperty
from kivy.uix.screenmanager import FadeTransition, SlideTransition
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen

from app.components.components import db, SimpleSnackbar
from app.utils import constants as const


class UserManagerScreen(MDScreen):
    top_bar = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.login_btn = None
        self.register_btn = None
        self.bind(on_kv_post=self.init_login_screen)
        self.bind(on_pre_leave=self.set_back_to_login)

    def set_definitions(self, *args):
        self.login_btn = self.ids.login_btn
        self.register_btn = self.ids.register_btn
        self.sm = self.ids.signin_signup_manager

    def init_login_screen(self, *args):
        self.set_definitions()
        self.top_bar.disabled = True
        self.login_btn.disabled = True
        self.register_btn.disabled = False

    def set_back_to_login(self, *args):
        if self.sm.current == const.REGISTER_SCR:
            self.sm.transition = FadeTransition()
            self.sm.current = const.LOGIN_SCR
            self.login_btn.disabled = True
            self.register_btn.disabled = False
            self.sm.transition = SlideTransition()

    def switch_scr(self, *args):
        selection_text = args[0].text.lower().replace(' ', '_')  # stupid hack for bad screen naming
        if const.LOGIN_SCR.startswith(selection_text):
            self.sm.transition.direction = 'right'
            self.sm.current = const.LOGIN_SCR
            self.login_btn.disabled = True
            self.register_btn.disabled = False
            self.login_btn.bold = False
            self.register_btn.bold = True

        elif const.REGISTER_SCR.startswith(selection_text):
            self.sm.transition.direction = 'left'
            self.sm.current = const.REGISTER_SCR
            self.login_btn.disabled = False
            self.register_btn.disabled = True
            self.login_btn.bold = True
            self.register_btn.bold = False


class LoginScr(MDScreen):
    top_bar = ObjectProperty()
    user_data = DictProperty()

    def sign_in(self, *args):
        user = args[0]
        password = args[1].ids.text_field
        entry = [user.text.strip(), password.text.strip()]
        if any([user.error, password.error]) or any([len(x) == 0 for x in entry]):
            SimpleSnackbar(text='There are errors in the fields', color=const.RGB_ERROR)
            return False
        else:
            self.user_data = db.get_login_user(entry[0], entry[1])
            self.top_bar.disabled = False
            return len(self.user_data) > 0


class RegisterScr(MDScreen):
    top_bar = ObjectProperty()
    user_data = DictProperty()

    def sign_up(self, *args):
        user, email = args[0], args[1]
        password = args[2].ids.text_field
        entry = [user.text.strip(), email.text.strip(), password.text.strip()]
        if any([email.error, user.error, password.error]) or any([len(x) == 0 for x in entry]):
            SimpleSnackbar(text='There are errors in the fields', color=const.RGB_ERROR)
            return False
        else:
            self.user_data = db.add_user(entry[0], entry[1], entry[2])
            self.top_bar.disabled = False
            return len(self.user_data) > 0


class PasswordField(MDRelativeLayout):
    hint_txt = StringProperty()
    value = StringProperty()
