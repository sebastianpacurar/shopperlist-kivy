from kivy.uix.widget import Widget
from kivymd.uix.appbar import MDActionTopAppBarButton
from kivymd.uix.bottomsheet import MDBottomSheetDragHandle
from kivymd.uix.dialog import MDDialog, MDDialogContentContainer
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.snackbar import MDSnackbarButtonContainer, MDSnackbarActionButtonText, MDSnackbarSupportingText, \
    MDSnackbarCloseButton
from kivy.metrics import sp, dp
from kivy.properties import StringProperty, ColorProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarActionButton
from kivymd.uix.list import MDListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from db.database import Database, SQLITE, MYSQL
from app.utils import constants as const

# This is where the DB gets instantiated
db = Database(SQLITE)


class RV(MDRecycleView):
    pass


class TopGap(Widget):
    top_bar_height = NumericProperty()


class BottomGap(Widget):
    pass


class SimpleTextField(MDTextField):
    hint_txt = StringProperty()
    helper_txt = StringProperty()


class PasswordField(MDRelativeLayout):
    field_mode = StringProperty('outlined')
    hint_txt = StringProperty()
    is_hidden = BooleanProperty(False)  # used in toggle_visibility when clicking eye icon
    skip = BooleanProperty(False)  # used to cancel save_text_value during on_text after setting/unsetting text to symbols
    text_value = StringProperty()  # the actual literal value
    masked_text = StringProperty()  # the literal value masked

    # set text_value and masked_text vars. triggered on set_text
    def save_text_value(self, *args):
        args[0].text = args[0].text.replace(' ', '')  # prevent whitespaces
        if len(args[0].text) > 0:
            if not self.skip or (len(args[0].text) == 1 and self.is_hidden):  # update vars only if not marked as skip and if is first element while is_hidden is True
                if len(args[0].text) < len(self.text_value):  # trigger if erase/delete event occurs
                    diff = len(self.text_value) - len(args[0].text)  # TODO: handle multi-select delete
                    self.text_value = self.text_value[:-diff]
                elif args[0].text[-1] != '*':  # if last typed element is not a star, add it to text_value var
                    self.text_value += args[0].text[-1]
                self.masked_text = '*' * len(self.text_value)

            if self.is_hidden:  # if is_hidden is on, change the text, and mark as Skipped, to prevent re-trigger of save_text_value func
                args[0].text = self.masked_text
                self.skip = True
            if self.skip:  # skip happens only once, after eye icon is toggled
                self.skip = False
        else:  # if field is empty, then reset vars
            self.masked_text = ''
            self.text_value = ''

    # enable/disable masked pass. set skip to prevent re-trigger of save_text_value, when resetting text_field text value
    def toggle_visibility(self, *args):
        icon_btn = args[0]
        self.is_hidden = not self.is_hidden
        self.skip = not self.skip
        if self.is_hidden:
            icon_btn.icon = 'eye-off'
            args[1].text = self.masked_text
        else:
            icon_btn.icon = 'eye'
            args[1].text = self.text_value


class DropTextField(MDTextField):
    hint_txt = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    def text_validate(self):
        if self.text in self.data:
            self.text = self.text.strip()
        elif len(self.text) > 1:
            self.text = ''

    def on_focus_event(self):
        if self.focus:
            self.text = ''
            db_op = None
            if self.hint_txt == 'Category':
                db_op = db.get_product_categories()
            elif self.hint_txt == 'Unit':
                db_op = db.get_product_units()
            self.data = [entry[1] for entry in db_op]
            DropdownMenu().drop(self)


class FilterTextField(MDBoxLayout):
    hint_txt = StringProperty()
    filter_prefix = StringProperty()
    filter_suffix = StringProperty()
    prefix_width = NumericProperty()
    clear_filter_func = ObjectProperty()
    clear_btn_disabled = BooleanProperty(False)

    def handle_clear_btn(self):
        drop_text = self.ids.text_field
        if drop_text.text in drop_text.data:
            self.clear_btn_disabled = False
        else:
            self.clear_btn_disabled = True


class DropdownMenu(MDDropdownMenu):
    def __init__(self):
        super().__init__(
            padding=[dp(12), 0, dp(12), 0],
            radius=[12, 12, 12, 12],
            elevation=4,
        )
        self.main_app = MDApp.get_running_app()

    def on_dismiss(self):
        super().on_dismiss()
        curr_scr = self.main_app.sm.current

        if curr_scr == const.LIST_SCR:
            list_scr = self.main_app.sm.get_screen(const.LIST_SCR)
            if self.caller.text in self.caller.data:
                list_scr.update_filtered_category(self.caller.text)
            else:
                list_scr.update_filtered_category('All Categories')
            list_scr.refresh_data()

    def on_dropdown_item_select(self, text_input, content):
        text_input.text = str(content)
        self.dismiss()

    def drop(self, widget):
        menu_items = []
        curr_scr = self.main_app.sm.current
        self.caller = widget

        if isinstance(self.caller, DropTextField):
            self.ver_growth = 'down'
            self.position = 'bottom' if curr_scr == const.LIST_SCR else 'center'

            for entry in self.caller.data:
                menu_items.append(
                    {
                        'text': entry,
                        'on_release': lambda item=entry: self.on_dropdown_item_select(self.caller, item)
                    }
                )
        elif isinstance(self.caller, MDActionTopAppBarButton):
            menu_items = [
                {
                    'text': 'Add product',
                    'on_release': lambda screen=const.ADD_PROD_SCR: (
                        self.main_app.change_screen_and_update_bar(screen),
                        self.dismiss()
                    )
                },
                {
                    'text': 'Manage Data',
                    'on_release': lambda screen=const.MANAGE_DATA_SCR: (
                        self.main_app.change_screen_and_update_bar(screen),
                        self.dismiss()
                    )
                },
            ]

        self.items = menu_items
        self.open()


class EditableTwoLineItemList(MDListItem):
    itm_id = StringProperty()
    headline = StringProperty()
    supporting = StringProperty()
    sheet_func = ObjectProperty()


class SelectableProdItemWithImg(MDListItem):
    headline = StringProperty()
    supporting = StringProperty()
    tertiary = StringProperty()
    itm_id = StringProperty()
    itm_icon = StringProperty()
    list_id = StringProperty()
    checkbox_func = ObjectProperty()
    sheet_func = ObjectProperty()


class BottomSheetItemDescription(MDBoxLayout):
    img_path = StringProperty()
    category = StringProperty()
    price = StringProperty()
    category_name = StringProperty()


class BottomSheetQuantitySelector(MDBoxLayout):
    quantity_val = NumericProperty()
    initial_quantity = NumericProperty()
    price_val = NumericProperty()
    unit_price = NumericProperty()
    apply_quantity_func = ObjectProperty()
    decrease_btn_disabled = BooleanProperty()
    apply_btn_disabled = BooleanProperty()

    def increase_quantity_val(self):
        self.quantity_val = self.quantity_val + 1
        self.price_val = self.unit_price * self.quantity_val
        if self.decrease_btn_disabled and self.price_val > 0:
            self.decrease_btn_disabled = False
        self.handle_apply_btn()

    def decrease_quantity_val(self):
        self.quantity_val = self.quantity_val - 1
        self.price_val = self.unit_price * self.quantity_val
        if self.quantity_val == 1:
            self.decrease_btn_disabled = True
        self.handle_apply_btn()

    def handle_apply_btn(self):
        if self.quantity_val == self.initial_quantity:
            self.apply_btn_disabled = True
        elif self.apply_btn_disabled:
            self.apply_btn_disabled = False


class ProdItemWithImg(MDListItem):
    img_path = StringProperty()
    headline = StringProperty()


class TwoLineProdImgListItem(MDListItem):
    headline = StringProperty()
    supporting = StringProperty()
    prod_id = NumericProperty()
    img_path = StringProperty()
    image_func = ObjectProperty()
    icon_func = ObjectProperty()


class SelectSignInSignUpButton(MDButton):
    text = StringProperty()


class BottomSheetSelectionLineItem(MDListItem):
    text = StringProperty()


class BottomSheetHandleContainer(MDBottomSheetDragHandle):
    title = StringProperty()


class DynamicDialog(MDDialog):
    confirm = ObjectProperty()
    headline = StringProperty()
    supporting = StringProperty()
    accept_txt = StringProperty()
    cancel_txt = StringProperty()
    should_refresh = BooleanProperty(False)

    def on_dismiss(self):
        super().on_dismiss()
        if self.should_refresh:
            main_sm = MDApp.get_running_app().sm
            if main_sm.current == const.COLLECTION_SCR:
                main_sm.get_screen(const.COLLECTION_SCR).refresh_data()
            if main_sm.current == const.MANAGE_DATA_SCR:
                inner_scr = main_sm.get_screen(const.MANAGE_DATA_SCR).sm
                inner_scr.get_screen(inner_scr.current).display_search_results()
            if main_sm.current == const.LIST_SCR:
                main_sm.get_screen(const.LIST_SCR).init_data()


class AddShoppingListContent(MDDialogContentContainer):
    pass


class RenameShoppingListContent(MDDialogContentContainer):
    pass


class DeleteShoppingListContent(MDDialogContentContainer):
    pass


class RemoveProductFromListContent(MDDialogContentContainer):
    pass


class RenameCategoryContent(MDDialogContentContainer):
    pass


class DeleteCategoryContent(MDDialogContentContainer):
    pass


class RenameUnitContent(MDDialogContentContainer):
    pass


class DeleteUnitContent(MDDialogContentContainer):
    pass


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
        self.add_widget(MDSnackbarSupportingText(text=self.text))
        self.y = dp(24)
        self.orientation = 'horizontal'
        self.pos_hint = {'center_x': 0.5, 'y': 0}
        self.background_color = self.color
        self.open()


class MySnackbar(MDSnackbar):
    text = StringProperty()

    def __init__(self, message, db_res, **kwargs):
        super().__init__(**kwargs)
        self.main_app = MDApp.get_running_app()
        self.text = message
        self.background_color = const.RGB_SUCCESS if db_res else const.RGB_ERROR

        self.y = dp(24)
        self.orientation = 'horizontal'
        self.pos_hint = {'center_x': 0.5, 'y': 0}

        self.add_widget(MDSnackbarSupportingText(
            text=self.text,
            theme_text_color='Custom',
            theme_font_size='Custom',
            text_color='white',
            font_size=sp(15.5),
            bold=True
        ))

        bar_buttons = MDSnackbarButtonContainer(pos_hint={'center_y': .5})

        if isinstance(db_res, tuple):
            response, val_id, screen_name = db_res
            if response and screen_name:
                func = None
                match screen_name:
                    case const.LIST_SCR:
                        func = lambda _: (self.main_app.change_screen_to_list_scr(val_id), self.dismiss())
                    case const.PROD_SCR:
                        func = lambda _: (self.main_app.change_screen_to_prod_scr(val_id), self.dismiss())

                bar_buttons.add_widget(
                    MDSnackbarActionButton(
                        MDSnackbarActionButtonText(
                            text='View',
                            theme_text_color='Custom',
                            theme_font_size='Custom',
                            text_color='white',
                            font_size=sp(15.5),
                            bold=True,
                        ),
                        style='outlined',
                        theme_line_color='Custom',
                        line_color='white',
                        radius=(dp(5), dp(5), dp(5), dp(5)),
                        on_release=func
                    )
                )

        bar_buttons.add_widget(
            MDSnackbarCloseButton(
                icon='close',
                on_release=self.dismiss
            )
        )

        self.add_widget(bar_buttons)
        self.open()
