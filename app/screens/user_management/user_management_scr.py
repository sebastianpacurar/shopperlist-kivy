from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen


class UserManagerScr(MDScreen):
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

        print(sm.current)


class LoginScr(MDScreen):
    def sign_in(self, *args):
        print(args)


class RegisterScr(MDScreen):
    def sign_up(self, *args):
        print(args)


class PasswordField(MDRelativeLayout):
    hint_txt = StringProperty()
    value = StringProperty()
