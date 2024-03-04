from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from app.components.components import db, BottomSheetSelectionLineItem, RenameShoppingListContent, DeleteShoppingListContent
from app.utils import constants as const


class CollectionScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.bind(on_pre_enter=self.set_definitions)

    def set_definitions(self, *args):
        self.sm = self.ids.collections_manager
        self.sm.get_screen(const.USER_COLLECTION_SCR).display_user_collections()

    def switch_scr(self, *args):
        if self.sm.current != args[0]:
            match args[0]:
                case const.USER_COLLECTION_SCR:
                    self.sm.transition.direction = 'right'
                    self.sm.current = const.USER_COLLECTION_SCR
                    self.sm.get_screen(const.USER_COLLECTION_SCR).display_user_collections()
                case const.ALL_COLLECTION_SCR:
                    self.sm.transition.direction = 'left'
                    self.sm.current = const.ALL_COLLECTION_SCR
                    self.sm.get_screen(const.ALL_COLLECTION_SCR).display_all_collections()

    def refresh_data(self, *args):
        self.sm.get_screen(const.USER_COLLECTION_SCR).display_user_collections()
        self.sm.get_screen(const.ALL_COLLECTION_SCR).display_all_collections()


# TODO: continue here
class BaseCollectionScr(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_app = MDApp.get_running_app()

    def create_item_data(self, entry):
        entry = [str(x) for x in entry]
        stamp = entry[3]
        sheet_content = set_bottom_sheet_content(entry[0], entry[2])
        if not isinstance(stamp, str):
            stamp = entry[2].strftime("%Y-%m-%d %I:%M %p")
        if len(entry) == 5:
            item_data = {
                'itm_id': entry[0],
                'headline': entry[2],
                'supporting': f'created by {entry[4]}',
                'tertiary': stamp,
                'itm_icon': 'dots-vertical',
                'sheet_func': lambda name=entry[2], list_id=entry[0]: self.main_app.toggle_bottom(name, list_id, sheet_content),
                'on_release': lambda list_id=entry[0]: self.main_app.change_screen_to_list_scr(list_id),
            }
        else:
            item_data = {
                'itm_id': entry[0],
                'headline': entry[2],
                'supporting': stamp,
                'itm_icon': 'dots-vertical',
                'sheet_func': lambda name=entry[2], list_id=entry[0]: self.main_app.toggle_bottom(name, list_id, sheet_content),
                'on_release': lambda list_id=entry[0]: self.main_app.change_screen_to_list_scr(list_id),
            }
        return item_data


class UserCollectionScr(BaseCollectionScr):
    def __init(self, **kwargs):
        super().__init__(**kwargs)

    def display_user_collections(self, *args):
        rv_data = []
        curr_user = db.get_active_user()[0]

        for entry in db.get_shop_lists_for_active_user(curr_user):
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)

        self.ids.rv_usr_collection.data = rv_data


class AllCollectionScr(BaseCollectionScr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_all_collections(self, *args):
        rv_data = []
        for entry in db.get_all_shop_lists():
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)

        self.ids.rv_collection.data = rv_data


def set_bottom_sheet_content(list_id, list_name):
    return [
        BottomSheetSelectionLineItem(
            text='Rename',
            on_release=lambda _: (
                MDApp.get_running_app().show_dialog(RenameShoppingListContent(), list_id),
                MDApp.get_running_app().bottom.set_state('toggle')),
        ),
        BottomSheetSelectionLineItem(
            text='Delete',
            on_release=lambda _: (
                MDApp.get_running_app().show_dialog(DeleteShoppingListContent(), list_name, list_id),
                MDApp.get_running_app().bottom.set_state('toggle')),
        )
    ]
