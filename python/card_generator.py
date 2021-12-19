import json
from layout_damage import *
from layout_upgrade import *

class CardTexGenerator(object):
    """docstring for CardTexGenerator."""

    def __init__(self):
        # super(CardTexGenerator, self).__init__()
        # self.arg = arg
        self.debug = True

        self.data = {}
        self.cardParams = {}
        self.cardToProcess = {}
        self.jsonFile = 'json/data.json'
        # self.jsonFile = 'json/damage_deck.json'
        self.jsonParams = 'json/card_style_parameters.json'
        self.outputTexFile = 'tex/cards.tex'

        self.colorTheme = "black_and_color"
        self.ifIncludePictures = True
        self.ifIncludeFrame = True

        self.texContent = ""

        self.cardsId = {"captains":["Cap106", "Cap824"], "upgrades":["W201"]}

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
        # cardToProcessAll = sum(self.data.values(), [])
        self.cardToProcess = []
        for category,cardsIdList in self.cardsId.items():
            for value in cardsIdList:
                cardToProcessTmp = [element for element in self.data[category] if element['id'] == value]
                lenCardToProcessTmp = len(cardToProcessTmp)
                if lenCardToProcessTmp == 0:
                    self.print_debug("ID not found: {:10s}".format(value))
                elif lenCardToProcessTmp > 1:
                    self.print_debug("ID present more than once {:10s}".format(value))
                self.cardToProcess.extend(cardToProcessTmp)
        self.print_debug("listCardsToProcess done")

    def processCards (self):
        currRow = 0
        currCol = 0
        limitRow = 3
        limitCol = 3
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
        elif (type == 'captain' or type == 'weapon'):
            size = self.cardParams["sizes"]["upgrade"]
            texCard = texCard + cardUpgradeTex(card, size)
            texCardBack = texCardBack + cardBackUpgradeTex(card, size)
        else:
            print("Card not found!")
            return ("","")
        texCard = "\n" + texCard + "% CARD END\n% TYPE: " + card["type"] + "\n% NAME: " + card["name"]
        texCardBack = "\n" + texCardBack + "% CARD BACK END\n% TYPE: " + card["type"] + "\n% NAME: " + card["name"]
        tex = (texCard, texCardBack)
        return tex
        self.print_debug("cardTex done")

    def writeTexFile (self):
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
