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
        rules = self._rules.get(current_tag)
        if rules == None:
            raise (ValueError("Error: tag doesn't exist"))
        if isinstance(elements.content, list):
            for el in elements.content:
                if isinstance(el, Elem):
                    self._check_one_element(el)

            
        elif isinstance(elements.content, Elem):
                self._check_one_element(elements.content)
        else: 
            return False
        childs = elements.content if isinstance(elements.content, list) else [elements.content]

        allowed = rules.get("allowed")
        if allowed: 
            for child in childs: 
                tag = child.tag if isinstance(child, Elem) else "text" if isinstance(child, Text) else None
                if tag not in allowed:
                    raise ValueError(f"<{child.tag}> non allowed in <{current_tag}>")

                
        order = rules.get("order")
        if order: 
            pos = 0;
            for child in childs: 
                child_tag = child.tag if isinstance(child, Elem) else "text" if isinstance(child, Text) else None
                if tag in order:
                    if order.index(child_tag) != pos: 
                        raise ValueError(f"<{tag}> wrong order in <{current_tag} need this order <{[tag for tag in order]}>")
                    else:
                        pos += 1

        unique = rules.get("unique")
        if unique : 
            for tag in unique: 
                q = sum(1 for c in childs if (isinstance(c, Elem) and c.tag == tag) or (isinstance(c, Text) and "text" == tag))
                if q > 1:
                    raise ValueError(f"<{tag}> non unique in <{current_tag}>")

        min = rules.get("min")
        if min :
            for rule in min:
                tag, nb = next(iter(rule.items()))
                q = sum(1 for c in childs if (isinstance(c, Elem) and c.tag == tag) or (isinstance(c, Text) and "text" == tag))
                if q < nb:
                    raise ValueError(f"<{tag}> non unique in <{current_tag}>")


        at_least = rules.get("at_least")
        if at_least :
            q = 0
            for tag in at_least: 
                q =+ sum(1 for c in childs if (isinstance(c, Elem) and c.tag == tag) or (isinstance(c, Text) and "text" == tag))
                if q == 0:
                    raise ValueError(f"<{tag}> need at least <{[tag for tag in at_least]}>")

        exclusive = rules.get("exclusive")
        if exclusive :
            nbn_found = 0
            q = 0
            for tag in exclusive: 
                for c in childs:
                    if isinstance(c, Elem) and c.tag == tag or isinstance(c, Text) and "text" == tag:
                        q += 1
                        if q > 1:
                            raise ValueError(f"<{tag}> need exclusivly as a child one of: <{[tag for tag in at_least]}>")
    def is_valid(self):
        try:
            self._check_one_element(self.element)
        except ValueError as e:
            #print (e)
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
            return (False)
        return (True)

def verif_page(page, page_title, result):
    v = "\033[32mVALIDATE \u2714\033[0m"
    x = "\033[31mERROR \u2718\033[0m"
    print(f"\n\n\033[01m ----- Test: {page_title} ----- {v if result == page.is_valid() else x} \n\033[0m")
    print(f"\n\033[01mpage html:\n\033[0m")
    page.display_html()
    print(f"\n\033[01mis_valid() return value: \033[0m{page.is_valid()}")

    
if __name__ == "__main__":
    page = Page(elem.Html([
            elem.Head(
                elem.Title(
                    Text('"Hello ground!"'))),
                elem.Body([
                    elem.H1(
                        Text('"Oh no, not again!"')),
                    ])]))

    verif_page(page, "body: valid page", True)

    v = "\033[32mVALIDATE \u2714\033[0m"
    x = "\033[31mERROR \u2718\033[0m"
    print(f"\n\n\033[01m ----- Test: write to file ----- {v if page.write_to_file('page.html') else x} \n\033[0m")

    body_in_body = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([elem.Body(), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))
        
    verif_page(body_in_body, "body: another body as child", False)

    head_after_body = Page(elem.Html([
        elem.Body([ 
            elem.H1(
                Text('"Oh no, not again!"')),
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            ])]))

    verif_page(head_after_body, "head: wrong placement after body", False)

    wrong_element_tag = Page(elem.Html([
        elem.Body([ 
            elem.H1(
                Text('"Oh no, not again!"')),
        elem.Head(
            elem.Title(
                elem.Elem('bad tag'))),
            ])]))


    verif_page(wrong_element_tag, "element: new with bad tag", False)

    wrong_element_child = Page(elem.Html([
            elem.Head(
                elem.Title(
                    Text('"Hello ground!"'))),
                elem.Body([
                    elem.Div(elem.Meta()), 
                    elem.H1(
                        Text('"Oh no, not again!"')),
                    ])]))


    verif_page(wrong_element_child, "div: div wrong child", False)

    div_inside_P = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([
                elem.Div(elem.Span(elem.P(Text("Coucou")))),
                elem.Div(), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))


    verif_page(div_inside_P, "p: good child", True)

    div_inside_P = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([
                elem.Div(
                elem.P(elem.Div())),
                elem.Div(), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))


    verif_page(div_inside_P, "p: wrong child", False)

    div_inside_span = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([
                elem.Span(elem.Div()), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))


    verif_page(div_inside_span, "span: wrong child", False)

    ul_with_wrong_child = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([
                elem.Ul(elem.Div()), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))


    verif_page(ul_with_wrong_child, "ul: wrong child", False)

    ul_without_child = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([
                elem.Ul(), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))


    verif_page(ul_without_child, "ul: no child", False)

    ul_with_good_child = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([
                elem.Ul(elem.Li()), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))


    verif_page(ul_with_good_child, "good child", True)

    tr_with_wrong_child = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([
                elem.Table(elem.Tr(elem.Div())), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))


    verif_page(tr_with_wrong_child, "tr: wrong child", False)

    tr_with_exclusive_childs = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([
                elem.Table(elem.Tr([elem.Th(), elem.Td()])), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))

    verif_page(tr_with_exclusive_childs, "tr: non exclusive childs", False)

    table_with_wrong_child = Page(elem.Html([
        elem.Head(
            elem.Title(
                Text('"Hello ground!"'))),
            elem.Body([
                elem.Table(elem.Div()), 
                elem.H1(
                    Text('"Oh no, not again!"')),
                ])]))

    verif_page(tr_with_exclusive_childs, "table: wrong child", False)









    

