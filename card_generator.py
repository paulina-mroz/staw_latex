import json

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
        # self.jsonFile = 'test.json'
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
        self.cardToProcess = self.data["damages"]
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
            texPageTmp = texPage + texRow + "\n\\vspace{1ex}\n"
            texBackPageTmp = texBackPage + texBackRow + "\n\\vspace{1ex}\n"
            texAllTmp = texAll + texPageTmp + "\n\\newpage\n"
            texAllTmp = texAllTmp + texBackPageTmp + "\n\\newpage\n"
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
            texCard = texCard + self.cardDamageTex(card)
            texCardBack = texCardBack + self.cardBackDamageTex(card)
        # elif x == 'b':
        else:
            print("Card not found!")
            return ("","")
        texCard = "\n" + texCard + "% CARD END\n% TYPE: " + card["type"] + "\n% NAME: " + card["name"]
        texCardBack = "\n" + texCardBack + "% CARD BACK END\n% TYPE: " + card["type"] + "\n% NAME: " + card["name"]
        tex = (texCard, texCardBack)
        return tex
        self.print_debug("cardTex done")

    def tikzCommand (self, style):
        if style == "clip":
            prefix = r"\clip"
        elif style == "":
            prefix = r"\draw"
        else:
            prefix = r"\draw [{:s}]".format(style)
        return prefix

    def tikzRectangle (self, style, x1, y1, x2, y2):
        prefix = self.tikzCommand(style)
        command = r"{:s} ({:.2f}cm,{:.2f}cm) rectangle ({:.2f}cm,{:.2f}cm);".format(prefix, x1, y1, x2, y2)
        return command

    def tikzCShape (self, style, x1, y1, x2, y2, title_thick, thick):
        ix1 = x1 + thick
        iy1 = y1 + thick
        iy2 = y2 - title_thick
        prefix = self.tikzCommand(style)

        command = ""
        command = command + prefix + "\n"
        command = command + r"({:.2f}cm,{:.2f}cm) [rounded corners={}cm] --".format(  x2 ,  y1 , thick)         + "\n"
        command = command + r"({:.2f}cm,{:.2f}cm) [rounded corners={}cm] --".format(  x1 ,  y1 , thick)         + "\n"
        command = command + r"({:.2f}cm,{:.2f}cm) [rounded corners={}cm] --".format(  x1 ,  y2 , title_thick/2) + "\n"
        command = command + r"({:.2f}cm,{:.2f}cm) [rounded corners={}cm] --".format(  x2 ,  y2 , title_thick/2) + "\n"
        command = command + r"({:.2f}cm,{:.2f}cm) [rounded corners={}cm] --".format(  x2 , iy2 , thick/2)       + "\n"
        command = command + r"({:.2f}cm,{:.2f}cm) [rounded corners={}cm] --".format( ix1 , iy2 , thick/2)       + "\n"
        command = command + r"({:.2f}cm,{:.2f}cm) [rounded corners={}cm] --".format( ix1 , iy1 , thick/2)       + "\n"
        command = command + r"({:.2f}cm,{:.2f}cm) [rounded corners={}cm] --".format(  x2 , iy1 , thick/2)       + "\n"
        command = command + r"cycle;"
        return command

    def tikzResizedTextNode(self, style, x, y, scale_x, scale_y, resize_height, text):
        command = r"\node [{:s}] () at ({:.2f}cm,{:.2f}cm) ".format(style, x, y)
        command = command +  r"{{\scalebox{{ {:.2f} }}[ {:.2f} ]{{\resizebox{{!}}{{ {:.2f}cm }}".format(scale_x, scale_y, resize_height)
        command = command +  r"{{{:s}}} }} }};".format(text)
        return command

    def tikzTextNode(self, style, x, y, text):
        command = r"\node [{:s}] () at ({:.2f}cm,{:.2f}cm) ".format(style, x, y)
        command = command +  r"{{{:s}}};".format(text)
        return command

    def cardDamageTex (self, card):
        tex = ""
        size = self.cardParams["sizes"][card["type"]]["mini"]

        line_width = size["line_width"]
        cw = size["card_width"]
        ch = size["card_height"]

        tex = tex + r"\begin{tikzpicture}" + "\n"
        tex = tex + r"[" + "\n"
        tex = tex + r"border_style/.style      = {{ fill=border_fill  , draw=none         , line width={:.2f}pt , rounded corners=0.0cm    }},".format(0.0) + "\n"
        tex = tex + r"card_style/.style        = {{ fill=card_fill    , draw=card_line    , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["card_round"]) + "\n"
        tex = tex + r"textbox_style/.style     = {{ fill=textbox_fill , draw=textbox_line , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["textbox_round"]) + "\n"
        tex = tex + r"panel_lines_style/.style = {{ fill=card_fill    , draw=panel_line   , line width={:.2f}pt , rounded corners=0.0cm    }},".format(line_width) + "\n"
        tex = tex + r"panel_fill_style/.style = {{ fill=panel_fill , draw=none       , line width={:.2f}pt }},".format(0.0) + "\n"
        tex = tex + r"panel_line_style/.style = {{ fill=none       , draw=panel_line , line width={:.2f}pt }},".format(line_width) + "\n"
        tex = tex + r"title_style/.style  = { rectangle , inner sep=0.05cm, minimum height = 1cm, fill=title_fill , draw=none , text=title_font , line width=0.0pt , font=\scshape\bfseries }," + "\n"
        tex = tex + r"text_style/.style  =  { rectangle , inner sep=0.05cm , align=center , fill=none , draw=none , text=black , font=\scriptsize }," + "\n"
        tex = tex + r"id_number_style/.style  =  { rectangle , inner sep=0.05cm , align=center , fill=none , draw=none , text=panel_line , font=\tiny }" + "\n"
        # tex = tex + r"text_style/.style  =  { rectangle , inner sep=0.05cm, below , align=center , fill=none , draw=none , text=black , font=\scriptsize }" + "\n"
        tex = tex + r"]" + "\n"

        border_thick = size["border_thick"]
        tex = tex + r"\begin{scope}" + "\n"
        # tex = tex + self.tikzRectangle("border_style", 0-border_thick, 0-border_thick, cw+border_thick, ch+border_thick) + "\n"
        tex = tex + self.tikzRectangle("card_style", 0, 0, cw, ch) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        title_height = size["title_height"]
        panel_thick  = size["panel_thick"]
        panel_gap    = size["panel_gap"]
        panel_outer_x1 = 0 + panel_gap
        panel_outer_x2 = cw - panel_gap
        panel_outer_y1 = 0 + panel_gap
        panel_outer_y2 = ch - panel_gap
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + self.tikzCShape("clip"            , panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick) + "\n"
        tex = tex + self.tikzCShape("panel_fill_style", panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick) + "\n"
        panel_line1_x1 = panel_outer_x1+1.2*panel_thick
        panel_line2_y2 = panel_outer_y2-1.2*title_height
        panel_line3_x1 = panel_outer_x2-1.2*panel_thick
        panel_line_thick = 0.05
        tex = tex + self.tikzRectangle("panel_lines_style", panel_line1_x1, 0, panel_line1_x1+panel_line_thick, ch) + "\n"
        tex = tex + self.tikzRectangle("panel_lines_style", 0, panel_line2_y2-panel_line_thick, cw, panel_line2_y2) + "\n"
        tex = tex + self.tikzRectangle("panel_lines_style", panel_line3_x1-panel_line_thick, 0, panel_line3_x1, ch/2) + "\n"
        tex = tex + self.tikzResizedTextNode("title_style", cw/2 + 0.05, panel_outer_y2 - title_height/2, 0.35, 1.0, title_height - 0.1, card["name"].upper()) + "\n"
        tex = tex + self.tikzTextNode("id_number_style", panel_line3_x1+((panel_outer_x2-panel_line3_x1)/2), panel_outer_y1+panel_thick/2, card["id"]) + "\n"
        tex = tex + r"\end{scope}" + "\n"
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + self.tikzCShape("panel_line_style", panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        textbox_gap = size["textbox_gap"]
        textbox_x1 = panel_outer_x1 + panel_thick + textbox_gap
        textbox_y1 = panel_outer_y1 + panel_thick + textbox_gap
        textbox_x2 = cw - panel_gap - textbox_gap
        textbox_y2 = panel_outer_y2 - title_height - textbox_gap
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + self.tikzRectangle("textbox_style", textbox_x1, textbox_y1, textbox_x2, textbox_y2) + "\n"

        card_text_from_json = card["text"]
        card_text_tmp = card_text_from_json.replace("\n\n", "\n\n\\vspace{1em}\n")
        card_text_tmp = card_text_tmp.replace("[hit]", "\inlinegraphics{../pics_vector/hit.pdf}")
        card_text_tmp = card_text_tmp.replace("[crit]", "\inlinegraphics{../pics_vector/crit.pdf}")
        card_text_tmp = card_text_tmp.replace("[talent]", "\inlinegraphics{../pics_vector/talent.pdf}")
        card_text_tmp = card_text_tmp.replace("[turn-left]", "\inlinegraphics{../pics_vector/turn-left.pdf}")
        card_text_tmp = card_text_tmp.replace("[turn-right]", "\inlinegraphics{../pics_vector/turn-right.pdf}")
        card_text_tmp = card_text_tmp.replace("[weapon]", "\inlinegraphics{../pics_vector/weapon.pdf}")
        card_text = card_text_tmp.replace("ACTION:", "\\textbf{ACTION:}")
        # tex = tex + self.tikzTextNode("text_style, text width={:.2f}cm".format(textbox_x2-textbox_x1-0.1), textbox_x1+((textbox_x2-textbox_x1)/2), textbox_y2-size["textbox_round"], card_text) + "\n"
        tex = tex + self.tikzTextNode("text_style, text width={:.2f}cm".format(textbox_x2-textbox_x1-0.2), textbox_x1+((textbox_x2-textbox_x1)/2), textbox_y2-((textbox_y2-textbox_y1)/2), card_text) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        tex = tex + r"\end{tikzpicture}" + "\n"
        return tex

    def tikzDamageBackHit (self, style):
        prefix = self.tikzCommand(style)
        command = ""
        command = command + prefix + "\n"
        command = command + """ (36.42225pt, -198.5916pt) -- (36.42225pt, -198.5916pt)
         -- (36.42225pt, -198.5916pt)
         -- (51.66899pt, -193.2883pt)
         -- (51.66899pt, -193.2883pt)
         -- (54.7941pt, -190.8261pt)
         -- (54.7941pt, -190.8261pt)
         -- (60.57082pt, -180.9773pt)
         -- (60.57082pt, -180.9773pt)
         -- (62.08601pt, -172.4542pt)
         -- (62.08601pt, -172.4542pt)
         -- (64.54823pt, -185.0494pt)
         -- (64.54823pt, -185.0494pt)
         -- (66.63163pt, -189.2162pt)
         -- (66.63163pt, -189.2162pt)
         -- (75.43875pt, -195.4664pt)
         -- (75.43875pt, -195.4664pt)
         -- (85.47698pt, -198.2127pt)
         -- (85.47698pt, -198.2127pt)
         -- (75.72285pt, -200.5802pt)
         -- (75.72285pt, -200.5802pt)
         -- (68.52563pt, -205.3152pt)
         -- (68.52563pt, -205.3152pt)
         -- (62.65422pt, -215.4481pt)
         -- (62.65422pt, -215.4481pt)
         -- (61.32841pt, -223.9712pt)
         -- (61.32841pt, -223.9712pt)
         -- (58.7715pt, -213.0806pt)
         -- (58.7715pt, -213.0806pt)
         -- (54.88879pt, -205.2205pt)
         -- (54.88879pt, -205.2205pt)
         -- (50.53258pt, -202.5689pt)
         -- (50.53258pt, -202.5689pt)
         -- (44.18766pt, -199.8226pt) -- cycle
        ;"""
        return command

    def tikzCircle (self, style, x, y, r):
        prefix = self.tikzCommand(style)
        command = r"{:s} ({:.2f}cm,{:.2f}cm) circle ({:.2f}cm);".format(prefix, x, y, r)
        return command

    def cardBackDamageTex (self, card):
        tex = ""
        size = self.cardParams["sizes"][card["type"]]["mini"]

        line_width = size["line_width"]
        cw = size["card_width"]
        ch = size["card_height"]

        tex = tex + r"\begin{tikzpicture}" + "\n"
        tex = tex + r"[" + "\n"
        tex = tex + r"border_style/.style  = {{ fill=border_fill  , draw=none         , line width={:.2f}pt    , rounded corners=0.0cm    }},".format(0.0) + "\n"
        tex = tex + r"card_style/.style    = {{ fill=dmg_back_card_fill , draw=dmg_back_card_line , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["card_round"]) + "\n"
        tex = tex + r"circle_style/.style  = {{ fill=dmg_back_card_fill!60!black , draw=dmg_back_card_line , line width={:.2f}pt }},".format(line_width) + "\n"
        tex = tex + r"hitbox_style/.style  = {{ rectangle , inner sep=0.0cm , align=center , fill=none , draw=none, line width={:.2f}pt }}".format(0.0) + "\n"
        tex = tex + r"]" + "\n"

        border_thick = size["border_thick"]
        tex = tex + r"\begin{scope}" + "\n"
        # tex = tex + self.tikzRectangle("border_style", 0-border_thick, 0-border_thick, cw+border_thick, ch+border_thick) + "\n"
        tex = tex + self.tikzRectangle("card_style", 0, 0, cw, ch) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        tex = tex + r"\begin{scope}" + "\n"
        back_hit = r"\resizebox{{ {:.2f}cm }}{{!}}{{".format(0.6*cw) + "\n"
        back_hit = back_hit + r"\begin{tikzpicture}" + "\n"
        back_hit = back_hit + r"[" + "\n"
        # back_hit = back_hit + r"hit_style/.style = {{ inner color=black , outer color=border_fill!70!black , draw=dmg_back_card_fill!60!black , line width={:.2f}pt , rounded corners=0.0cm }}".format(line_width, size["card_round"])
        back_hit = back_hit + r"hit_style/.style = {{ inner color=black , outer color=border_fill!70!black , draw=none , line width={:.2f}pt , rounded corners=0.0cm }}".format(0.0, size["card_round"])
        back_hit = back_hit + r"]" + "\n"
        back_hit = back_hit + self.tikzDamageBackHit("hit_style") + "\n"
        back_hit = back_hit + r"\end{tikzpicture}"
        back_hit = back_hit + "}" + "\n"
        tex = tex + self.tikzTextNode("hitbox_style", cw/2, ch/2, back_hit) + "\n"
        tex = tex + r"\end{scope}" + "\n"

        circle_r = 0.1
        circle_gap = 3*circle_r
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + self.tikzCircle("circle_style", 0+circle_gap, 0+circle_gap, circle_r) + "\n"
        tex = tex + self.tikzCircle("circle_style", 0+circle_gap, ch/4+0.5*circle_gap, circle_r) + "\n"
        tex = tex + self.tikzCircle("circle_style", 0+circle_gap, ch/2, circle_r) + "\n"
        tex = tex + self.tikzCircle("circle_style", 0+circle_gap, ch*3/4-0.5*circle_gap, circle_r) + "\n"
        tex = tex + self.tikzCircle("circle_style", 0+circle_gap, ch-circle_gap, circle_r) + "\n"
        tex = tex + self.tikzCircle("circle_style", cw-circle_gap, 0+circle_gap, circle_r) + "\n"
        tex = tex + self.tikzCircle("circle_style", cw-circle_gap, ch/4+0.5*circle_gap, circle_r) + "\n"
        tex = tex + self.tikzCircle("circle_style", cw-circle_gap, ch/2, circle_r) + "\n"
        tex = tex + self.tikzCircle("circle_style", cw-circle_gap, ch*3/4-0.5*circle_gap, circle_r) + "\n"
        tex = tex + self.tikzCircle("circle_style", cw-circle_gap, ch-circle_gap, circle_r) + "\n"
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
