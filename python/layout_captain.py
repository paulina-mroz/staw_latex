from tikz_commands import *

def cardCaptainTex (card, size):
    tex = ""
    cardKeysUsed = dict.fromkeys(card.keys(),False)

    line_width = size["line_width"]
    cw = size["card_width"]
    ch = size["card_height"]

    tex = tex + r"\begin{tikzpicture}" + "\n"
    tex = tex + r"[" + "\n"
    tex = tex + r"border_style/.style      = {{ fill=border_fill  , draw=none         , line width={:.2f}pt , rounded corners=0.0cm    }},".format(0.0) + "\n"
    # tex = tex + r"border_style/.style      = {{ fill=none  , draw=white         , line width={:.2f}pt , rounded corners=0.0cm    }},".format(0.0) + "\n"
    tex = tex + r"card_style/.style        = {{ fill=none    , draw=card_line    , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["card_round"]) + "\n"
    tex = tex + r"picture_style/.style     = {{anchor=north, inner sep=0, outer sep=0pt}}," + "\n"
    tex = tex + r"textbox_style/.style     = {{ fill=textbox_fill , draw=textbox_line , line width={:.2f}pt , rounded corners={:.2f}cm }},".format(line_width, size["textbox_round"]) + "\n"
    tex = tex + r"panel_lines_style/.style = {{ fill=card_fill    , draw=panel_line   , line width={:.2f}pt , rounded corners=0.0cm    }},".format(line_width) + "\n"
    tex = tex + r"panel_fill_style/.style = {{ fill=panel_fill , draw=none       , line width={:.2f}pt }},".format(0.0) + "\n"
    tex = tex + r"panel_line_style/.style = {{ fill=none       , draw=panel_line , line width={:.2f}pt }},".format(line_width) + "\n"
    tex = tex + r"title_style/.style  = { rectangle , anchor=west, inner sep=0.05cm, minimum height = 1cm, fill=title_fill , draw=none , text=title_font , line width=0.0pt , font=\scshape\bfseries }," + "\n"
    tex = tex + r"captain_style/.style  = { rectangle , anchor=east, inner sep=0.05cm, fill=none , draw=none , line width=0.0pt , font=\scshape\bfseries }," + "\n"
    tex = tex + r"text_style/.style  =  { rectangle , inner sep=0.05cm , align=left, below , fill=none , draw=none , text=black , font=\scriptsize }," + "\n"
    tex = tex + r"text_icon_style/.style  =  { inner sep=0.05cm , align=center , fill=none , draw=none }," + "\n"
    tex = tex + r"box_inner/.style       =  { draw=none, fill=card_fill }," + "\n"
    tex = tex + r"box_middle/.style      =  { draw=none, fill=box_frame }," + "\n"
    tex = tex + r"box_outer/.style       =  { draw=none, fill=card_fill }," + "\n"
    tex = tex + r"box_uniq_outer/.style  =  { draw=none, fill=panel_fill }," + "\n"
    tex = tex + r"box_upgrade_middle/.style  =  { draw=none, fill=upgrade_box_frame }," + "\n"
    tex = tex + r"box_text/.style        =  { inner sep=0.05cm, fill=none , draw=none , text=upgrade_box_frame , font=\scshape\bfseries\large }" + "\n"
    # tex = tex + r"id_number_style/.style  =  { rectangle , inner sep=0.05cm , align=center , fill=none , draw=none , text=panel_line , font=\tiny\bfseries }" + "\n"
    # tex = tex + r"text_style/.style  =  { rectangle , inner sep=0.05cm, below , align=center , fill=none , draw=none , text=black , font=\scriptsize }" + "\n"
    tex = tex + r"]" + "\n"

    border_thick = size["border_thick"]
    picture_height = size["picture_height"]
    tex = tex + r"\begin{scope}" + "\n"
    tex = tex + tikzRectangle("border_style", 0-border_thick, 0-border_thick, cw+border_thick, ch+border_thick) + "\n"
    tex = tex + r"\end{scope}" + "\n"
    tex = tex + r"\begin{scope}" + "\n"
    tex = tex + tikzRectangle("clip, rounded corners={:.2f}cm".format(size["card_round"]), 0, 0, cw, ch) + "\n"
    tex = tex + tikzRectangle("fill=card_fill", 0-border_thick, 0-border_thick, cw+border_thick, ch+border_thick) + "\n"
    tex = tex + r"\begin{scope}" + "\n"
    tex = tex + tikzRectangle("clip", 0, ch-picture_height+0.01, cw, ch) + "\n"
    tex = tex + tikzTextNode("picture_style", cw/2, ch, tikzExternalGraphics(cw, "../pics_card/{:s}_{:s}.jpg".format(card["type"], card["id"]))) + "\n"
    tex = tex + r"\end{scope}" + "\n"
    tex = tex + tikzRectangle("fill=card_fill, draw=none, path fading=north", 0-border_thick, ch-picture_height-0.01, cw+border_thick, ch-picture_height+0.3) + "\n"
    tex = tex + r"\end{scope}" + "\n"
    tex = tex + r"\begin{scope}" + "\n"
    tex = tex + tikzRectangle("card_style", 0, 0, cw, ch) + "\n"
    tex = tex + r"\end{scope}" + "\n"

    title_height   = size["title_height"]
    panel_thick    = size["panel_thick"]
    panel_gap      = size["panel_gap"]

    panel_outer_x1 = 0 + panel_gap
    panel_outer_x2 = cw - panel_gap
    panel_outer_y1 = 0 + 2*panel_gap
    panel_outer_y2 = ch - picture_height
    title_offset = 0
    if card["unique"]:
        title_offset = 0.15
    cardKeysUsed["unique"] = True

    tex = tex + r"\begin{scope}" + "\n"
    tex = tex + tikzCShape("clip"            , panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick) + "\n"
    tex = tex + tikzCShape("panel_fill_style", panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick) + "\n"
    panel_line1_x1 = panel_outer_x1+1.2*panel_thick
    panel_line2_y2 = panel_outer_y2-1.4*title_height
    panel_line3_x1 = panel_outer_x2-1.2*panel_thick
    panel_line_thick = 0.06
    tex = tex + tikzRectangle("panel_lines_style", 0, panel_line2_y2-panel_line_thick, cw, panel_line2_y2) + "\n"
    tex = tex + tikzResizedTextNode("title_style", panel_outer_x1 + 1.3*panel_thick + title_offset, panel_outer_y2 - title_height/2, 0.45, 1.0, title_height - 0.1, card["name"].upper()) + "\n"
    tex = tex + tikzResizedTextNode("captain_style", panel_outer_x2 - 0.25*title_height, panel_outer_y2 - title_height/2, 0.35, 0.8, title_height - 0.1, r"\textcolor{cost_font}{\contour{card_fill}{CAPTAIN}}") + "\n"
    tex = tex + r"\end{scope}" + "\n"
    tex = tex + r"\begin{scope}" + "\n"
    tex = tex + tikzCShape("panel_line_style", panel_outer_x1, panel_outer_y1, panel_outer_x2, panel_outer_y2, title_height, panel_thick) + "\n"
    tex = tex + r"\end{scope}" + "\n"
    cardKeysUsed["name"] = True

    textbox_gap = size["textbox_gap"]
    textbox_x1 = panel_outer_x1 + panel_thick + textbox_gap
    textbox_y1 = panel_outer_y1 + panel_thick + textbox_gap
    textbox_x2 = cw - panel_gap - textbox_gap
    textbox_y2 = panel_outer_y2 - title_height - textbox_gap
    tex = tex + r"\begin{scope}" + "\n"
    tex = tex + tikzRectangle("textbox_style", textbox_x1, textbox_y1, textbox_x2, textbox_y2) + "\n"

    items_gap = 0.04
    items_gap2 = 2.5*items_gap
    if card["unique"]:
        unique_r = 0.8*panel_thick
        unique_x = panel_outer_x1+0.9*unique_r
        unique_y = panel_outer_y2 - title_height/2
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + tikzCircle("box_uniq_outer", unique_x, unique_y, unique_r) + "\n"
        tex = tex + tikzCircle("box_inner", unique_x, unique_y, unique_r-items_gap) + "\n"
        tex = tex + r"\end{scope}" + "\n"
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + tikzCircle("clip", unique_x, unique_y, unique_r-items_gap) + "\n"
        tex = tex + tikzTextNode("text_icon_style", unique_x, unique_y, tikzExternalGraphics(1.4*unique_r, "../pics_vector/unique.pdf" )) + "\n"
        tex = tex + r"\end{scope}" + "\n"
    cardKeysUsed["unique"] = True

    text_wrap = ""
    box_height = title_height+6*items_gap
    if "range" in card:
        range_height = box_height
        range_x2 = cw - panel_gap/2
        range_x1 = range_x2 - 2*range_height
        range_y1 = textbox_y2 - 1.2*range_height
        range_y2 = range_y1 + range_height
        tex = tex + r"\begin{scope}" + "\n"
        tex = tex + tikzRectangle("box_outer,  rounded corners={:.2f}cm".format(0.45*range_height), range_x1, range_y1, range_x2, range_y2) + "\n"
        tex = tex + tikzRectangle("box_middle, rounded corners={:.2f}cm".format(0.45*range_height-items_gap), range_x1+items_gap, range_y1+items_gap, range_x2-items_gap, range_y2-items_gap) + "\n"
        tex = tex + tikzRectangle("box_inner,  rounded corners={:.2f}cm".format(0.45*range_height-items_gap2), range_x1+items_gap2, range_y1+items_gap2, range_x2-items_gap2, range_y2-items_gap2) + "\n"
        tex = tex + tikzTextNode("box_text", range_x1+(range_x2-range_x1)/2, range_y1+(range_y2-range_y1)/2, r"{:s}".format(card["range"]) ) + "\n"
        tex = tex + r"\end{scope}" + "\n"
        text_wrap = r"\setlength{{\intextsep}}{{0pt}}\setlength{{\columnsep}}{{0pt}}\begin{{wrapfigure}}{{r}}{{{:.2f}cm}}\rule{{0pt}}{{{:.2f}cm}}\end{{wrapfigure}}".format(textbox_x2-range_x1,range_y2-range_y1)
    cardKeysUsed["range"] = True


    card_text = text_wrap + tikzTextReplace(card["text"])
    tex = tex + tikzTextNode("text_style, text width={:.2f}cm".format(textbox_x2-textbox_x1-0.2), textbox_x1+((textbox_x2-textbox_x1)/2), textbox_y2-textbox_gap, card_text) + "\n"
    tex = tex + r"\end{scope}" + "\n"
    cardKeysUsed["text"] = True

    tex = tex + r"\end{tikzpicture}" + "\n"

    cardKeysUsed["id"] = True
    cardKeysUsed["set"] = True
    for k in cardKeysUsed:
        if cardKeysUsed[k]==False:
            print("WARNING: Property {:20s} not used (in {:10s} {:10s})".format(k, card["type"], card["id"]))
    return tex
