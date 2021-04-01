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
        for card in self.cardToProcess:
            self.cardTex(card)
        self.print_debug("processCards done")

    def cardTex (self, card):
        type = card["type"]
        if type == "damage":
            self.cardDamageTex(card)
        # elif x == 'b':
        else:
            print("Card not found!")
            # print(card)
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
        size = self.cardParams["sizes"][card["type"]]["mini"]

        line_width = size["line_width"]
        cw = size["card_width"]
        ch = size["card_height"]

        self.addTex(r"\begin{tikzpicture}")
        self.addTex(r"[")
        self.addTex(r"border_style/.style   = {{ fill=border_fill  , draw=none         , line width=0.0pt    , rounded corners=0.0cm    }},".format(0.0))
        self.addTex(r"card_style/.style     = {{ fill=card_fill    , draw=card_line    , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["card_round"]))
        self.addTex(r"textbox_style/.style  = {{ fill=textbox_fill , draw=textbox_line , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["textbox_round"]))
        self.addTex(r"panel_fill_style/.style = {{ fill=panel_fill , draw=none       , line width={:.2f}pt }},".format(0.0))
        self.addTex(r"panel_line_style/.style = {{ fill=none       , draw=panel_line , line width={:.2f}pt }},".format(line_width))
        self.addTex(r"title_style/.style  = { rectangle , inner sep=0.05cm, minimum height = 1cm, fill=title_fill , draw=none , text=title_font , line width=0.0pt , font=\scshape\bfseries },")
        self.addTex(r"text_style/.style  =  { rectangle , inner sep=0.05cm, below , align=center , fill=none , draw=none , text=black , font=\scriptsize }")
        self.addTex(r"]")

        border_thick = size["border_thick"]
        self.addTex(r"\begin{scope}")
        self.addTex(self.tikzRectangle("border_style", 0-border_thick, 0-border_thick, cw+border_thick, ch+border_thick))
        self.addTex(self.tikzRectangle("card_style", 0, 0, cw, ch))
        self.addTex(r"\end{scope}")

        title_height = size["title_height"]
        panel_thick  = size["panel_thick"]
        panel_gap    = size["panel_gap"]
        panel_outer_x1 = 0 + panel_gap
        panel_outer_x2 = cw - panel_gap
        panel_outer_y1 = 0 + panel_gap
        panel_outer_y2 = ch - panel_gap
        self.addTex(r"\begin{scope}")
        self.addTex(self.tikzCShape("clip"            , panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick))
        self.addTex(self.tikzCShape("panel_fill_style", panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick))
        self.addTex(self.tikzResizedTextNode("title_style", cw/2 + 0.05, panel_outer_y2 - title_height/2, 0.35, 1.0, title_height - 0.1, card["name"].upper()))
        self.addTex(r"\end{scope}")
        self.addTex(r"\begin{scope}")
        self.addTex(self.tikzCShape("panel_line_style", panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick))
        self.addTex(r"\end{scope}")

        textbox_gap = size["textbox_gap"]
        textbox_x1 = panel_outer_x1 + panel_thick + textbox_gap
        textbox_y1 = panel_outer_y1 + panel_thick + textbox_gap
        textbox_x2 = cw - panel_gap - textbox_gap
        textbox_y2 = panel_outer_y2 - title_height - textbox_gap
        self.addTex(r"\begin{scope}")
        self.addTex(self.tikzRectangle("textbox_style", textbox_x1, textbox_y1, textbox_x2, textbox_y2))

        card_text_from_json = card["text"]
        card_text_tmp = card_text_from_json.replace("\n\n", "\n\n\\vspace{1em}\n")
        card_text = card_text_tmp.replace("ACTION:", "\\textbf{ACTION:}")
        self.addTex(self.tikzTextNode("text_style, text width={:.2f}cm".format(textbox_x2-textbox_x1-0.1), textbox_x1+((textbox_x2-textbox_x1)/2), textbox_y2-size["textbox_round"], card_text))
        self.addTex(r"\end{scope}")

        self.addTex(r"\end{tikzpicture}")
        self.addTex(r"")

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
