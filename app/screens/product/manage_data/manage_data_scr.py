from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from app.components.components import db, MySnackbar, BottomSheetSelectionLineItem, \
    RenameCategoryContent, DeleteCategoryContent, RenameUnitContent, DeleteUnitContent
from app.utils import constants as const


class ManageDataScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.text_field = None
        self.search_field = None
        self.add_btn = None
        self.bind(on_kv_post=self.set_definitions)

    def set_definitions(self, *args):
        self.text_field = self.ids.text_field
        self.search_field = self.ids.search_field
        self.add_btn = self.ids.add_btn
        self.sm = self.ids.data_manager
        self.sm.get_screen(const.PROD_CATEGORIES_SCR).display_search_results()
        self.sm.get_screen(const.PROD_UNITS_SCR).display_search_results()

    def reset_fields(self):
        self.text_field.text = ''
        self.search_field.text = ''

    def switch_scr(self, *args):
        if self.sm.current != args[0]:
            match args[0]:
                case const.PROD_CATEGORIES_SCR:
                    self.sm.transition.direction = 'right'
                    self.sm.current = const.PROD_CATEGORIES_SCR
                    self.sm.get_screen(const.PROD_CATEGORIES_SCR).display_search_results()
                    self.reset_fields()
                case const.PROD_UNITS_SCR:
                    self.sm.transition.direction = 'left'
                    self.sm.current = const.PROD_UNITS_SCR
                    self.sm.get_screen(const.PROD_UNITS_SCR).display_search_results()
                    self.reset_fields()

    def add_entity(self):
        msg, db_result = 'Cannot be empty', 0
        if len(self.text_field.text) > 0:
            match self.sm.current:
                case const.PROD_CATEGORIES_SCR:
                    msg = f'Cannot add {self.text_field.text} Category'
                    db_result = db.add_category(self.text_field.text)
                    if db_result:
                        msg = f'{self.text_field.text} Category added'
                        self.sm.get_screen(const.PROD_CATEGORIES_SCR).display_search_results()
                        self.reset_fields()
                case const.PROD_UNITS_SCR:
                    msg = f'Cannot add {self.text_field.text} Unit'
                    db_result = db.add_unit(self.text_field.text)
                    if db_result:
                        msg = f'{self.text_field.text} unit added'
                        self.sm.get_screen(const.PROD_UNITS_SCR).display_search_results()
                        self.reset_fields()
        MySnackbar(msg, db_result)

    def filter_displayed_list(self, *args):
        self.sm.get_screen(self.sm.current).display_search_results(args[0])


class BaseAddScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_app = MDApp.get_running_app()

    def create_item_data(self, entry):
        entry = [str(x) for x in entry]
        sheet_content = set_bottom_sheet_content(self.main_app, self.name, entry[0], entry[1])
        return {
            'itm_id': str(entry[0]),
            'text': entry[1],
            'itm_icon': 'dots-vertical',
            'sheet_func': lambda name=entry[1], cat_id=entry[0]: self.main_app.toggle_bottom(name, cat_id, sheet_content),
        }


class CategoriesScreen(BaseAddScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_search_results(self, *args):
        prefix_str = '' if len(args) == 0 else args[0].text
        rv_data = []
        for entry in db.filter_categories(prefix_str):
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)
        self.ids.rv_categories.data = rv_data


class UnitsScreen(BaseAddScreen):
    def __init(self, **kwargs):
        super().__init__(**kwargs)

    def display_search_results(self, *args):
        prefix_str = '' if len(args) == 0 else args[0].text
        rv_data = []
        for entry in db.filter_units(prefix_str):
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)
        self.ids.rv_units.data = rv_data


def set_bottom_sheet_content(main_app, screen, entity_id, entity_name):
    rename_widget = RenameCategoryContent if screen == const.PROD_CATEGORIES_SCR else RenameUnitContent
    delete_widget = DeleteCategoryContent if screen == const.PROD_CATEGORIES_SCR else DeleteUnitContent
    screen_change = main_app.change_screen_to_category_scr if screen == const.PROD_CATEGORIES_SCR else main_app.change_screen_to_unit_scr

    return [
        BottomSheetSelectionLineItem(
            text='View Products',
            on_release=lambda _: (
                screen_change(entity_id),
                main_app.bottom.set_state('toggle')),
        ),
        BottomSheetSelectionLineItem(
            text='Rename',
            on_release=lambda _: (
                main_app.show_dialog(rename_widget(), entity_id),
                main_app.bottom.set_state('toggle')),
        ),
        BottomSheetSelectionLineItem(
            text='Delete',
            on_release=lambda _: (
                main_app.show_dialog(delete_widget(), entity_name, entity_id),
                main_app.bottom.set_state('toggle')),
        )
    ]
