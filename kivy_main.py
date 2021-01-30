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

# kivy.require('1.9.0')

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
    input_title = StringProperty("Title")
    input_author = StringProperty("Author")
    input_category = StringProperty("Category")
    input_rating = NumericProperty(0)
    input_rented_person = StringProperty("Borrowed to...")
    input_date_completed = StringProperty("1.01.2021")
    input_pages = NumericProperty(0)
    book_id = NumericProperty(0)
    def reset_properties(self):
        self.input_title = "Title"
        self.input_author = "Author"
        self.input_category = "Category"
        self.input_rating = 0
        self.input_rented_person = "Borrowed to..."
        self.input_date_completed = "1.01.2021"
        self.input_pages = 0
        self.book_id = 0
     

class WishScreen(Screen):
    pass

class SettingsScreen(Screen):
    def delete_DB(self):
        SqliteDB.delete_table()

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
    book_id = NumericProperty()
    
class StarsButton(BoxLayout):
    rating = NumericProperty()
    # def __init__(self, **kwargs):
    #     super(StarsButton, self).__init__(**kwargs)
    #     self.set_rating(self.rating)
    #     print(self.rating)

    def set_rating(self, value):
        if value == 1:
            self.ids['first_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.ids['sec_s'].background_color = 1.0, 1.0, 1.0, 1.0
            self.ids['third_s'].background_color = 1.0, 1.0, 1.0, 1.0
            self.ids['fourth_s'].background_color = 1.0, 1.0, 1.0, 1.0
            self.rating = 1
        elif value == 2:
            self.ids['first_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.ids['sec_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.ids['third_s'].background_color = 1.0, 1.0, 1.0, 1.0
            self.ids['fourth_s'].background_color = 1.0, 1.0, 1.0, 1.0
            self.rating = 2
        elif value == 3:
            self.ids['first_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.ids['sec_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.ids['third_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.ids['fourth_s'].background_color = 1.0, 1.0, 1.0, 1.0
            self.rating = 3
        elif value == 4:
            self.ids['first_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.ids['sec_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.ids['third_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.ids['fourth_s'].background_color = 1.0, 0.0, 1.0, 1.0
            self.rating = 4
        else:
            pass

        

class ShelfItem(BoxLayout):
    shelf_title = StringProperty()

class BookScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(BookScrollView, self).__init__(**kwargs)
        
        self.data = SqliteDB.get_books_fromDB()

        #TODO: height below is fixed, but should be dynamic
        layout = GridLayout(cols=3, spacing=15, size_hint_y=None, height=900, col_default_width = self.width / 3)
        for item in self.data:
            book = BookItem(book_id=item['ID'],title=item['title'])
            layout.add_widget(book)
        self.add_widget(layout)


class BookcaseApp(App):
    def build(self):
        SqliteDB()
        Builder.load_file('kv/root.kv')
        self.root = RootRoot()
        return self.root

    def add_book_to_db(
            self, input_title, input_author, input_category, input_rating, input_rented_person,
            input_date_completed, input_pages):
        
        if input_rented_person:
            is_rent = True
        
        print("add")
        input_rating = int(input_rating)
        is_rent = int(is_rent)
        input_pages = int(input_pages)
        
        SqliteDB.add_book_toDB(
            input_title, input_author, input_category, input_rating,
            is_rent, input_rented_person, input_date_completed, input_pages)
    
    def update_book_in_db(
            self, id, input_title, input_author, input_category, input_rating,
            input_rented_person, input_date_completed, input_pages):
        
        if input_rented_person:
            is_rent = True

        print("update")
        
        input_rating = int(input_rating)
        is_rent = int(is_rent)
        input_pages = int(input_pages)
        
        SqliteDB.edit_book_inDB(
            id, input_title, input_author, input_category, input_rating,
            is_rent, input_rented_person, input_date_completed, input_pages)
        
    def add_home_screen(self):
        index = 0
        for i in range(len(self.root.ids.rootmanager.screen_names)):
            if self.root.ids.rootmanager.screen_names[i].find('home') != -1:
                index = i
        
        self.root.ids['rootmanager'].remove_widget(self.root.ids.rootmanager.screens[index])
        self.root.ids['rootmanager'].add_widget(HomeScreen())

    def open_edit_book(self, id):
        for i in range(len(self.root.ids.rootmanager.screen_names)):
            if self.root.ids.rootmanager.screen_names[i].find('new') != -1:
                index = i
        
        book_values = SqliteDB.get_single_book_fromDB(id)
        self.root.ids['rootmanager'].remove_widget(self.root.ids.rootmanager.screens[index])
        self.root.ids['rootmanager'].add_widget(AddScreen(
            input_title = book_values['title'],
            input_author = book_values['author'],
            input_category = book_values['category'],
            input_rating = book_values['rating'],
            input_rented_person = book_values['rentedPerson'],
            input_date_completed = book_values['dateCompleted'],
            input_pages = book_values['pageCount'],
            book_id = id
            ))
        # self.root.ids['rootmanager'].screens[4].children[0].children[0].children[1].children[1].children[1]
        self.root.ids['rootmanager'].current = 'new'
        #                          AddScreen -> BoxLayout -> BoxLayout -> BoxLayout -> BoxLayout -> StarsButton -> set_rating
        self.root.ids['rootmanager'].screens[4].children[0].children[0].children[1].children[1].children[1].set_rating(book_values['rating'])


if __name__ == '__main__':
    BookcaseApp().run()
