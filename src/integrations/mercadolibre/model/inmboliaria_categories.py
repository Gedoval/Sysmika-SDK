import json
import os


class InmobiliariaCategories:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.__load_categories_from_file()

    def __load_categories_from_file(self):
        self.categories = json.load(open(self.current_dir + "/resources/categories.json"))
