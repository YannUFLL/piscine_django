from elem import Text 
from elem import Elem

class Page: 
    def __init__ (self, element):
        if not isinstance(element, Elem):
            raise Exception("Error: arg is not an instance of Elem")
        self.element = element
        self._authorise_type = ["html", "head", "body",
"title", "meta", "img", "table", "th", "tr", "td", "ul", "ol", "li", "h1", "h2", "p", "div", "span", "hr", "br"]
        self._has_header = False
        self._has_body = False
        self._rules = {
            "html": {"allowed": ["head", "body"], "order": ["head","body"]},
            "head": {"allowed": ["title", "meta"], "unique": ["title"]},
            "body": {"allowed": ["h1", "h2", "div", "table", "ul", "ol", "span", "text"]},
            "div": {"allowed": ["h1", "h2", "div", "table", "ul", "ol", "span", "text"]},
            "title": {"allowed": ["text"], "unique":["text"]},
            "h1": {"allowed": ["text"], "unique":["text"]},
            "h2": {"allowed": ["text"], "unique":["text"]},
            "li": {"allowed": ["text"], "unique":["text"]},
            "th": {"allowed": ["text"], "unique":["text"]},
            "td": {"allowed": ["text"], "unique":["text"]},
            "p": {"allowed": ["text"]},
            "span": {"allowed": ["text", "p"]},
            "ul": {"allowed": ["li"], "min":{"li":1}},
            "ol": {"allowed": ["li"], "min":{"li":1}},
            "tr": {"allowed": ["th","td"], "at_least":["th", "td"], "exclusive":["th", "td"]},
            "table": {"allowed": ["tr"], "at_least":["tr"]}}
        
        self._local_state = { "html" : {"in_tag": False, "order": [False, False]},
                             "head": {"in_tag": False, "unique": False},
                             "body": {"in_tag": False},
                             "div": {"in_tag": False},
                             "title": {"in_tag": False, "unique":False},
                             "h1": {"in_tag": False, "unique":False},
                             "h2": {"in_tag": False, "unique":False},
                             "li": {"in_tag": False, "unique":False},
                             "th": {"in_tag": False, "unique":False},
                             "td": {"in_tag": False, "unique":False},
                             "p": {"in_tag": False},
                             "span": {"in_tag": False},
                             "ul": {"in_tag": False, "min": 0},
                             "ul": {"in_tag": False, "min": 0},
                             "tr": {"in_tag": False, "at_least": False, "exclusive": [False,False]},
                             "table": {"in_tag": False, "at_least": False},

        }

    def _verify_rules(self, tag):
        rules = self._rules
        for bal, data in self._local_state.items():
            if data.get("in_tag"):
                rules.get("order").count(tag) != 0


    def _check_elements(self, elements):
        if elements.content == Text:
            return True
        elif elements.content == list:
            for el in elements:
                self._check_elements(el.contents)
        elif elements.content == Elem:

            tag = elements.tag
            rule = self._local_state[tag]

            if elements.content != None:
                self._local_state[tag]["in_tag"] = True
                self._verify_rules(tag)


        elif elements.content != Elem:
            return False
           


    def is_valid(self):

