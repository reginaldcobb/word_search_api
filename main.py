from enum import Enum
import os
import random

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List

# import svgwrite
from svgutils.compose import *
from svgutils.transform import fromstring

app = FastAPI()

class AlignType(str, Enum):
    left = "left"
    middle = "middle"
    right = "right"

class PositionType(str, Enum):
    top = "top"
    bottom = "bottom"

class WordInputType(str, Enum):
    file = "file"
    list = "list"

class TitleParameters(BaseModel):
    align: str | None = AlignType.left
    position: str | None = PositionType.top
    text: str |None = "Word Search"

class WordSearchModel(BaseModel):
    input: str | None = WordInputType.list
    word_list: List[str] | None = None
    # word_file: str | None = None
    row: int | None = 10
    column: int | None = 10
    title: TitleParameters 

# Define the path to the static folder
static_folder = "static"

# Check if the static folder exists, and create it if not
if not os.path.exists(static_folder):
    os.makedirs(static_folder)

@app.post("/create_wordsearch")
async def create_wordsearch(data: WordSearchModel ):    
    # Read in words from file or from list
    if data.input == "file":
        words = []
        pass
        # if word_file:
        #     async for line in word_file:
        #         line_str = line.decode('utf-8').strip()
        #         line_words = line_str.split(',')
        #         words.extend(line_words)
        # else:
        #     return 'File selected but No file uploaded', 400
    else:
        # words = data.word_list.split(",") if data.word_list else []
        # words = [word.upper() for word in words]
        print ("words=", data.word_list)

    svg_files = get_settings(data.word_list, data.row, data.column, data.title.text, data.title.align, data.title.position)


    return {
        "input": data.input,
        "word_list": data.word_list,
        # "file_name": words_file.filename,
        "row": data.row,
        "column": data.column,
        "title": data.title.model_dump() if data.title else None,
    }

def get_settings(words, rows, cols, title, title_align, title_pos):

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
    grids = generate_puzzle(words, rows, cols, title, title_align, title_pos)
    
    # print_docx(words, grids[0], grids[1], docx_output_file, docx_output_solution_file, rows, cols, title,
    #         title_pos, title_align, font_type, font_size, font_red_value, font_green_value, font_blue_value)

    # Print the SVG version of the puzzles
    svg_files = print_svg(words, grids[0], grids[1], svg_output_file, svg_output_solution_file, rows, cols)

    # Print the Text version of the puzzles
    # print_text(words, grids[0], grids[1], text_output_file,
    #         text_output_solution_file, rows, cols)

    return (svg_files)

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
        directions.append('horizontal')
    if vert == "TRUE":
        directions.append('vertical')
    if (diag_right == "TRUE") or (diag_left == "TRUE"):
        directions.append('diagonal')

    horz_reverse_order = ["forward"]
    if horz_reverse == "TRUE":
        horz_reverse_order.append("reverse")

    vert_reverse_order = ["forward"]
    if vert_reverse == "TRUE":
        vert_reverse_order.append("reverse")


    for word in words:
        placed = False
        while not placed:
            # direction = random.choice(['horizontal', 'vertical', 'diagonal'])
            direction = random.choice(directions)
            order = random.choice(["forward", "reverse"])

            if direction == 'horizontal':
                horz_order = random.choice(horz_reverse_order)
                row = random.randint(0, rows-1)
                col = random.randint(0, cols - len(word))
                if all(grid[row][col + i] in ['-', word[i]] for i in range(len(word))):
                    if horz_order != "forward":
                        placed_word = reversed(word)
                    else:
                        placed_word = word
                    for i, letter in enumerate(placed_word):
                        grid[row][col + i] = letter.upper()
                        placed_grid[row][col + i] = letter.upper()
                    placed = True

            elif direction == 'vertical':
                vert_order = random.choice(vert_reverse_order)
                row = random.randint(0, rows - len(word))
                col = random.randint(0, cols-1)
                if all(grid[row + i][col] in ['-', word[i]] for i in range(len(word))):
                    if vert_order != "forward":
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
                    if order == "forward":
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

    # get the filename only
    # filename_only = svg_filename[:-4]
    # get the file extension only
    # extension_only = svg_filename[-4:]
    # svg_file = filename_only + '-' + request.session["name"] + extension_only
    # return_svg_file = svg_file
    
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

    # get the filename only
    # filename_only = svg_solution_filename[:-4]
    # get the file extension only
    # extension_only = svg_solution_filename[-4:]
    # svg_solution_file = filename_only + '-' + request.session["name"] + extension_only
    # return_svg_solution_file = svg_solution_file

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

        # return_svg_solution_file = "".join(["\static\\", return_svg_solution_file])
        # return_svg_solution_file = "".join(["static\\", return_svg_solution_file])
        # print("return_svg_solution_file=", return_svg_solution_file)

        # return_svg_file = "".join(["\static\\", return_svg_file])
        # return_svg_file = "".join(["static\\", return_svg_file])
        # print("return_svg_file=", return_svg_file)

        # Save the SVG files for this session
        # request.session["return_svg_file"] = return_svg_file
        # request.session["return_svg_solution_file"] = return_svg_solution_file

    return [svg_file, svg_solution_file]

