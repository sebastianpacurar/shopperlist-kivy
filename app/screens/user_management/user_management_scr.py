from kivy.properties import StringProperty, DictProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen

from app.components.components import db, SimpleSnackbar

success_color = (0, .65, 0, 1)
error_color = (.65, 0, 0, 1)


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
        password = args[1].ids.text_field
        entry = [user.text.strip(), password.text.strip()]
        if any([user.error, password.error]) or any([len(x) == 0 for x in entry]):
            SimpleSnackbar(text='There are errors in the fields', color=error_color)
            return False
        else:
            self.user_data = db.get_login_user(entry[0], entry[1])
            return len(self.user_data) > 0


class RegisterScr(MDScreen):
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
            return len(self.user_data) > 0


class PasswordField(MDRelativeLayout):
    hint_txt = StringProperty()
    value = StringProperty()
