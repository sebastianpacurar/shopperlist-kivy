from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.recycleview import RecycleView
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarCloseButton
from kivymd.uix.list import OneLineAvatarListItem, TwoLineRightIconListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout


class MainScreen(MDScreen):
    pass


class ProductsScreen(MDScreen):
    pass


class CollectionScreen(MDScreen):
    pass


class ListScreen(MDScreen):
    pass


class ContentNavigationDrawer(MDScrollView):
    pass


class AddShoppingListContent(MDBoxLayout):
    pass


class AddProductScreen(MDScreen):
    pass


class EditableItemList(TwoLineRightIconListItem):
    itm_icon = StringProperty()


class ProdItemWithImg(OneLineAvatarListItem):
    img_path = StringProperty()


class RV(RecycleView):
    pass


class ShopListProduct(MDScrollView):
    text = StringProperty()


class MySnackbar(MDSnackbar):
    text = StringProperty(None)
    font_size = NumericProperty('15sp')
    bold_text = BooleanProperty(False)


def show_snackbar(db_result):
    sb = MySnackbar(
        MDSnackbarCloseButton(
            icon='close-thick',
            on_release=lambda _: sb.dismiss()
        ),
        text='Success' if db_result else 'Failure',
        bold_text=True,
        md_bg_color=(0, .65, 0, 1) if db_result else (.65, 0, 0, 1)
    )
    sb.open()


def on_dropdown_item_select(text_input, content, menu):
    text_input.text = str(content[1])
    menu.dismiss()
