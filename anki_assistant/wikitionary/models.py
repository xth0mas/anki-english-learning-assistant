import copy
import json
import random
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
        self._fix_ipa(json)
        return Word(json)

    """
    Fix bugs in the Python program having generated the dictionary file.

    :return: The updated JSON document
    """
    def _fix_ipa(self, json):
        # IPA could contains multiple IPA text (Ex: /car/ in US, /cAr/). We keep only the first one
        if "ipa" in json:
            ipa = json.get("ipa")
            index_second_slash = ipa.index('/', 1)
            if index_second_slash < len(ipa) - 1:
                ipa = ipa[:index_second_slash + 1]
                # json.set("ipa", TextNode.valueOf(ipa))
                json["ipa"] = ipa


class Word:
    def __init__(self, word):
        self.word = word
        self.annotated_word = self._add_annotations(word)

    def _add_annotations(self, word, num_of_def=1, num_of_quot=1, num_of_transl=3):
        word = copy.deepcopy(word)
        if "audio" in word:
            word["audio"] = {
                "name": word["audio"],
                "url": word["audio_url"],
                "include": True
            }
            del word["audio_url"]

        if "images" in word:
            for i, image in enumerate(word["images"]):
                value = True if i < 1 else False
                word["images"][i].update({
                    "include": value,
                    "card": value
                })

        if "synonyms" in word:
            for i, synonym in enumerate(word["synonyms"]):
                word["synonyms"][i] = {
                    "text": synonym,
                    "include": True
                }

        if "translations" in word:
            for i, translation in enumerate(word["translations"]):
                value = True if i < num_of_transl else False
                word["translations"][i] = {
                    "text": translation,
                    "include": value
                }

        if "types" in word:
            for i, type in enumerate(word["types"]):
                word["types"][i].update({
                    "include": True
                })
                if "definitions" in type:
                    for j, definition in enumerate(type["definitions"]):
                        value = True if j < num_of_def else False
                        word["types"][i]["definitions"][j].update({
                            "include": value,
                            "card": value
                        })
                        if "quotations" in definition:
                            for k, quotation in enumerate(definition["quotations"]):
                                value = True if k < num_of_quot else False
                                word["types"][i]["definitions"][j]["quotations"][k] = {
                                    "text": quotation,
                                    "include": value,
                                    "card_sample": bool(random.getrandbits(1))
                                }
        return word

    def as_json(self):
        return self.word

    def as_annotated_json(self):
        return self.annotated_word
