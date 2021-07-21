import json
import traceback


class Dictionary:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dictionary = self._load_dictionary()

    def _load_dictionary(self):
        try:
            with open(self.filepath, 'r') as json_file:
                data = json.load(json_file)
            return data
        except Exception:
            print(traceback.format_exc())
            return None

    """
    Search inside the full JSON dictionary after the given identifier.
    Only the rank could be used as identifier for now.
    """
    def search_word(self, identifier):
        json = None
        for i, value in enumerate(self.dictionary):
            print(i, ": ", value['title'])
            if value['rank'] == identifier:
                json = value
                break
        return Word(json)


class Word:
    def __init__(self, word):
        self.word = word

    def as_json(self):
        return self.word
