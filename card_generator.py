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

        # self.colorTheme = "white_and_black"
        # self.colorTheme = "color_and_white"
        self.colorTheme = "color_and_black"
        self.ifIncludePictures = True
        self.ifIncludeFrame = True
        self.cardSize = "mini"
        # self.cardSize = "standard"

        self.texContent = ""

        self.cardsId = ["S329", "S322"]

    def print_debug (self, message):
        if self.debug:
            print(message)

    def readJsonData (self):
        with open(self.jsonFile,encoding="utf8") as f:
            self.data = json.loads(f.read())
        with open(self.jsonParams,encoding="utf8") as f:
            self.cardParams = json.loads(f.read())
        self.print_debug("readJsonData done\n===")


    def addTex (self, line):
        self.texContent = self.texContent+line+"\n"

    # def setTikzStyle (self):
    #     colors = self.cardParams["damage"]["color_and_black"]
    #     print(colors)
    #     size = self.cardParams["damage"]["mini"]
    #     print(size)
    #
    #     print(self.texContent)
    #     print("setTikzStyle done\n===")

    def writeTexFile (self):
        f = open(self.outputTexFile, "w")
        f.write(self.texContent)
        f.close()
        self.print_debug("writeTexFile done\n===")

    def doTheThing (self):
        self.readJsonData()
        self.writeTexFile()


if __name__ == '__main__':
    ctg = CardTexGenerator()
    ctg.doTheThing()
