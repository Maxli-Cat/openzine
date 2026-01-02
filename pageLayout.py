from PIL import Image, ImageDraw, ImageFont
import math
import os

### CONFIG SECTION

PAPER_WIDTH = 11
PAPER_HEIGHT = 17
ROWS = 3
DPI = 600
INPUT_FOLDER = "pages\\"
RELATIVE = True
CUT_LINES = True
CREASE_LINES = False
LINE_COLOR = (100,100,100)
PAGE_NUMBERS = True
PAGE_NUMBER_COLOR = (255,0,0)

### END CONFIG SECTION

SHEET_WIDTH = int(PAPER_WIDTH * DPI)
SHEET_HEIGHT = int(PAPER_HEIGHT * DPI)

PAGE_WIDTH = SHEET_WIDTH // 2
PAGE_HEIGHT = SHEET_HEIGHT // ROWS

if RELATIVE:
    base = os.getcwd()
    INPUT_FOLDER = os.path.join(base, INPUT_FOLDER)

FORWARD_CORNERS = [(0, i*PAGE_HEIGHT) for i in range(ROWS)]
BACK_CORNERS = [(PAGE_WIDTH, i * PAGE_HEIGHT) for i in range(ROWS)]
BACK_CORNERS.reverse()


if __name__ == "__main__":
    inputs = [os.path.join(INPUT_FOLDER, i) for i in os.listdir(INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, i))]
    inputs.sort()
    print("Page images:", *inputs, sep="\n")

    pages = [
        Image.open(i).convert('RGBA').resize((PAGE_WIDTH, PAGE_HEIGHT)) for i in inputs
    ]

    if PAGE_NUMBERS:
        font = ImageFont.load_default(50)
        for i, page in enumerate(pages):
            draw = ImageDraw.Draw(page)
            if i % 2 == 0:
                draw.text((PAGE_WIDTH-200, PAGE_HEIGHT - 85), f"Page {i}", fill=PAGE_NUMBER_COLOR, font=font)
            else:
                draw.text((75, PAGE_HEIGHT - 85), f"Page {i}", fill=PAGE_NUMBER_COLOR, font=font)



    pages[0].save("foronline.pdf", save_all=True, append_images=pages[1:])

    if len(pages) % (ROWS * 4) > 0:
        print(f"Warning: adding {(ROWS * 4) - (len(pages) % (ROWS * 4))} pages of padding")

    while len(pages) % (ROWS * 4) != 0:
        pages.append(Image.new('RGBA', (PAGE_WIDTH, PAGE_HEIGHT), color='white'))

    sheets = []


    for sheet in range(math.ceil(len(inputs) / (ROWS * 4))):
        front = Image.new("RGBA", (SHEET_WIDTH, SHEET_HEIGHT), color="white")
        back = Image.new("RGBA", (SHEET_WIDTH, SHEET_HEIGHT), color="white")

        start = sheet * (ROWS * 2)

        for row in range(ROWS):
            height = row * PAGE_HEIGHT
            front_left = pages[-(row*2 + 1 + start)]
            front_right = pages[row*2 + start]

            back_left = pages[row*2 + 1 + start]
            back_right = pages[-(row*2 + 2 + start)]

            front.paste(front_left, (0, PAGE_HEIGHT * row))
            back.paste(back_left, (0, PAGE_HEIGHT*row))

            front.paste(front_right, (PAGE_WIDTH, PAGE_HEIGHT * row))
            back.paste(back_right, (PAGE_WIDTH, PAGE_HEIGHT * row))

        if CUT_LINES or CREASE_LINES:
            fcanvas = ImageDraw.Draw(front)
            bcanvas = ImageDraw.Draw(back)
            if CUT_LINES:
                for i in range(ROWS):
                    fcanvas.line((0, PAGE_HEIGHT*i, SHEET_WIDTH, PAGE_HEIGHT*i), 'white', width=60)
                    bcanvas.line((0, PAGE_HEIGHT*i, SHEET_WIDTH, PAGE_HEIGHT*i), 'white', width=60)
                    fcanvas.line((0, PAGE_HEIGHT*i, SHEET_WIDTH, PAGE_HEIGHT*i), LINE_COLOR)
                    bcanvas.line((0, PAGE_HEIGHT*i, SHEET_WIDTH, PAGE_HEIGHT*i), LINE_COLOR)
            if CREASE_LINES:
                fcanvas.line((SHEET_WIDTH // 2, 0, SHEET_WIDTH // 2, SHEET_HEIGHT), LINE_COLOR)
                bcanvas.line((SHEET_WIDTH // 2, 0, SHEET_WIDTH // 2, SHEET_HEIGHT), LINE_COLOR)


        sheets.append(front)
        sheets.append(back)

    sheets[0].save("forprint.pdf", save_all=True, append_images=sheets[1:])






