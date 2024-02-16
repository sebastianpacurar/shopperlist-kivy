from kivy.properties import StringProperty, DictProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen

from app.components.components import db


class UserManagerScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login = 'login_scr'
        self.register = 'register_scr'

    def switch_scr(self, *args):
        selection_text = args[0].text.lower()
        sm = self.ids.signin_signup_manager

        if self.login.startswith(selection_text):
            sm.transition.direction = 'right'
            sm.current = self.login
        elif self.register.startswith(selection_text):
            sm.transition.direction = 'left'
            sm.current = self.register


class LoginScr(MDScreen):
    user_data = DictProperty()

    def sign_in(self, *args):
        user = args[0]
        password = args[1]
        self.user_data = db.get_login_user(user, password)
        return len(self.user_data) > 0


class RegisterScr(MDScreen):
    user_data = DictProperty()

    def sign_up(self, *args):
        user, email = args[0], args[1]
        password = args[2].ids.text_field
        if any([email.error, user.error, password.error]):
            print('Handle text errors snackbar')
        else:
            self.user_data = db.add_user(user.text, email.text, password.text)
            return len(self.user_data) > 0


class PasswordField(MDRelativeLayout):
    hint_txt = StringProperty()
    value = StringProperty()
