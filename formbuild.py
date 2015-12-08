import os
from html import escape
import abc

def main():
    basedir = os.path.abspath(os.path.dirname(__file__))
    htmlformfile = os.path.join(basedir,"form.html")

    htmlform = create_login_form(HtmlFormBuilder())
    with open(htmlformfile,"w",encoding="utf-8") as file:
        file.write(htmlform)
        print("wrote",htmlformfile)

def create_login_form(builder):
    builder.add_title("Login")
    builder.add_label("Username",0,0,target="username")
    builder.add_entry("username",0,1)
    builder.add_label("Password",1,0,target="Password")
    builder.add_entry("Password",1,1,kind = "Password")
    builder.add_button('Login',2,0)
    builder.add_button('Cancel',2,1)
    return builder.form()

class AbstractBaseBuilder:
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def add_title(self,title):
        self.title = title

    @abc.abstractmethod
    def add_lable(self,text,row,column,**kwargs):
        pass

    @abc.abstractmethod
    def add_entry(self,variable,row,column,**kwargs):
        pass

    @abc.abstractmethod
    def add_button(self,text,row,column,**kwargs):
        pass

class HtmlFormBuilder(AbstractBaseBuilder):

    def __init__(self):
        self.title = "HtmlFormBuilder"
        self.items = {}

    def add_title(self,text):
        super().add_title(escape(text))

    def add_label(self,text,row,column,**kwargs):
        self.items[(row,column)] = ('<td><lable for="{}">{}</td>'
            .format(kwargs['target'],escape(text)))

    def add_entry(self, variable, row, column, **kwargs):
        html = """<td><input name="{}" type="{}" /></td>""".format(
                variable, kwargs.get("kind", "text"))
        self.items[(row, column)] = html


    def add_button(self, text, row, column, **kwargs):
        html = """<td><input type="submit" value="{}" /></td>""".format(
                escape(text))
        self.items[(row, column)] = html

    def form(self):
        html = ["<!doctype html>\n<html><head><title>{}</title></head>"
                "<body>".format(self.title), '<form><table border="0">']
        thisrow = None
        for key,value in sorted(self.items.items()):
            row,column = key
            if thisrow == None:
                html.append("<tr>")
            if thisrow != row:
                html.append('   </tr>\n<tr>')
            thisrow = row
            html.append("   " + value)
        html.append("  </tr>\n</table></form></body></html>")
        return '\n'.join(html)



if __name__ == '__main__':
    main()








