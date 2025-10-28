from elem import Text 
from elem import Elem
import elem

class Page: 
    def __init__ (self, element):
        if not isinstance(element, Elem) or isinstance(element, Text):
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
            "img": {},
            "hr": {},
            "hr": {},
            "meta": {},
            "td": {"allowed": ["text"], "unique":["text"]},
            "p": {"allowed": ["text"]},
            "span": {"allowed": ["text", "p"]},
            "ul": {"allowed": ["li"], "min":[{"li":1}]},
            "ol": {"allowed": ["li"], "min":[{"li":1}]},
            "tr": {"allowed": ["th","td"], "at_least":["th", "td"], "exclusive":["th", "td"]},
            "table": {"allowed": ["tr"], "at_least":["tr"]}}


    def _check_one_element(self, elements):
        if isinstance(elements, Text):
            return True
        current_tag = elements.tag
        rules = self._rules[current_tag]
        if isinstance(elements.content, list):
            for el in elements.content:
                self._check_one_element(el)
        elif isinstance(elements.content, Elem):
                self._check_one_element(elements.content)
        else: 
            return False
        childs = elements.content if isinstance(elements.content, list) else [elements.content]

        allowed = rules.get("allowed")
        if allowed: 
            for child in childs: 
                if isinstance(child, Elem) and child.tag not in allowed:
                    raise ValueError(f"<{child.tag}> non allowed in <{current_tag}>")
                
        order = rules.get("order")
        if order: 
            pos = 0;
            for child in childs: 
                if isinstance(child, Elem) and child.tag in order:
                    if order.index(child.tag) != pos: 
                        raise ValueError(f"<{tag}> wrong order in <{current_tag} need this order <{[tag for tag in order]}>")
                    else:
                        pos += 1

        unique = rules.get("unique")
        if unique : 
            for tag in unique: 
                q = sum(1 for c in childs if isinstance(c, Elem) and c.tag == tag)
                if q > 1:
                    raise ValueError(f"<{tag}> non unique in <{current_tag}>")

        min = rules.get("min")
        if min : 
            for tag, nb in min.items(): 
                q = sum(1 for c in childs if isinstance(c, Elem) and c.tag == tag)
                if q < nb:
                    raise ValueError(f"<{tag}> non unique in <{current_tag}>")


        at_least = rules.get("at_least")
        if at_least :
            q = 0
            for tag in at_least: 
                q =+ sum(1 for c in childs if isinstance(c, Elem) and c.tag == tag)
                if q == 0:
                    raise ValueError(f"<{tag}> need at least <{[tag for tag in at_least]}>")

        exclusive = rules.get("exclusive")
        if exclusive :
            nbn_found = 0
            q = 0
            for tag in exclusive: 
                for c in childs:
                    if isinstance(c, Elem) and c.tag == tag:
                        q += 1
                        if q > 1:
                            raise ValueError(f"<{tag}> need exclusivly as a child one of: <{[tag for tag in at_least]}>")
    def is_valid(self):
        try:
            self._check_one_element(self.element)
        except Exception as e:
            print (e)
            return (False)
        return (True)
    
    def display_html(self):
        result = ""
        if isinstance(self.element, elem.Html):
            result += "<!DOCTYPE html>\n"
            result += str(self.element)
            print(result)
        else: 
            print(self.element)
    
    def write_to_file(self, file_name):
        try:
            with open(file_name, 'w') as file:
                if isinstance(self.element, elem.Html):
                    result = "<!DOCTYPE html>\n"
                    result += str(self.element)
                    file.write(result)
                else: 
                    file.write(self.element)
        except Exception as e: 
            print (e)

def verif_page(page, page_title):
    print(f"\n\n ----- Testing page name: {page_title} ----- \n")
    print(f"\n --- page html : ----- \n\n {page.display_html()}\n")
    print(f"\n --- result of validity test: {page.is_valid()}")
    

    
if __name__ == "__main__":
    page = Page(elem.Html([
            elem.Head(
                elem.Title(
                    Text('"Hello ground!"'))),
                elem.Body([
                    elem.H1(
                        Text('"Oh no, not again!"')),
                    ])]))
    print("\n\nTEST ---- page.is_valid() ---- \n")
    print(page.is_valid())
    print("\n\nTEST ---- page.display_html() ---- \n")
    page.display_html()
    print("\n\nTEST ---- page.write_to_file() ---- \n")
    page.write_to_file("page.html")

    body_in_body = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([elem.Body(), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))
        
    verif_page(body_in_body, "body in body")

    head_after_body = Page(elem.Html([
        elem.Body([ 
            elem.H1(
                Text('"Oh no, not again!"')),
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            ])]))

    verif_page(head_after_body, "head after body")

    page_with_wrong_element = Page(elem.Html([
        elem.Body([ 
            elem.H1(
                Text('"Oh no, not again!"')),
        elem.Head(
            elem.Title(
                elem.Elem('bad tag'))),
            ])]))

    verif_page(head_after_body, "element with bad tag")


