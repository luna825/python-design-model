import os
import sys

def main():
    basedir = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(basedir,"diagram.txt")

    diagram = create_diagram(DiagramFactory())
    diagram.save(filename)
    print("wrote",filename)

def create_diagram(factory):
    diagram = factory.make_diagram(30,7)
    retangle = factory.make_retangle(4,1,22,5,"yellow")
    text = factory.make_text(7,3,"Abstract Factory")
    diagram.add(retangle)
    diagram.add(text)
    return diagram

BLANK = " "
CORNER = "+"
HORIZONTAL = "-"
VERTICAL = "|"

class DiagramFactory:

    @classmethod
    def make_diagram(cls, width ,height):
        return cls.Diagram(width,height)

    @classmethod
    def make_retangle(cls,x,y,width,height,fill="white"):
        return cls.Retangle(x,y,width,height,fill)

    @classmethod
    def make_text(cls,x,y,text):
        return cls.Text(x,y,text)

    class Diagram:
        def __init__(self,width,height):
            self.width = width
            self.height = height
            self.diagram = DiagramFactory._create_retangle(width, height, BLANK)

        def add(self, component):
            for y,row in enumerate(component.rows):
                for x,char in enumerate(row):
                    self.diagram[y+component.y][x+component.x] = char
        def save(self,filenameOrfile):
            file = None if isinstance(filenameOrfile, str) else filenameOrfile
            try:
                if file == None:
                    file = open(filenameOrfile,"w",encoding="utf-8")
                for row in self.diagram:
                    print(''.join(row),file=file)
            finally:
                if isinstance(filenameOrfile,str) and file is not None:
                    file.close()

    class Retangle:
        def __init__(self,x,y,width,height,fill):
            self.x = x
            self.y = y
            self.rows = DiagramFactory._create_retangle(width,height,
                BLANK if fill=="white" else "%")

    class Text:
        def __init__(self,x,y,text):
            self.x = x
            self.y = y
            self.rows = [list(text)]

    def _create_retangle(width,height,fill):
        rows = [[fill for _ in range(width)] for _ in range(height)]
        for x in range(1,width-1):
            rows[0][x] = HORIZONTAL
            rows[height - 1][x] = HORIZONTAL
        for y in range(1,height-1):
            rows[y][0] = VERTICAL
            rows[y][width-1]= VERTICAL
        for y,x in ((0,0),(0,width-1),(height-1,0),(height-1,width-1)):
            rows[y][x] = CORNER
        return rows


if __name__ == '__main__':
    main()
