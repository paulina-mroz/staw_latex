import json

class CardTexGenerator(object):
    """docstring for CardTexGenerator."""

    def __init__(self):
        # super(CardTexGenerator, self).__init__()
        # self.arg = arg
        self.debug = True

        self.data = {}
        self.cardParams = {}
        # self.jsonFile = 'data.json'
        # self.jsonFile = 'test.json'
        self.jsonFile = 'json/damage_deck.json'
        self.jsonParams = 'json/card_style_parameters.json'
        self.outputTexFile = 'tex/cards.tex'

        self.colorTheme = "test_color"
        self.ifIncludePictures = True
        self.ifIncludeFrame = True
        self.cardSize = "mini"
        # self.cardSize = "standard"

        self.texContent = ""

        self.cardsId = ["S329", "S322"]

    def print_debug (self, message):
        if self.debug:
            print("=== DEBUG === {:s}".format(message))

    def readJsonData (self):
        with open(self.jsonFile,encoding="utf8") as f:
            self.data = json.loads(f.read())
        with open(self.jsonParams,encoding="utf8") as f:
            self.cardParams = json.loads(f.read())
        self.print_debug("readJsonData done")


    def addTex (self, line):
        self.texContent = self.texContent+line+"\n"

    def customColors (self):
        colors = self.cardParams["colors"][self.colorTheme]
        print(colors)
        self.print_debug("customColors done")

        for name,hex in colors.items():
            self.addTex(r"\definecolor{"+name+r"}{HTML}{"+hex+r"}")

    # def setTikzStyle (self):
    #     colors = self.cardParams["damage"]["color_and_black"]
    #     print(colors)
    #     size = self.cardParams["damage"]["mini"]
    #     print(size)
    #
    #     print(self.texContent)
    #     print("setTikzStyle done")

    def writeTexFile (self):
        print(self.texContent)
        f = open(self.outputTexFile, "w")
        f.write(self.texContent)
        f.close()
        self.print_debug("writeTexFile done")

    def doTheThing (self):
        self.readJsonData()
        self.customColors()
        self.writeTexFile()


if __name__ == '__main__':
    ctg = CardTexGenerator()
    ctg.doTheThing()
