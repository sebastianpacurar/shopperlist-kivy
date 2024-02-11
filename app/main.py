import os
from decimal import Decimal

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar.toolbar import ActionTopAppBarButton

from app.Database import Database
from app.components import on_dropdown_item_select, AddShoppingListContent, show_snackbar

placeholder_img = os.path.join(os.getcwd(), '..', 'images', 'placeholder_image.png')


class MyKivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.prev_screen = None

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.theme_style = 'Light'

    def on_start(self):
        self.prev_screen = self.root.ids.scr_manager.current_screen.name
        self.update_top_bar()
        self.display_products()

    def toggle_dropdown(self, widget):
        data = None
        menu_items = []
        menu = MDDropdownMenu(
            caller=widget,
            width_mult=4,
            radius=[12, 12, 12, 12],
            position='center',
            elevation=4,
        )

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
                        'on_release': lambda item=entry: on_dropdown_item_select(widget, item, menu)
                    }
                )
        elif isinstance(widget, ActionTopAppBarButton):
            menu_items = [
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'Add Product',
                    'on_release': lambda target='add_product_scr': (self.change_screen(target), menu.dismiss())
                },
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'Add Category',
                    'on_release': lambda target='add_category_scr': (self.change_screen(target), menu.dismiss())
                },
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'Add Unit',
                    'on_release': lambda target='add_unit_scr': (self.change_screen(target), menu.dismiss())
                }
            ]

        menu.items = menu_items
        menu.open()

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
        price = Decimal(self.root.ids.product_price_text.text)
        category = self.root.ids.product_category_text.text
        unit = self.root.ids.product_unit_text.text
        db_result = db.add_product(name, price, category, unit)
        show_snackbar(db_result)

    def perform_shop_list_add(self):
        shop_list_name = self.dialog.content_cls.ids.shop_list_name_text.text
        db_result = db.add_shopping_list(shop_list_name)
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
                top_bar.right_action_items = [
                    ['dots-horizontal-circle-outline', lambda item: self.toggle_dropdown(item)]]
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
            case 'add_category_scr':
                top_bar.title = 'Add Category'
                top_bar.left_action_items = [['arrow-left', lambda _: self.navigate_back()]]
                top_bar.right_action_items = []
            case 'add_unit_scr':
                top_bar.title = 'Add Category'
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

    def display_products(self):
        rv_data = []
        for entry in db.get_all_products():
            item_data = {
                'text': entry[1],
                'secondary_text': entry[2],
                'itm_icon': 'dots-vertical',
            }
            rv_data.append(item_data)

        self.root.ids.rv_prod_list.data = rv_data

    def display_collections(self):
        rv_data = []
        for entry in db.get_shop_lists():
            name = entry[1]
            stamp = entry[2].strftime("%Y-%m-%d %I:%M %p")
            id_val = str(entry[0])
            item_data = {
                'id': id_val,
                'text': name,
                'secondary_text': stamp,
                'itm_icon': 'dots-vertical',
                'on_release': lambda x=id_val: self.display_list_products(x),
            }
            rv_data.append(item_data)

        self.root.ids.rv_collection.data = rv_data

    def display_list_products(self, *args):
        self.change_screen('list_content_scr')
        rv_data = []
        for entry in db.get_shop_list(args[0]):
            item_data = {
                'text': entry[1],
                'img_path': entry[4],
                '_no_ripple_effect': True,
            }
            rv_data.append(item_data)

        self.root.ids.rv_list_content.data = rv_data

    def display_bottom_sheet(self, *args):
        print(args[0].id)


if __name__ == '__main__':
    db = Database()
    MyKivyApp().run()
