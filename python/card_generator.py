import json
from tikz_commands import *

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
            texCard = texCard + self.cardDamageTex(card, size)
            texCardBack = texCardBack + self.cardBackDamageTex(card, size)
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

    def cardDamageTex (self, card, size):
        tex = ""

        line_width = size["line_width"]
        cw = size["card_width"]
        ch = size["card_height"]

        tex = tex + r"\begin{tikzpicture}" + "\n"
        tex = tex + r"[" + "\n"
        # tex = tex + r"border_style/.style      = {{ fill=border_fill  , draw=none         , line width={:.2f}pt , rounded corners=0.0cm    }},".format(0.0) + "\n"
        tex = tex + r"border_style/.style      = {{ fill=none  , draw=white         , line width={:.2f}pt , rounded corners=0.0cm    }},".format(0.0) + "\n"
        tex = tex + r"card_style/.style        = {{ fill=card_fill    , draw=card_line    , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["card_round"]) + "\n"
        tex = tex + r"textbox_style/.style     = {{ fill=textbox_fill , draw=textbox_line , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["textbox_round"]) + "\n"
        tex = tex + r"panel_lines_style/.style = {{ fill=card_fill    , draw=panel_line   , line width={:.2f}pt , rounded corners=0.0cm    }},".format(line_width) + "\n"
        tex = tex + r"panel_fill_style/.style = {{ fill=panel_fill , draw=none       , line width={:.2f}pt }},".format(0.0) + "\n"
        tex = tex + r"panel_line_style/.style = {{ fill=none       , draw=panel_line , line width={:.2f}pt }},".format(line_width) + "\n"
        tex = tex + r"title_style/.style  = { rectangle , inner sep=0.05cm, minimum height = 1cm, fill=title_fill , draw=none , text=title_font , line width=0.0pt , font=\scshape\bfseries }," + "\n"
        tex = tex + r"text_style/.style  =  { rectangle , inner sep=0.05cm , align=center , fill=none , draw=none , text=black , font=\scriptsize }," + "\n"
        tex = tex + r"id_number_style/.style  =  { rectangle , inner sep=0.05cm , align=center , fill=none , draw=none , text=panel_line , font=\tiny\bfseries }" + "\n"
        # tex = tex + r"text_style/.style  =  { rectangle , inner sep=0.05cm, below , align=center , fill=none , draw=none , text=black , font=\scriptsize }" + "\n"
        tex = tex + r"]" + "\n"

        border_thick = size["border_thick"]
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + tikzRectangle("border_style", 0-border_thick, 0-border_thick, cw+border_thick, ch+border_thick) + "\n"
        tex = tex + tikzRectangle("card_style", 0, 0, cw, ch) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        title_height = size["title_height"]
        panel_thick  = size["panel_thick"]
        panel_gap    = size["panel_gap"]
        panel_outer_x1 = 0 + panel_gap
        panel_outer_x2 = cw - panel_gap
        panel_outer_y1 = 0 + panel_gap
        panel_outer_y2 = ch - panel_gap
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + tikzCShape("clip"            , panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick) + "\n"
        tex = tex + tikzCShape("panel_fill_style", panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick) + "\n"
        panel_line1_x1 = panel_outer_x1+1.2*panel_thick
        panel_line2_y2 = panel_outer_y2-1.2*title_height
        panel_line3_x1 = panel_outer_x2-1.2*panel_thick
        panel_line_thick = 0.05
        tex = tex + tikzRectangle("panel_lines_style", panel_line1_x1, 0, panel_line1_x1+panel_line_thick, ch) + "\n"
        tex = tex + tikzRectangle("panel_lines_style", 0, panel_line2_y2-panel_line_thick, cw, panel_line2_y2) + "\n"
        tex = tex + tikzRectangle("panel_lines_style", panel_line3_x1-panel_line_thick, 0, panel_line3_x1, ch/2) + "\n"
        tex = tex + tikzResizedTextNode("title_style", cw/2 + 0.05, panel_outer_y2 - title_height/2, 0.35, 1.0, title_height - 0.1, card["name"].upper()) + "\n"
        tex = tex + tikzTextNode("id_number_style", panel_line3_x1+((panel_outer_x2-panel_line3_x1)/2), panel_outer_y1+panel_thick/2, card["id"]) + "\n"
        tex = tex + r"\end{scope}" + "\n"
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + tikzCShape("panel_line_style", panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        textbox_gap = size["textbox_gap"]
        textbox_x1 = panel_outer_x1 + panel_thick + textbox_gap
        textbox_y1 = panel_outer_y1 + panel_thick + textbox_gap
        textbox_x2 = cw - panel_gap - textbox_gap
        textbox_y2 = panel_outer_y2 - title_height - textbox_gap
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + tikzRectangle("textbox_style", textbox_x1, textbox_y1, textbox_x2, textbox_y2) + "\n"

        card_text_from_json = card["text"]
        card_text_tmp = card_text_from_json.replace("\n\n", "\n\n\\vspace{1em}\n")
        card_text_tmp = card_text_tmp.replace("[hit]", "\inlinegraphics{../pics_vector/hit.pdf}")
        card_text_tmp = card_text_tmp.replace("[crit]", "\inlinegraphics{../pics_vector/crit.pdf}")
        card_text_tmp = card_text_tmp.replace("[talent]", "\inlinegraphics{../pics_vector/talent.pdf}")
        card_text_tmp = card_text_tmp.replace("[turn-left]", "\inlinegraphics{../pics_vector/turn-left.pdf}")
        card_text_tmp = card_text_tmp.replace("[turn-right]", "\inlinegraphics{../pics_vector/turn-right.pdf}")
        card_text_tmp = card_text_tmp.replace("[weapon]", "\inlinegraphics{../pics_vector/weapon.pdf}")
        card_text = card_text_tmp.replace("ACTION:", "\\textbf{ACTION:}")
        # tex = tex + tikzTextNode("text_style, text width={:.2f}cm".format(textbox_x2-textbox_x1-0.1), textbox_x1+((textbox_x2-textbox_x1)/2), textbox_y2-size["textbox_round"], card_text) + "\n"
        tex = tex + tikzTextNode("text_style, text width={:.2f}cm".format(textbox_x2-textbox_x1-0.2), textbox_x1+((textbox_x2-textbox_x1)/2), textbox_y2-((textbox_y2-textbox_y1)/2), card_text) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        tex = tex + r"\end{tikzpicture}" + "\n"
        return tex

    def cardBackDamageTex (self, card, size):
        tex = ""

        line_width = size["line_width"]
        cw = size["card_width"]
        ch = size["card_height"]

        tex = tex + r"\begin{tikzpicture}" + "\n"
        tex = tex + r"[" + "\n"
        # tex = tex + r"border_style/.style  = {{ fill=border_fill  , draw=none         , line width={:.2f}pt    , rounded corners=0.0cm    }},".format(0.0) + "\n"
        tex = tex + r"border_style/.style  = {{ fill=dmg_back_card_fill  , draw=dmg_back_card_fill         , line width={:.2f}pt    , rounded corners=0.0cm    }},".format(0.0) + "\n"
        tex = tex + r"card_style/.style    = {{ fill=dmg_back_card_fill , draw=none , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["card_round"]) + "\n"
        tex = tex + r"circle_style/.style  = {{ fill=dmg_back_card_fill!60!black , draw=dmg_back_card_line , line width={:.2f}pt }},".format(line_width) + "\n"
        tex = tex + r"hitbox_style/.style  = {{ rectangle , inner sep=0.0cm , align=center , fill=none , draw=none, line width={:.2f}pt }}".format(0.0) + "\n"
        tex = tex + r"]" + "\n"

        border_thick = size["border_thick"]
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + tikzRectangle("border_style", 0-border_thick, 0-border_thick, cw+border_thick, ch+border_thick) + "\n"
        tex = tex + tikzRectangle("card_style", 0, 0, cw, ch) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        tex = tex + r"\begin{scope}" + "\n"
        back_hit = r"\resizebox{{ {:.2f}cm }}{{!}}{{".format(0.6*cw) + "\n"
        back_hit = back_hit + r"\begin{tikzpicture}" + "\n"
        back_hit = back_hit + r"[" + "\n"
        # back_hit = back_hit + r"hit_style/.style = {{ inner color=black , outer color=border_fill!70!black , draw=dmg_back_card_fill!60!black , line width={:.2f}pt , rounded corners=0.0cm }}".format(line_width, size["card_round"])
        back_hit = back_hit + r"hit_style/.style = {{ inner color=black , outer color=border_fill!85!black , draw=none , line width={:.2f}pt , rounded corners=0.0cm }}".format(0.0, size["card_round"])
        back_hit = back_hit + r"]" + "\n"
        back_hit = back_hit + tikzDamageBackHit("hit_style") + "\n"
        back_hit = back_hit + r"\end{tikzpicture}"
        back_hit = back_hit + "}" + "\n"
        tex = tex + tikzTextNode("hitbox_style", cw/2, ch/2, back_hit) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        circle_r = 0.1
        circle_gap = 3*circle_r
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + tikzCircle("circle_style", 0+circle_gap, 0+circle_gap, circle_r) + "\n"
        tex = tex + tikzCircle("circle_style", 0+circle_gap, ch/4+0.5*circle_gap, circle_r) + "\n"
        tex = tex + tikzCircle("circle_style", 0+circle_gap, ch/2, circle_r) + "\n"
        tex = tex + tikzCircle("circle_style", 0+circle_gap, ch*3/4-0.5*circle_gap, circle_r) + "\n"
        tex = tex + tikzCircle("circle_style", 0+circle_gap, ch-circle_gap, circle_r) + "\n"
        tex = tex + tikzCircle("circle_style", cw-circle_gap, 0+circle_gap, circle_r) + "\n"
        tex = tex + tikzCircle("circle_style", cw-circle_gap, ch/4+0.5*circle_gap, circle_r) + "\n"
        tex = tex + tikzCircle("circle_style", cw-circle_gap, ch/2, circle_r) + "\n"
        tex = tex + tikzCircle("circle_style", cw-circle_gap, ch*3/4-0.5*circle_gap, circle_r) + "\n"
        tex = tex + tikzCircle("circle_style", cw-circle_gap, ch-circle_gap, circle_r) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        tex = tex + r"\end{tikzpicture}" + "\n"
        return tex

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
