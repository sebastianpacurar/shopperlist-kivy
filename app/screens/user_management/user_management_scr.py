from kivy.properties import StringProperty, DictProperty, ObjectProperty
from kivy.uix.screenmanager import FadeTransition, SlideTransition
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen

from app.components.components import db, SimpleSnackbar

success_color = (0, .65, 0, 1)
error_color = (.65, 0, 0, 1)


class UserManagerScreen(MDScreen):
    top_bar = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login = 'log_in_scr'
        self.register = 'register_scr'
        self.bind(on_kv_post=self.init_login_screen)
        self.bind(on_pre_leave=self.set_back_to_login)

    def init_login_screen(self, *args):
        self.top_bar.disabled = True
        login_btn = self.ids.login_btn
        register_btn = self.ids.register_btn
        login_btn.disabled = True
        register_btn.disabled = False

    def set_back_to_login(self, *args):
        login_btn = self.ids.login_btn
        register_btn = self.ids.register_btn
        sm = self.ids.signin_signup_manager
        if sm.current == self.register:
            sm.transition = FadeTransition()
            sm.current = self.login
            login_btn.disabled = True
            register_btn.disabled = False
            sm.transition = SlideTransition()

    def switch_scr(self, *args):
        login_btn = self.ids.login_btn
        register_btn = self.ids.register_btn
        sm = self.ids.signin_signup_manager

        selection_text = args[0].text.lower().replace(' ', '_')

        if self.login.startswith(selection_text):
            sm.transition.direction = 'right'
            sm.current = self.login
            login_btn.disabled = True
            register_btn.disabled = False
            login_btn.bold = False
            register_btn.bold = True

        elif self.register.startswith(selection_text):
            sm.transition.direction = 'left'
            sm.current = self.register
            login_btn.disabled = False
            register_btn.disabled = True
            login_btn.bold = True
            register_btn.bold = False


class LoginScr(MDScreen):
    top_bar = ObjectProperty()
    user_data = DictProperty()

    def sign_in(self, *args):
        user = args[0]
        password = args[1].ids.text_field
        entry = [user.text.strip(), password.text.strip()]
        if any([user.error, password.error]) or any([len(x) == 0 for x in entry]):
            SimpleSnackbar(text='There are errors in the fields', color=error_color)
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
            SimpleSnackbar(text='There are errors in the fields', color=error_color)
            return False
        else:
            self.user_data = db.add_user(entry[0], entry[1], entry[2])
            self.top_bar.disabled = False
            return len(self.user_data) > 0


class PasswordField(MDRelativeLayout):
    hint_txt = StringProperty()
    value = StringProperty()
