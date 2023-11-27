import svgwrite
import random

def create_word_search_puzzle(words, size):
    puzzle = [['A' for _ in range(size)] for _ in range(size)]

    for word in words:
        direction = random.choice(['horizontal', 'vertical', 'diagonal'])
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)

        if direction == 'horizontal':
            while y + len(word) > size:
                y = random.randint(0, size - 1)
            for i in range(len(word)):
                puzzle[x][y + i] = word[i]

        elif direction == 'vertical':
            while x + len(word) > size:
                x = random.randint(0, size - 1)
            for i in range(len(word)):
                puzzle[x + i][y] = word[i]

        elif direction == 'diagonal':
            while x + len(word) > size or y + len(word) > size:
                x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            for i in range(len(word)):
                puzzle[x + i][y + i] = word[i]

    return puzzle

def draw_word_search_puzzle(puzzle, file_name):
    dwg = svgwrite.Drawing(file_name, profile='tiny')

    cell_size = 20
    for i, row in enumerate(puzzle):
        for j, char in enumerate(row):
            # Set background rectangle with light grey color and fill opacity of 0
            dwg.add(dwg.rect((j * cell_size, i * cell_size), (cell_size, cell_size), fill='blue', fill_opacity=0))
            # Add text
            text = dwg.text(char, insert=(j * cell_size + 8, i * cell_size + 15), font_size="12")

            # Add a box around the character at position (1, 1)
            # if i == 1 and j == 1:
            #     box = dwg.rect((j * cell_size, i * cell_size), (cell_size, cell_size), fill='none', stroke='red', stroke_width=1)
            #     dwg.add(box)

             # Add a circle around the character at position (1, 1) with a thin blue line
            # if i == 1 and j == 1:
            #     radius = cell_size / 2
            #     center = (j * cell_size + radius, i * cell_size + radius)
            #     circle = dwg.circle(center=center, r=radius, fill='none', stroke='red', stroke_width=1)
            #     dwg.add(circle)   

            # if i == 7 and j == 7:
            #     radius = cell_size / 2
            #     center = (j * cell_size + radius, i * cell_size + radius)
            #     path_data = f"M {center[0] - radius} {center[1]} A {radius} {radius} 0 0 0 {center[0] + radius} {center[1]}"
            #     path = dwg.path(d=path_data, fill='none', stroke='blue', stroke_width=1)
            #     dwg.add(path)       

            # Add a half-circle to the left of the character at position (1, 1) with a thin blue line
            # if i == 7 and j == 7:
            #     radius = cell_size / 2
            #     center = (j * cell_size - radius, i * cell_size + radius)
            #     path_data = f'M {center[0]} {center[1]} A {radius} {radius} 0 0 1 {center[0]} {center[1] + 2 * radius}'
            #     path = dwg.path(d=path_data, fill='none', stroke='blue', stroke_width=1)
            #     dwg.add(path)

            # Add a half-circle to the left side of the character at position (1, 1) with a thin blue line
            if i == 1 and j == 1:
                radius = cell_size
                center = (j * cell_size, i * cell_size + radius)
                path_data = f"M{j * cell_size},{i * cell_size} A{radius},{radius} 0 0,0 {j * cell_size},{(i + 1) * cell_size}"
                half_circle = dwg.path(d=path_data, fill='none', stroke='red', stroke_width=1)
                dwg.add(half_circle)


            # Draw lines at the top and bottom of cell (4, 4)
            # if i == 4:
                # dwg.add(dwg.line((j * cell_size, i * cell_size), ((j + 1) * cell_size, i * cell_size), stroke='blue', stroke_width=1))
                # dwg.add(dwg.line((j * cell_size, (i + 1) * cell_size), ((j + 1) * cell_size, (i + 1) * cell_size), stroke='blue', stroke_width=1))

            # Draw lines at the left and right of cell (9, 9)
            # if j == 9:
                # dwg.add(dwg.line((j * cell_size, i * cell_size), (j * cell_size, (i + 1) * cell_size), stroke='blue', stroke_width=1))
                # dwg.add(dwg.line(((j + 1) * cell_size, i * cell_size), ((j + 1) * cell_size, (i + 1) * cell_size), stroke='blue', stroke_width=1))

            # Add borders at the top and bottom of the cell at position (4, 4) with a thin red line
            if i == 1 and j == 1:
                top_border = dwg.line(start=(j * cell_size, i * cell_size), end=((j + 1) * cell_size, i * cell_size), stroke='red', stroke_width=1)
                bottom_border = dwg.line(start=(j * cell_size, (i + 1) * cell_size), end=((j + 1) * cell_size, (i + 1) * cell_size), stroke='red', stroke_width=1)
                dwg.add(top_border)
                dwg.add(bottom_border)

            if i == 1 and j == 2:
                top_border = dwg.line(start=(j * cell_size, i * cell_size), end=((j + 1) * cell_size, i * cell_size), stroke='red', stroke_width=1)
                bottom_border = dwg.line(start=(j * cell_size, (i + 1) * cell_size), end=((j + 1) * cell_size, (i + 1) * cell_size), stroke='red', stroke_width=1)
                dwg.add(top_border)
                dwg.add(bottom_border)

           # Add a half-circle to the right side of the character at position (1, 1) with a thin green line
            if i == 1 and j == 2:
                radius = cell_size
                center = ((j + 1) * cell_size, i * cell_size + radius)
                path_data = f"M{(j + 1) * cell_size},{i * cell_size} A{radius},{radius} 0 0,1 {(j + 1) * cell_size},{(i + 1) * cell_size}"
                half_circle_right = dwg.path(d=path_data, fill='none', stroke='red', stroke_width=1)
                dwg.add(half_circle_right)

            # Add a half-circle to the top half of the cell at position (9, 9) with a thin orange line
            if i == 9 and j == 9:
                radius = cell_size
                center = (j * cell_size + radius, i * cell_size)
                path_data = f"M{j * cell_size},{i * cell_size} A{radius},{radius} 0 0,1 {(j + 1) * cell_size},{i * cell_size}"
                half_circle_top = dwg.path(d=path_data, fill='none', stroke='red', stroke_width=1)
                dwg.add(half_circle_top)

             # Add borders at the left and right of the cell at position (9, 9) with a thin blue line
            if i == 9 and j == 9:
                left_border = dwg.line(start=(j * cell_size, i * cell_size), end=(j * cell_size, (i + 1) * cell_size), stroke='red', stroke_width=1)
                right_border = dwg.line(start=((j + 1) * cell_size, i * cell_size), end=((j + 1) * cell_size, (i + 1) * cell_size), stroke='red', stroke_width=1)
                dwg.add(left_border)
                dwg.add(right_border)

            # Add a half-circle to the top half of the cell at position (9, 9) with a thin orange line
            if i == 9 and j == 9:
                radius = cell_size
                center = (j * cell_size + radius, (i + 1) * cell_size)
                path_data = f"M{j * cell_size},{(i + 1) * cell_size} A{radius},{radius} 0 0,0 {(j + 1) * cell_size},{(i + 1) * cell_size}"
                half_circle_bottom = dwg.path(d=path_data, fill='none', stroke='red', stroke_width=1)
                dwg.add(half_circle_bottom)

            # Add a half circle centered in the upper left corner of the cell at position (4, 4) with a thin blue line
            # if i == 4 and j == 4:
            #     radius = cell_size / 2
            #     center = (j * cell_size + radius, i * cell_size + radius)
            #     path_data = f"M{center[0]},{center[1] - radius} A{radius},{radius} 0 1,0 {center[0] + radius},{center[1]} Z"
            #     half_circle = dwg.path(d=path_data, fill='none', stroke='blue', stroke_width=1)
            #     dwg.add(half_circle)

            # Add an ellipse centered in the upper left corner of the cell at position (4, 4) with a thin green line
            # if i == 4 and j == 4:
            #     cx = j * cell_size + cell_size / 2
            #     cy = i * cell_size + cell_size / 2
            #     rx = cell_size / 2
            #     ry = cell_size / 2.5
            #     ellipse = dwg.ellipse(center=(cx, cy), r=(rx, ry), fill='none', stroke='green', stroke_width=1)
            #     # Rotate the ellipse 
            #     ellipse.rotate(45, center=(cx, cy))
            #     dwg.add(ellipse)


            # Add a half-ellipse at cell (16, 16)
            if i == 16 and j == 16:
                cx = (j + 0.5) * cell_size
                cy = (i + 0.5) * cell_size
                rx = cell_size / 3
                ry = cell_size / 3
                path_data = f"M{cx - rx},{cy} A{rx},{ry} 0 1,1 {cx + rx},{cy} "
                half_ellipse = dwg.path(d=path_data, fill='none', stroke='green', stroke_width=1)
                # Rotate the ellipse 
                half_ellipse.rotate(-30, center=(cx, cy))
                dwg.add(half_ellipse)


                # Draw a line from the end of the half-ellipse to cell (17, 17)
                end_x = (j + 1) * cell_size
                end_y = (i + 1) * cell_size
                line = dwg.line(start=(cx + rx, cy), end=(end_x, end_y), stroke='red', stroke_width=1)
                line.rotate(-30, center=(cx, cy))
                dwg.add(line)


            # Add a half-ellipse at cell (18, 18)
            if i == 18 and j == 18:
                cx = (j + 0.5) * cell_size
                cy = (i + 0.5) * cell_size
                rx = cell_size / 3
                ry = cell_size / 3
                path_data = f"M{cx - rx +1},{cy} A{rx},{ry} 0 1,1 {cx + rx},{cy} "
                half_ellipse = dwg.path(d=path_data, fill='none', stroke='green', stroke_width=1)
                # Rotate the ellipse 
                half_ellipse.rotate(135, center=(cx, cy))
                dwg.add(half_ellipse)




            dwg.add(text)






            dwg.add(text)

    dwg.save()

# Example usage:
word_list = ['python', 'code', 'svg', 'word', 'search']
puzzle_size = 20

word_search_puzzle = create_word_search_puzzle(word_list, puzzle_size)
draw_word_search_puzzle(word_search_puzzle, 'word_search_puzzle_with_background_and_line.svg')
