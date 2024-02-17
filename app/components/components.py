from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.list import OneLineAvatarListItem, TwoLineRightIconListItem, ThreeLineRightIconListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar.toolbar import ActionTopAppBarButton

from db.database import Database, SQLITE, MYSQL

# This is where the DB first gets instantiated
db = Database(SQLITE)


class MainScreen(MDScreen):
    pass


class AddShoppingListContent(MDBoxLayout):
    pass


class EditableTwoLineItemList(TwoLineRightIconListItem):
    itm_icon = StringProperty()


class EditableThreeLineItemList(ThreeLineRightIconListItem):
    itm_icon = StringProperty()


class ProdItemWithImg(OneLineAvatarListItem):
    img_path = StringProperty()


class RV(MDRecycleView):
    pass


class MySnackbar(MDSnackbar):
    text = StringProperty('')
    font_size = NumericProperty('15sp')
    bold_text = BooleanProperty(False)

    def __init__(self, db_res, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Success' if db_res else 'Failure'
        self.md_bg_color = (0, .65, 0, 1) if db_res else (.65, 0, 0, 1)
        self.bold_text = True
        self.show()

    def show(self):
        self.open()

    def dismiss_sb(self):
        self.dismiss()


class DropdownHandler(MDDropdownMenu):
    def __init__(self, app_instance):
        super().__init__(
            width_mult=4,
            radius=[12, 12, 12, 12],
            position='center',
            elevation=4,
        )
        self.app_instance = app_instance

    def toggle(self, widget):
        data = None
        menu_items = []
        self.caller = widget

        # trigger items belonging to a specific table column
        if isinstance(widget, MDTextField):
            if widget.hint_text == 'Category':
                data = db.get_product_categories()
            elif widget.hint_text == 'Unit':
                data = db.get_product_units()

            for entry in data:
                menu_items.append(
                    {
                        'viewclass': 'OneLineListItem',
                        'text': entry[1],
                        'on_release': lambda item=entry: self.on_dropdown_item_select(widget, item)
                    }
                )
        # trigger items which trigger options from the ActionTopAppBarButton
        elif isinstance(widget, ActionTopAppBarButton):
            menu_items = [
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'Add product',
                    'on_release': lambda target='add_prod_scr': (
                        self.app_instance.change_screen(target), self.dismiss())
                },
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'Add Category',
                    'on_release': lambda target='add_category_scr': (
                        self.app_instance.change_screen(target), self.dismiss())
                },
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'Add Unit',
                    'on_release': lambda target='add_unit_scr': (
                        self.app_instance.change_screen(target), self.dismiss())
                }
            ]

        self.items = menu_items
        self.open()

    def on_dropdown_item_select(self, text_input, content):
        """ perform menu_item selection and update the caller text value """
        text_input.text = str(content[1])
        self.dismiss()
