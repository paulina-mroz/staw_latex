def tikzCommand (style):
    if style == "clip":
        prefix = r"\clip"
    elif style == "":
        prefix = r"\draw"
    else:
        prefix = r"\draw [{:s}]".format(style)
    return prefix

def tikzRectangle (style, x1, y1, x2, y2):
    prefix = tikzCommand(style)
    command = r"{:s} ({:.2f}cm,{:.2f}cm) rectangle ({:.2f}cm,{:.2f}cm);".format(prefix, x1, y1, x2, y2)
    return command

def tikzCShape (style, x1, y1, x2, y2, title_thick, thick):
    ix1 = x1 + thick
    iy1 = y1 + thick
    iy2 = y2 - title_thick
    prefix = tikzCommand(style)

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

def tikzResizedTextNode(style, x, y, scale_x, scale_y, resize_height, text):
    command = r"\node [{:s}] () at ({:.2f}cm,{:.2f}cm) ".format(style, x, y)
    command = command +  r"{{\scalebox{{ {:.2f} }}[ {:.2f} ]{{\resizebox{{!}}{{ {:.2f}cm }}".format(scale_x, scale_y, resize_height)
    command = command +  r"{{{:s}}} }} }};".format(text)
    return command

def tikzTextNode(style, x, y, text):
    command = r"\node [{:s}] () at ({:.2f}cm,{:.2f}cm) ".format(style, x, y)
    command = command +  r"{{{:s}}};".format(text)
    return command

def tikzDamageBackHit (style):
    prefix = tikzCommand(style)
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

def tikzCircle (style, x, y, r):
    prefix = tikzCommand(style)
    command = r"{:s} ({:.2f}cm,{:.2f}cm) circle ({:.2f}cm);".format(prefix, x, y, r)
    return command
