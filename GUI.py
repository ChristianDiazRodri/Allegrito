from kivy.app import App
from selenium import webdriver
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.config import Config
from plyer import filechooser
import time
import QuestionsModule


LabelBase.register(name='Tuffy', fn_regular='fonts/tuffy_bold.ttf')
Window.minimum_height = 400
Config.set('graphics', 'resizable', False)


class Allegrito(Widget):
    kiosk = ObjectProperty(None)
    link = ObjectProperty(None)
    questionnaire = ObjectProperty(None)
    driver_path = ObjectProperty(None)

    def browse_kiosk(self):
        try:
            self.kiosk.text = filechooser.open_file(title="Pick an Excel file file..",
                                 filters=[("Excel file", "*.xlsx")])[0]
        except:
            pass

    def browse_questionnaire(self):
        try:
            self.questionnaire.text = filechooser.open_file(title="Pick an Excel file file..",
                                 filters=[("Excel file", "*.xlsx")])[0]
        except:
            pass

    def browse_driver(self):
        try:
            self.driver_path.text = filechooser.open_file(title="Pick an Excel file file..",
                                 filters=[("Excel file", "*.xlsx")])[0]
        except:
            pass

    def run(self):
        try:
            driver = webdriver.Chrome(self.driver_path.text)
            driver.get(self.link.text)
            time.sleep(2)
            QuestionsModule.Select_language(driver,self.link)
        except Exception as e:
            print(e)



class AllegritoApp(App):

    def build(self):
        return Allegrito()


AllegritoApp().run()
