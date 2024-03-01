from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db
from app.utils import constants as const


class AddDataScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.bind(on_kv_post=self.set_definitions)

    def set_definitions(self, *args):
        self.sm = self.ids.data_manager
        self.sm.get_screen(const.PROD_CATEGORY_SCR).display_all_categories()

    def switch_scr(self, *args):
        if self.sm.current != args[0]:
            match args[0]:
                case const.PROD_CATEGORY_SCR:
                    self.sm.transition.direction = 'right'
                    self.sm.current = const.PROD_CATEGORY_SCR
                    self.sm.get_screen(const.PROD_CATEGORY_SCR).display_all_categories()
                case const.PROD_UNIT_SCR:
                    self.sm.transition.direction = 'left'
                    self.sm.current = const.PROD_UNIT_SCR
                    self.sm.get_screen(const.PROD_UNIT_SCR).display_all_units()


class CategoryScr(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_all_categories(self, *args):
        rv_data = []
        for entry in db.get_product_categories():
            rv_data.append({'supporting': entry[1]})

        self.ids.rv_category.data = rv_data


class UnitScr(MDScreen):
    def __init(self, **kwargs):
        super().__init__(**kwargs)

    def display_all_units(self, *args):
        rv_data = []
        for entry in db.get_product_units():
            rv_data.append({'supporting': entry[1]})

        self.ids.rv_unit.data = rv_data
