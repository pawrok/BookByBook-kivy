from sqliteDB import SqliteDB

from kivy.uix.label import Label
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView 
from kivy.properties import ListProperty, StringProperty, ObjectProperty, \
        NumericProperty, BooleanProperty, AliasProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config

import kivy

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '650')

kivy.require('1.9.0')

class RootRoot(BoxLayout):
    pass

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

class GridLayoutTest(GridLayout):
    pass

class BookItem(BoxLayout):
    title = StringProperty()

class ShelfItem(BoxLayout):
    shelf_title = StringProperty()

class BookScrollView(ScrollView):
    def __init__(self, **kwargs): 
        super(BookScrollView, self).__init__(**kwargs) 
        self.data = SqliteDB.get_books_fromDB()
        #[{'ID': 2, 'title': 'title1'}, {'ID': 1, 'title': 'title2'}, {'ID': 1, 'title': 'title2'}, {'ID': 1, 'title': 'title2'}, {'ID': 1, 'title': 'title2'}]

        layout = GridLayout(cols=3, spacing=15, size_hint_y=None, col_default_width = self.width / 3)
        for item in self.data:
            book = BookItem(title=item['title'])
            layout.add_widget(book)
        self.add_widget(layout)


class BookcaseApp(App):
    def build(self):
        SqliteDB()
        Builder.load_file('kv/root.kv')
        return RootRoot()

    def add_book_to_db(self, input_title, input_author):
        SqliteDB.add_book_toDB(5, input_title, input_author)


if __name__ == '__main__':
    BookcaseApp().run()
