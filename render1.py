
import abc
import collections
from html import escape
import textwrap
import sys
#what mean html.escape textwrap collections.ChainMap

class Render(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(Class, Subclass):
        if Class is Subclass:
            attributes = collections.ChainMap(*(Superclass.__dict__
                        for Superclass in Subclass.__mro__))
            methods = ("header", "paragraph", "footer")
            if all(method in attributes for method in methods):
                return True
        return NotImplemented


MESSAGE = """This is a very short {} paragraph that demonstrates
the simple {} class."""

def main():
    paragraph1 = MESSAGE.format("plain-text","TextRender")
    paragraph2 = "This is an anthor paragraph just so that we can see \
two paragraph in action."    
    title = "Plain Text"
    textPage = Page(title,TextRender(22))
    textPage.add_paragraph(paragraph1)
    textPage.add_paragraph(paragraph2)
    textPage.render()

    print()

    title = "Html"
    htmlPage = Page(title,HtmlRender(HtmlWriter()))
    htmlPage.add_paragraph(paragraph1)
    htmlPage.add_paragraph(paragraph2)
    htmlPage.render()


class Page:

    def __init__(self,title,renderer):
        self.title = title
        self.renderer = renderer
        self.paragraph = []

    def add_paragraph(self,paragraph):
        self.paragraph.append(paragraph)

    def render(self):
        self.renderer.header(self.title)
        for paragraph in self.paragraph:
            self.renderer.paragraph(paragraph)
        self.renderer.footer()

class TextRender:

    def __init__(self,width = 80,file = sys.stdout):
        self.width = width
        self.file = file
        self.previous = False

    def header(self,title):
        self.file.write('{0:^{2}}\n{1:^{2}}\n'.format(
            title,'='*len(title),self.width))

    def paragraph(self,paragraph):
        if self.previous:
            self.file.write('\n')
        self.file.write(textwrap.fill(paragraph,self.width))
        self.file.write('\n')
        self.previous = True

    def footer(self):
        pass

class HtmlWriter:

    def __init__(self,file=sys.stdout):
        self.file = file

    def header(self):
        self.file.write('<!DOCTYPE html>\n<html lang="en">\n')

    def title(self,title):
        self.file.write('<head>\n<meta charset="UTF-8">\n\
<title>{}</title>\n</head>\n'.format(escape(title)))
    def start_body(self):
        self.file.write('<body>\n')
    def body(self,text):
        self.file.write('<p>{}</p>\n'.format(escape(text)))
    def end_body(self):
        self.file.write('</body>\n')
    def footer(self):
        self.file.write('</html>\n')

class HtmlRender:

    def __init__(self,htmlwriter):
        self.htmlwriter = htmlwriter

    def header(self,title):
        self.htmlwriter.header()
        self.htmlwriter.title(title)

    def paragraph(self,text):
        self.htmlwriter.start_body()
        self.htmlwriter.body(escape(text))
        

    def footer(self):
        self.htmlwriter.end_body()
        self.htmlwriter.footer()


if __name__ == '__main__':
    main()