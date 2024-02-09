from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget, IconRightWidget, IRightBodyTouch, \
    TwoLineRightIconListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarCloseButton

from app.Database import Database


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
    pass


class IconContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True
    spacing = NumericProperty('24dp')


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
            on_release=lambda x: sb.dismiss()
        ),
        text='Success' if db_result else 'Failure',
        bold_text=True,
        md_bg_color=(0, .65, 0, 1) if db_result else (.65, 0, 0, 1)
    )
    sb.open()


class MyKivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {
            'prod': {'entries': None, 'i': 0},
            'collection': {'entries': None, 'i': 0},
            'list': {'entries': None, 'i': 0}
        }
        self.dialog = None
        self.prev_screen = None
        self.db = Database()

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.theme_style = 'Light'

    def on_start(self):
        self.prev_screen = self.root.ids.scr_manager.current_screen.name
        self.update_top_bar()
        self.get_products()

    def show_dialog(self):
        content = AddShoppingListContent()

        if not self.dialog:
            self.dialog = MDDialog(
                type='custom',
                content_cls=content,
                on_dismiss=lambda _: self.clearDialog(),
                buttons=[
                    MDFlatButton(
                        text='Add',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda _: self.perform_shop_list_add(),
                    ),
                    MDFlatButton(
                        text='Cancel',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.error_color,
                        on_release=lambda _: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()

    def clearDialog(self):
        self.dialog = None

    def perform_product_add(self):
        name = self.root.ids.product_name_text.text
        price = self.root.ids.product_price_text.text
        category = self.root.ids.product_category_text.text
        unit = self.root.ids.product_unit_text.text
        db_result = self.db.add_product(name, price, unit, category)

        show_snackbar(db_result)

    def perform_shop_list_add(self):
        shop_list_name = self.dialog.content_cls.ids.shop_list_name_text.text
        db_result = self.db.add_shopping_list(shop_list_name)
        self.dialog.dismiss()
        show_snackbar(db_result)

    def update_top_bar(self):
        top_bar = self.root.ids.top_bar
        sm = self.root.ids.scr_manager
        nav_drawer = self.root.ids.nav_drawer
        match sm.current:
            case 'products_list_scr':
                top_bar.title = 'Products'
                top_bar.left_action_items = [['menu', lambda _: nav_drawer.set_state('open')]]
                top_bar.right_action_items = [['plus-thick', lambda _: self.change_screen('add_product_scr')]]
            case 'collection_scr':
                top_bar.title = 'Collections'
                top_bar.left_action_items = [['menu', lambda _: nav_drawer.set_state('open')]]
                top_bar.right_action_items = [['plus-thick', lambda _: self.show_dialog()]]
            case 'list_content_scr':
                top_bar.title = 'Shopping List'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = [['plus-thick', lambda _: print('show dialog for add item in list')]]
            case 'add_product_scr':
                top_bar.title = 'Add Product'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = []

    def navigate_back(self):
        sm = self.root.ids.scr_manager
        sm.current = self.prev_screen
        sm.transition.direction = 'right'
        self.update_top_bar()

    def change_screen(self, screen_name):
        sm = self.root.ids.scr_manager
        self.prev_screen = sm.current_screen.name
        sm.transition.direction = 'left'
        sm.current = screen_name
        self.update_top_bar()

    # issue here
    def get_products(self):
        self.data['prod']['entries'] = self.db.get_all_products()
        curr_scr = self.root.ids.scr_manager.current
        container_id = self.root.ids.prod_items
        container_id.clear_widgets()
        Clock.schedule_interval(
            lambda dt: self.thread_widget(dt, curr_scr, container_id, self.data['prod']),
            1 / 60)

    def get_collections(self):
        self.data['collection']['entries'] = self.db.get_shop_lists()
        curr_scr = self.root.ids.scr_manager.current
        container_id = self.root.ids.collection_id
        container_id.clear_widgets()
        Clock.schedule_interval(
            lambda dt: self.thread_widget(dt, curr_scr, container_id, self.data['collection']),
            1 / 60)

    def get_list_content(self, *args):
        self.change_screen('list_content_scr')
        list_id = args[0].id.split('_')[1]
        self.data['list']['entries'] = self.db.get_shop_list(list_id)
        curr_scr = self.root.ids.scr_manager.current
        container_id = self.root.ids.list_content_items
        container_id.clear_widgets()
        Clock.schedule_interval(
            lambda dt: self.thread_widget(dt, curr_scr, container_id, self.data['list']),
            1 / 60)

    def thread_widget(self, dt, current_screen, container_widget, entity):
        if entity['i'] < len(entity['entries']):
            entry = entity['entries'][entity['i']]
            item = None

            match current_screen:
                case 'collection_scr':
                    name = entry[1]
                    stamp = entry[2].strftime("%Y-%m-%d %I:%M %p")
                    item = EditableItemList(
                        id=f'e_{entry[0]}',
                        text=name,
                        secondary_text=stamp,
                        on_release=lambda x: self.get_list_content(x)
                    )
                    item.add_widget(IconRightWidget(
                        icon='dots-vertical',
                        on_release=lambda x: print('no idea here')
                    ))

                case 'list_content_scr':
                    item = OneLineAvatarListItem(
                        ImageLeftWidget(
                            source=entry[4]
                        ),
                        text=entry[1],
                        _no_ripple_effect=True
                    )

                case 'products_list_scr':
                    name = entry[1]
                    category = entry[2]
                    item = EditableItemList(
                        id=f'e_{entry[0]}',
                        text=name,
                        secondary_text=category,
                        _no_ripple_effect=True
                    )
                    item.add_widget(IconRightWidget(
                        icon='dots-vertical',
                        on_release=lambda x: print('no idea here')
                    ))

            container_widget.add_widget(item)
            entity['i'] += 1
        else:
            entity['i'] = 0
            return False


if __name__ == '__main__':
    MyKivyApp().run()
