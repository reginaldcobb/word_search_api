from enum import Enum
import os
import random

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse

from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import List

# import svgwrite
from svgutils.compose import *
from svgutils.transform import fromstring

from docx import Document
from docx.shared import RGBColor
from docx.shared import Pt

app = FastAPI()

class AlignType(str, Enum):
    left = "LEFT"
    middle = "MIDDLE"
    right = "RIGHT"
class PositionType(str, Enum):
    top = "TOP"
    bottom = "BOTTOM"
class WordInputType(str, Enum):
    file = "FILE"
    list = "LIST"
class TitleParameters(BaseModel):
    align: str | None = AlignType.left
    position: str | None = PositionType.top
    text: str |None = "Word Search"
class WordSearchModel(BaseModel):
    input: str | None = WordInputType.list
    word_list: List[str] | None = None
    # word_file: str | None = None
    row: int | None = 20
    column: int | None = 20
    title: TitleParameters 

# Create a Jinja2Templates instance for rendering HTML templates
templates = Jinja2Templates(directory="templates")

# Define the path to the static folder
static_folder = "static"

# Check if the static folder exists, and create it if not
if not os.path.exists(static_folder):
    os.makedirs(static_folder)


@app.get("/file_links", response_class=HTMLResponse)
async def file_links(request: Request):
    # Define the links to the files
    # file1_link = "/static/docx-out.docx"
    file1_link = f"static/docx-out.docx"
    print("file1_link=", file1_link)
    file2_link = "/static/docx-out_solution.docx"
    file3_link = "/static/svg_out.svg"
    file4_link = "/static/svg_out_solution.svg"
    file5_link = "/static/text_out.txt"
    file6_link = "/static/text_out_solution.txt"

    # Render the HTML template and pass the file links as context variables
    return templates.TemplateResponse("template.html", {
        "request": request,
        "file1_link": file1_link,
        "file2_link": file2_link,
        "file3_link": file3_link,
        "file4_link": file4_link,
        "file5_link": file5_link,
        "file6_link": file6_link,
    })

@app.get("/get_wordsearch")
async def create_wordsearch():  
    files_to_return = []

    # List of file extensions you want to include
    file_extensions = [".txt", ".svg", ".docx"]

    for root, _, files in os.walk(static_folder):
        for file in files:
            if any(file.endswith(extension) for extension in file_extensions):
                file_path = os.path.join(root, file)
                files_to_return.append(file_path)

    # Return the files as individual responses
    responses = [FileResponse(file_path) for file_path in files_to_return]
    return responses


@app.post("/create_wordsearch")
async def create_wordsearch(data: WordSearchModel ):    
    # Read in words from file or from list
    # if data.input == WordInputType.file:
    #     words = []
    #     pass
        # if word_file:
        #     async for line in word_file:
        #         line_str = line.decode('utf-8').strip()
        #         line_words = line_str.split(',')
        #         words.extend(line_words)
        # else:
        #     return 'File selected but No file uploaded', 400

    # Set config variables
    docx_output_file = "docx-out.docx"
    docx_output_solution_file = "docx-out_solution.docx"
    svg_output_file = "svg_out.svg"
    svg_output_solution_file = "svg_out_solution.svg"
    text_output_file = "text_out.txt"
    text_output_solution_file = "text_out_solution.txt"
    font_type = "Courier"
    font_size = "15"
    font_red_value = "0x00"
    font_green_value = "0x00"
    font_blue_value = "0x00"

    # Generate the grids
    grids = generate_puzzle(data.word_list, data.row, data.column, data.title.text, data.title.align, data.title.position)
    
    print_docx(data.word_list, grids[0], grids[1], docx_output_file, docx_output_solution_file,  data.row, data.column, data.title.text,
            data.title.position, data.title.align,  font_type, font_size, font_red_value, font_green_value, font_blue_value)

    # Print the SVG version of the puzzles
    print_svg(data.word_list, grids[0], grids[1], svg_output_file, svg_output_solution_file, data.row, data.column)

    # Print the Text version of the puzzles
    print_text(data.word_list, grids[0], grids[1], text_output_file,
            text_output_solution_file, data.row, data.column)

    return {
        "input": data.input,
        "word_list": data.word_list,
        # "file_name": words_file.filename,
        "row": data.row,
        "column": data.column,
        "title": data.title.model_dump() if data.title else None,
    }


def generate_puzzle(words, rows, cols, title, title_align, title_pos):

    directions = []

    grid = [['-' for _ in range(cols)] for _ in range(rows)]
    placed_grid = [['%' for _ in range(cols)] for _ in range(rows)]

    # Set config variables to DEFAULT add these as ENUMs above
    horz = "TRUE"
    vert = "TRUE"
    diag_right = "TRUE"
    diag_left = "TRUE"
    horz_reverse = "TRUE"
    vert_reverse = "TRUE"

    if horz == "TRUE":
        directions.append('HORIZONTAL')
    if vert == "TRUE":
        directions.append('VERTICAL')
    if (diag_right == "TRUE") or (diag_left == "TRUE"):
        directions.append('DIAGONAL')

    horz_reverse_order = ["FORWARD"]
    if horz_reverse == "TRUE":
        horz_reverse_order.append("REVERSE")

    vert_reverse_order = ["FORWARD"]
    if vert_reverse == "TRUE":
        vert_reverse_order.append("REVERSE")


    for word in words:
        placed = False
        while not placed:
            direction = random.choice(directions)
            order = random.choice(["FORWARD", "REVERSE"])

            if direction == 'HORIZONTAL':
                horz_order = random.choice(horz_reverse_order)
                row = random.randint(0, rows-1)
                col = random.randint(0, cols - len(word))
                if all(grid[row][col + i] in ['-', word[i]] for i in range(len(word))):
                    if horz_order != "FORWARD":
                        placed_word = reversed(word)
                    else:
                        placed_word = word
                    for i, letter in enumerate(placed_word):
                        grid[row][col + i] = letter.upper()
                        placed_grid[row][col + i] = letter.upper()
                    placed = True

            elif direction == 'VERTICAL':
                vert_order = random.choice(vert_reverse_order)
                row = random.randint(0, rows - len(word))
                col = random.randint(0, cols-1)
                if all(grid[row + i][col] in ['-', word[i]] for i in range(len(word))):
                    if vert_order != "FORWARD":
                        placed_word = reversed(word)
                    else:
                        placed_word = word
                    for i, letter in enumerate(placed_word):
                        grid[row + i][col] = letter.upper()
                        placed_grid[row + i][col] = letter.upper()
                    placed = True
            else:  # Place Diagional
                row = random.randint(0, rows - len(word))
                col = random.randint(0, cols - len(word))
                drow = random.choice([1, -1])
                dcol = random.choice([1, -1])

                if row + (drow * (len(word) - 1)) < 0 or row + (drow * (len(word) - 1)) >= rows:
                    continue
                if col + (dcol * (len(word) - 1)) < 0 or col + (dcol * (len(word) - 1)) >= cols:
                    continue

                if all(grid[row + drow*i][col + dcol*i] in ['-', word[i]] for i in range(len(word))):
                    if order == "FORWARD":
                        placed_word = reversed(word)
                    else:
                        placed_word = word
                    for i, letter in enumerate(placed_word):
                        grid[row + drow*i][col + dcol*i] = letter.upper()
                        placed_grid[row + drow*i][col +
                                                dcol*i] = letter.upper()
                    placed = True

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '-':
                grid[row][col] = random.choice(['A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                                                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

    return [grid, placed_grid]

def print_svg(words, grid, placed_grid, svg_filename, svg_solution_filename, rows, cols):

    width = len(grid[0])
    height = len(grid)
    cell_size = cols

    words.sort()

    # Define the number of columns and rows
    num_columns = 3
    col_buffer = (width*width)/3 - cell_size
    start_col_buffer = cell_size * 3
    
    svg_file = os.path.join(static_folder, svg_filename)

    with open(svg_file, "w") as f:
        f.write(
            # Make svg display area larger to accomodate words below the puzzle
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * cell_size*2}" height="{height * cell_size *2}">\n')

        for y in range(height):
            for x in range(width):
                f.write(
                    f'\t<rect x="{x * cell_size}" y="{y * cell_size}" width="{cell_size}" height="{cell_size}" fill-opacity="0" />\n')
                f.write(
                    f'\t<text x="{x * cell_size + cell_size / 2}" y="{y * cell_size + cell_size / 2}" text-anchor="middle" alignment-baseline="middle" fill="black">{grid[y][x]}</text>\n')

        # Loop over the words and add them to the SVG file
        for i, word in enumerate(words):
            # Calculate the row and column for this word
            row = i // num_columns
            col = i % num_columns
            f.write(f'\t<text x="{(col * (cell_size  + col_buffer)) + start_col_buffer}" y="{(row) * cell_size + cell_size / 2 + cell_size * cell_size }" text-anchor="middle" alignment-baseline="middle" fill="black" >{word}</text>\n')

        f.write('</svg>\n')

    svg_solution_file = os.path.join(static_folder, svg_solution_filename)

    with open(svg_solution_file, "w") as solution:
        solution.write(
            # Make svg display area larger to accomodate words below the puzzle
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * cell_size*2}" height="{height * cell_size*2}">\n')
        for y in range(height):
            for x in range(width):
                if (placed_grid[y][x]) == '%':
                    # Not a word so print black
                    solution.write(
                        f'\t<rect x="{x * cell_size}" y="{y * cell_size}" width="{cell_size}" height="{cell_size}" fill-opacity="0" />\n')
                    solution.write(
                        f'\t<text x="{x * cell_size + cell_size / 2}" y="{y * cell_size + cell_size / 2}" text-anchor="middle" alignment-baseline="middle" fill="black">{grid[y][x]}</text>\n')

                else:
                    # a placed word so print Red
                    solution.write(
                        f'\t<rect x="{x * cell_size}" y="{y * cell_size}" width="{cell_size}" height="{cell_size}" fill-opacity="0" />\n')
                    solution.write(
                        f'\t<text x="{x * cell_size + cell_size / 2}" y="{y * cell_size + cell_size / 2}" text-anchor="middle" alignment-baseline="middle" fill="blue" font-weight = "900">{grid[y][x]}</text>\n')

        # Loop over the words and add them to the SVG file
        for i, word in enumerate(words):
            # Calculate the row and column for this word
            row = i // num_columns
            col = i % num_columns
            solution.write(
                f'\t<text x="{(col * (cell_size  + col_buffer)) + start_col_buffer}" y="{(row) * cell_size + cell_size / 2 + cell_size * cell_size }" text-anchor="middle" alignment-baseline="middle" fill="blue" font-weight = "900">{word}</text>\n')

        solution.write('</svg>\n')

    return [svg_file, svg_solution_file]

def print_docx(words, grid, placed_grid, docx_filename, docx_filename_solution, width, height, puzzle_title, puzzle_title_position, puzzle_title_align, font_type, font_size, red, green, blue):

    mydoc = Document()
    mydoc_docx = mydoc.add_paragraph()

    style = mydoc.styles['Normal']
    font = style.font
    font.name = font_type
    font.size = Pt(int(font_size))

    words.sort()
    longest_word = ''

    for word in words:
        if len(word) > len(longest_word):
            longest_word = word

    # Check how title is aliigned
    if (puzzle_title_align == AlignType.left):
        title_space = 0
    elif (puzzle_title_align == AlignType.right):
        title_space = int((int(height)*2 - len(puzzle_title) - 1))
    else:
        title_space = int((int(height)*2 - len(puzzle_title)) / 2)

    # Check if Print at TOP or BOTTOM
    if (puzzle_title_position == PositionType.top):
        # Print the Title First

        for i in range(title_space):
            doc = mydoc_docx.add_run(" ")

        # print Title
        doc = mydoc_docx.add_run(puzzle_title)
        doc = mydoc_docx.add_run("\n")

    for x in range(width):
        for y in range(height):
            out = (grid[x][y])
            doc = mydoc_docx.add_run(out)
            doc = mydoc_docx.add_run(" ")
        doc = mydoc_docx.add_run("\n")

    if (puzzle_title_position == PositionType.bottom):
        # Print the Title First

        for i in range(title_space):
            doc = mydoc_docx.add_run(" ")

            # print Title
        doc = mydoc_docx.add_run(puzzle_title)
        doc = mydoc_docx.add_run("\n")

    # Define the number of columns and rows
    num_columns = 3
    col_buffer = 4

    # Loop over the words and add them to the SVG file
    for i, word in enumerate(words):
        row = i // num_columns
        col = i % num_columns
        doc = mydoc_docx.add_run(word)
        for j in range(col_buffer + (len(longest_word) - len(word))):
            doc = mydoc_docx.add_run(" ")
        if (col == 2):
            doc = mydoc_docx.add_run("\n")

    filename = os.path.join(static_folder, docx_filename)
    mydoc.save(filename)

    # Print the Solution Puzzle

    mydoc_solution = Document()
    mydoc_docx = mydoc_solution.add_paragraph()

    style = mydoc_solution.styles['Normal']
    font = style.font
    font.name = font_type
    font.size = Pt(int(font_size))

    # mydoc.add_page_break()

    # Check if Print at TOP or BOTTOM
    if (puzzle_title_position == PositionType.top):
        # Print the Title First

        for i in range(title_space):
            doc = mydoc_docx.add_run(" ")

            # print Title
        doc = mydoc_docx.add_run(puzzle_title)
        doc = mydoc_docx.add_run("\n")

    for x in range(width):
        for y in range(height):
            if (placed_grid[x][y]) == '%':
                out = (grid[x][y])
                doc = mydoc_docx.add_run(out).bold = False
            else:
                out = (placed_grid[x][y])
                doc = mydoc_docx.add_run(
                    out).font.color.rgb = RGBColor(0, 0, 255)
            doc = mydoc_docx.add_run(" ")
        doc = mydoc_docx.add_run("\n")

    if (puzzle_title_position == PositionType.bottom):
        # Print the Title First
        for i in range(title_space):
            doc = mydoc_docx.add_run(" ")

        # print Title
        doc = mydoc_docx.add_run(puzzle_title)
        doc = mydoc_docx.add_run("\n")

    # Define the number of columns and rows
    num_columns = 3
    col_buffer = 4

    # Loop over the words and add them to the SVG file
    for i, word in enumerate(words):
        row = i // num_columns
        col = i % num_columns
        doc = mydoc_docx.add_run(word)
        for j in range(col_buffer + (len(longest_word) - len(word))):
            doc = mydoc_docx.add_run(" ")
        if (col == 2):
            doc = mydoc_docx.add_run("\n")

    # get the filename only
    filename = os.path.join(static_folder, docx_filename_solution)
    mydoc_solution.save(filename)


def print_text(words, grid, placed_grid, text_filename, test_solution_filename, rows, cols):

    words.sort()
    longest_word = ''
    for word in words:
        if len(word) > len(longest_word):
            longest_word = word

    # create text filie
    text_file = os.path.join(static_folder, text_filename)

    # create text file for solution
    text_solution_file = os.path.join(static_folder, test_solution_filename)

    # Define the number of columns and rows
    num_columns = 3
    col_buffer = 4

    with open(text_file, 'w') as f:
        for x in range(rows):
            for y in range(cols):
                f.write(grid[x][y])
                f.write(" ")
            f.write('\n')

        # Loop over the words and add them to the SVG file
        for i, word in enumerate(words):
            row = i // num_columns
            col = i % num_columns
            f.write(word)
            for j in range(col_buffer + (len(longest_word) - len(word))):
                f.write(" ")
            if (col == 2):
                f.write("\n")

    with open(text_solution_file, 'w') as f:

        for x in range(rows):
            for y in range(cols):
                if (placed_grid[x][y] == "%"):
                    f.write(" ")
                else:
                    f.write(placed_grid[x][y])
                f.write(" ")

            f.write('\n')

        # Loop over the words and add them to the SVG file
        for i, word in enumerate(words):
            row = i // num_columns
            col = i % num_columns
            f.write(word)
            for j in range(col_buffer + (len(longest_word) - len(word))):
                f.write(" ")
            if (col == 2):
                f.write("\n")

