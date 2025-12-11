#!/usr/bin/python3


class Text(str):
    """
    A Text class to represent a text you could use with your HTML elements.

    Because directly using str class was too mainstream.
    """

    def __str__(self):
        """
        Do you really need a comment to understand this method?..
        """
        return (super().__str__().replace('&', '&amp;')
                                .replace('<', '&lt;')
                                .replace('>', '&gt;')
                                .replace('"', '&quot;')
                                .replace('\n', '\n<br />\n'))


class Elem:
    """
    Elem will permit us to represent our HTML elements.
    """
    class ValidationError(Exception):
        def __init__(self):
            super().__init__("Error: wrong element type in content")

    def __init__(self, tag='div', attr={}, content=None, tag_type='double'):
        """
        __init__() method.

        Obviously.
        """
        self.tag = tag 
        self.attr = attr
        self.content = [] 
        self.tag_type = tag_type

        if content is not None:
            self.add_content(content)


    def __str__(self):
        """
        The __str__() method will permit us to make a plain HTML representation
        of our elements.
        Make sure it renders everything (tag, attributes, embedded
        elements...).
        """
        result = ""
        if self.tag_type == 'double':
            result += f"<{self.tag}{self.__make_attr()}>"
            content = ""
            content = '\n  '.join(self.__make_content().rstrip('\n').split('\n'))
            result += content
            if content == '':
                result += f"</{self.tag}>"
            else: 
                result += f"\n</{self.tag}>"
        elif self.tag_type == 'simple':
            result += f"<{self.tag}{self.__make_attr()} />"
        return result 

    def __make_attr(self):
        """
        Here is a function to render our elements attributes.
        """
        result = ''
        for pair in sorted(self.attr.items()):
            result += ' ' + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result
    
    def __make_content(self):
        """
        Here is a method to render the content, including embedded elements.
        """

        if len(self.content) == 0:
            return ''
        result = '\n'
        for elem in self.content:
            result += str(elem) 
            result += '\n'
        return result

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        """
        Is this object a HTML-compatible Text instance or a Elem, or even a
        list of both?
        """
        return (isinstance(content, Elem) or type(content) == Text or
                (type(content) == list and all([type(elem) == Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))

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

if __name__ == '__main__':
    print(
        Html([
            Head(
                Title(
                    Text('"Hello ground!"'))),
                Body([
                    H1(
                        Text('"Oh no, not again!"')),
                    Img(attr={"src":"http://i.imgur.com/pfp3T.jpg"})])]))
    print(Text(">"))
    print(Div())
    try:
        Html(1)
    except Exception as e: 
        print(type(e) == Elem.ValidationError)
    print("hello")
