from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView 
from kivy.properties import ListProperty, StringProperty, ObjectProperty, \
        NumericProperty, BooleanProperty, AliasProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

import kivy

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '650')

kivy.require('1.9.0')

class RootRoot(BoxLayout):
    pass

class RootScreenManager(ScreenManager):
    pass

class MiddleScreenManager(ScreenManager):
    pass

class HomeScreen(Screen):
    pass

class StatsScreen(Screen):
    pass

class AddScreen(Screen):
    pass

class WishScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class Books(Screen):
    pass

class Shelves(Screen):
    pass

class Tags(Screen):
    pass

class BookItem(BoxLayout):
    book_title = StringProperty()

class ShelfItem(BoxLayout):
    shelf_title = StringProperty()

class BookWidget(BoxLayout):
    data = ListProperty()
    def _get_data_for_widgets(self):
        return self.data
    data_for_widgets = AliasProperty(_get_data_for_widgets, bind=['data'])

class BookViewer(RecycleView): 
    def __init__(self, **kwargs): 
        super(BookViewer, self).__init__(**kwargs) 
        self.data = [{
            'book_index': 1,
            'book_content': 'contentxxx',
            'book_title': 'title1'},
            {'book_index': 2,
            'book_content': 'contentxxx',
            'book_title': 'title2'},
            {'book_index': 3,
            'book_content': 'contentxxx',
            'book_title': 'title3'},
            {'book_index': 4,
            'book_content': 'contentxxx',
            'book_title': 'title4'
            }]

class ShelfViewer(RecycleView): 
    def __init__(self, **kwargs): 
        super(ShelfViewer, self).__init__(**kwargs) 
        self.data = [{
            'shelf_title': 'title1'},
            {
            'shelf_title': 'title2'},
            {
            'shelf_title': 'title3'},
            {
            'shelf_title': 'title4'
            }]


class BookcaseApp(App):
    def build(self):
        # self.book_store = BookWidget()
        # self.book_store2 = BookWidget()
        self.data = self.load_books()
        # self.shelf_store = ShelfWidget()
        # self.load_shelves()
        Builder.load_file('kv/root.kv')
        return RootRoot()



    def load_books(self):
        return  [{
            'book_index': 1,
            'book_content': 'contentxxx',
            'book_title': 'title1'},
            {'book_index': 2,
            'book_content': 'contentxxx',
            'book_title': 'title2'},
            {'book_index': 3,
            'book_content': 'contentxxx',
            'book_title': 'title3'},
            {'book_index': 4,
            'book_content': 'contentxxx',
            'book_title': 'title4'
            }]
        # self.book_store.data = data
        # self.book_store2.data = data

    def load_shelves(self):
        data = [{
            'shelf_title': 'random shelf'}]
        self.shelf_store.data = data


if __name__ == '__main__':
    BookcaseApp().run()
