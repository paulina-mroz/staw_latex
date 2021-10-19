import json
from layout_damage import *

class CardTexGenerator(object):
    """docstring for CardTexGenerator."""

    def __init__(self):
        # super(CardTexGenerator, self).__init__()
        # self.arg = arg
        self.debug = True

        self.data = {}
        self.cardParams = {}
        self.cardToProcess = {}
        # self.jsonFile = 'data.json'
        # self.jsonFile = 'json/test.json'
        self.jsonFile = 'json/damage_deck.json'
        self.jsonParams = 'json/card_style_parameters.json'
        self.outputTexFile = 'tex/cards.tex'

        # self.colorTheme = "test_color"
        self.colorTheme = "black_and_color"
        # self.colorTheme = "white_and_color"
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
        for name,hex in colors.items():
            self.addTex(r"\definecolor{"+name+r"}{HTML}{"+hex+r"}")
        self.print_debug("customColors done")

    def listCardsToProcess (self):
        self.cardToProcess = sum(self.data.values(), [])
        self.print_debug("listCardsToProcess done")

    def processCards (self):
        currRow = 0
        currCol = 0
        limitRow = 4
        limitCol = 4
        texAll = ""
        texAllTmp = ""
        texPage = ""
        texPageTmp = ""
        texBackPage = ""
        texBackPageTmp = ""
        texRow = ""
        texBackRow = ""
        for card in self.cardToProcess:
            texTuple = self.cardTex(card)
            texCard = texTuple[0]
            texCardBack = texTuple[1]

            texRow = texRow + texCard
            texBackRow = texCardBack + texBackRow
            texPageTmp = texPage + texRow + "\n"
            texBackPageTmp = texBackPage + texBackRow + "\n"
            texAllTmp = texAll + texPageTmp + "\\newpage"
            texAllTmp = texAllTmp + texBackPageTmp + "\\newpage"
            currCol = currCol + 1
            if currCol >= limitCol:
                currCol = 0
                texRow = ""
                texBackRow = ""
                texPage = texPageTmp
                texBackPage = texBackPageTmp
                currRow = currRow + 1
                if currRow >= limitRow:
                    currRow = 0
                    texPage = ""
                    texBackPage = ""
                    texAll = texAllTmp
        texAll = texAllTmp
        self.addTex(texAll)

        self.print_debug("processCards done")

    def cardTex (self, card):
        texCard = "% CARD BEGIN\n% TYPE: " + card["type"] + "\n% NAME: " + card["name"] + "\n"
        texCardBack = "% CARD BACK BEGIN\n% TYPE: " + card["type"] + "\n% NAME: " + card["name"] + "\n"
        type = card["type"]
        if type == "damage":
            size = self.cardParams["sizes"][card["type"]]
            texCard = texCard + cardDamageTex(card, size)
            texCardBack = texCardBack + cardBackDamageTex(card, size)
        elif type == 'captain':
            texCard = texCard + self.cardCaptainTex(card)
            # texCardBack = texCardBack + self.cardBackDamageTex(card)
        else:
            print("Card not found!")
            return ("","")
        texCard = "\n" + texCard + "% CARD END\n% TYPE: " + card["type"] + "\n% NAME: " + card["name"]
        texCardBack = "\n" + texCardBack + "% CARD BACK END\n% TYPE: " + card["type"] + "\n% NAME: " + card["name"]
        tex = (texCard, texCardBack)
        return tex
        self.print_debug("cardTex done")

    def writeTexFile (self):
        # print(self.texContent)
        f = open(self.outputTexFile, "w")
        f.write(self.texContent)
        f.close()
        self.print_debug("writeTexFile done")

    def doTheThing (self):
        self.readJsonData()
        self.customColors()
        self.listCardsToProcess()
        self.processCards()
        self.writeTexFile()


if __name__ == '__main__':
    ctg = CardTexGenerator()
    ctg.doTheThing()
