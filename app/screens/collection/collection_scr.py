from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db


class CollectionScreen(MDScreen):
    test = StringProperty('test')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all = 'all_collection_scr'
        self.mine = 'usr_collection_scr'

    def switch_scr(self, *args):
        sm = self.ids.collections_manager

        if args[0].text == 'My Lists':
            sm.transition.direction = 'right'
            sm.current = self.mine
            self.ids.collections_manager.get_screen(self.mine).display_user_collections()
        else:
            sm.transition.direction = 'left'
            sm.current = self.all
            self.ids.collections_manager.get_screen(self.all).display_all_collections()




class AllCollectionScr(MDScreen):
    func = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_all_collections(self):
        rv_data = []
        for entry in db.get_all_shop_lists():
            name = entry[2]
            if isinstance(entry[3], str):
                # sqlite3
                stamp = entry[3]
            else:
                # mysql
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

        self.ids.rv_collection.data = rv_data


class UserCollectionScr(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_user_collections(self):
        rv_data = []
        curr_user = db.get_active_user()[0]

        for entry in db.get_shop_lists_for_active_user(curr_user):
            name = entry[2]
            if isinstance(entry[3], str):
                # sqlite3
                stamp = entry[3]
            else:
                # mysql
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

        self.ids.rv_usr_collection.data = rv_data
