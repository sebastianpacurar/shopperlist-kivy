import os

from kivy.metrics import sp
from kivy.properties import StringProperty, ColorProperty, NumericProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarActionButton
from kivymd.uix.list import OneLineAvatarListItem, TwoLineRightIconListItem, ThreeLineRightIconListItem, \
    TwoLineAvatarIconListItem, IconRightWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar.toolbar import ActionTopAppBarButton

from db.database import Database, SQLITE, MYSQL

# This is where the DB gets instantiated
db = Database(SQLITE)

kv_file = os.path.join(os.path.dirname(__file__), 'components.kv')


class RV(MDRecycleView):
    pass


class EditableTwoLineItemList(TwoLineRightIconListItem):
    itm_icon = StringProperty()


class EditableThreeLineItemList(ThreeLineRightIconListItem):
    itm_icon = StringProperty()


class ProdItemWithImg(OneLineAvatarListItem):
    img_path = StringProperty()


class TwoLineProdImgListItem(TwoLineAvatarIconListItem):
    prod_id = NumericProperty()
    img_path = StringProperty()
    itm_icon = StringProperty()
    image_func = ObjectProperty()
    icon_func = ObjectProperty()


class AddShoppingListContent(MDBoxLayout):
    def get_field_validation(self):
        return self.ids.shop_list_name_text.error


class Spacer(MDBoxLayout):
    value = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_kv_post=self.init_spacer)

    def init_spacer(self, *args):
        if self.orientation == 'vertical':
            self.size_hint_y = None
            self.height = self.value
        else:
            self.size_hint_x: None
            self.width = self.value


class SimpleSnackbar(MDSnackbar):
    text = StringProperty()
    color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show()

    def show(self):
        self.open()


class MySnackbar(MDSnackbar):
    text = StringProperty('')

    def __init__(self, message, db_res, **kwargs):
        super().__init__(**kwargs)
        self.main_app = MDApp.get_running_app()
        self.text = message
        self.md_bg_color = (0, .65, 0, 1) if db_res else (.65, 0, 0, 1)
        self.show()

        if db_res:
            response, val_id, screen_name = db_res
            if response and screen_name:
                func = None
                match screen_name:
                    case 'list_content_scr':
                        func = lambda _: (self.main_app.change_screen_to_list_scr(val_id), self.dismiss_sb())
                    case 'prod_scr':
                        func = lambda _: (self.main_app.change_screen_to_prod_scr(val_id), self.dismiss_sb())

                item = MDSnackbarActionButton(
                    text='View',
                    theme_text_color='Custom',
                    text_color='white',
                    font_size=sp(17.5),
                    on_release=func
                )

            self.add_widget(item)

    def show(self):
        self.open()

    def dismiss_sb(self):
        self.dismiss()


class DropdownHandler(MDDropdownMenu):
    change_screen_func = ObjectProperty

    def __init__(self):
        super().__init__(
            width_mult=4,
            radius=[12, 12, 12, 12],
            elevation=4,
        )
        self.parent_caller = None
        self.main_app = MDApp.get_running_app()

    def on_dismiss(self):
        super().on_dismiss()
        if isinstance(self.caller, IconRightWidget):
            self.parent_caller.bg_color = 'white'

    def toggle(self, widget):
        data = None
        menu_items = []
        self.caller = widget

        # trigger items belonging to a specific table column
        if isinstance(widget, MDTextField):
            self.hor_growth = 'left'
            self.ver_growth = 'down'
            self.position = 'center'

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
                        self.main_app.change_screen_and_update_bar(target), self.dismiss())
                },
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'Add Data',
                    'on_release': lambda target='add_data_scr': (
                        self.main_app.change_screen_and_update_bar(target), self.dismiss())
                },
            ]

        elif isinstance(widget, TwoLineProdImgListItem):
            widget.bg_color = self.theme_cls.primary_light
            self.parent_caller = widget
            self.caller = widget.children[0].children[0]
            prod_id = self.parent_caller.prod_id

            menu_items = [
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'View',
                    'on_release': lambda target=prod_id: (
                        self.main_app.change_screen_to_prod_scr(target),
                        self.dismiss()
                    )

                },
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'Delete',
                    'on_release': lambda target=prod_id: (
                        print('delete me?'),
                        self.dismiss()
                    )
                }
            ]

        self.items = menu_items
        self.open()

    def on_dropdown_item_select(self, text_input, content):
        """ perform menu_item selection and update the caller text value """
        text_input.text = str(content[1])
        self.dismiss()
