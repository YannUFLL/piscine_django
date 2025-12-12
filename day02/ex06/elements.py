from elem import Elem, Text

class Html(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("html", tag_type="double", content=content, **kwargs)

class Head(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("head", tag_type="double", content=content, **kwargs)

class Body(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("body", tag_type="double", content=content, **kwargs)

class Title(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("title", tag_type="double", content=content, **kwargs)

class Meta(Elem):
    def __init__(self, **kwargs):
        super().__init__("meta", tag_type="simple", **kwargs)

class Img(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("img", tag_type="simple", content=content, **kwargs)

class Table(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("table", tag_type="double", content=content, **kwargs)

class Th(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("th", tag_type="double", content=content, **kwargs)

class Tr(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("tr", tag_type="double", content=content, **kwargs)

class Td(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("td", tag_type="double", content=content, **kwargs)

class Ul(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("ul", tag_type="double", content=content, **kwargs)

class Ol(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("ol", tag_type="double", content=content, **kwargs)

class Li(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("li", tag_type="double", content=content, **kwargs)

class H1(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("h1", tag_type="double", content=content, **kwargs)

class H2(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("h2", tag_type="double", content=content, **kwargs)

class P(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("p", tag_type="double", content=content, **kwargs)

class Div(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("div", tag_type="double", content=content, **kwargs)

class Span(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("span", tag_type="double", content=content, **kwargs)

class Hr(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("hr", tag_type="simple", content=content, **kwargs)

class Br(Elem):
    def __init__(self, content=None, **kwargs):
        super().__init__("br", tag_type="simple", content=content, **kwargs)

def test_comparison():
    print("=== COMPARISON TESTS ===")
    print(
        Html([
            Head(
                Title(
                    Text('"Hello ground!"'))),
                Body([
                    H1(
                        Text('"Oh no, not again!"')),
                    Img(attr={"src":"http://i.imgur.com/pfp3T.jpg"})])]))
    print()
    
def test_html_elements():
    print("=== HTML ELEMENT TESTS ===")

    # 1. Basic structure test
    doc = Html([
        Head([
            Title(Text("Test page")),
            Meta(attr={"charset": "utf-8"})
        ]),
        Body([
            H1(Text("Main title")),
            H2(Text("Subtitle")),
            P(Text("Paragraph")),
            Br(),
            Hr(),
            Img(attr={"src": "image.png"}),
            Div([
                Span(Text("Inline text")),
                Ul([
                    Li(Text("Item 1")),
                    Li(Text("Item 2")),
                ])
            ]),
            Table([
                Tr([
                    Th(Text("Header")),
                    Th(Text("Header 2"))
                ]),
                Tr([
                    Td(Text("Cell 1")),
                    Td(Text("Cell 2"))
                ])
            ])
        ])
    ])

    print(doc)

    # 2. Empty tag test
    print(Div())
    print(Br())
    print(Hr())

    # 3. Text escaping / raw text
    print(Text("<hello> & \"world\""))

    # 4. Invalid content type (must raise ValidationError)
    try:
        Html(42)
    except Exception as e:
        print(type(e) is Elem.ValidationError)

    # 5. Invalid nesting
    try:
        Ul(P(Text("invalid")))
    except Exception as e:
        print(type(e) is Elem.ValidationError)

    # 6. Ensure Elem cannot be instantiated directly
    try:
        Elem("div")
    except Exception as e:
        print(type(e) is Elem.ValidationError)

    print("=== TESTS DONE ===")

if __name__ == '__main__':
    test_comparison()
    test_html_elements()