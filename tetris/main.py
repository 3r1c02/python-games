from frame import *
from random import randint
from copy import deepcopy

debug = True

points = 0
death_test = 0
start = False
right = False
left = False
rotate_clockwise = False
rotate_counterclockwise = False
rotation = 0
right_wall = False
left_wall = False
field_on_right = False
field_on_left = False
deny_rotation = False
drop = False
reprint = False
new_obj = True
difficulty = ()


field = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
         ]

obj = ([],
       [
           [[5, 0], [5, 1], [5, 2], [5, 3]],
           [[4, 0], [5, 0], [6, 0], [7, 0]],
           [[5, 0], [5, 1], [5, 2], [5, 3]],
           [[3, 0], [4, 0], [5, 0], [6, 0]],
       ],
       [
           [[5, 0], [6, 0], [5, 1], [6, 1]],
           [[5, 0], [6, 0], [5, 1], [6, 1]],
           [[5, 0], [6, 0], [5, 1], [6, 1]],
           [[5, 0], [6, 0], [5, 1], [6, 1]],
       ],
       [
           [[5, 0], [4, 1], [5, 1], [6, 1]],
           [[5, 0], [4, 1], [4, 0], [4, -1]],
           [[5, 0], [4, -1], [5, -1], [6, -1]],
           [[5, 0], [6, 1], [6, 0], [6, -1]],
       ],
       [
           [[5, 0], [5, 1], [5, 2], [4, 2]],
           [[4, 0], [4, 1], [5, 1], [6, 1]],
           [[6, 0], [5, 0], [5, 1], [5, 2]],
           [[4, 0], [5, 0], [6, 0], [6, 1]]
       ],
       [
           [[5, 0], [5, 1], [5, 2], [6, 2]],
           [[4, 1], [4, 0], [5, 0], [6, 0]],
           [[4, 0], [5, 0], [5, 1], [5, 2]],
           [[4, 1], [5, 1], [6, 1], [6, 0]]
       ],
       [
           [[4, 0], [5, 0], [5, 1], [6, 1]],
           [[4, 0], [4, 1], [5, 1], [5, 2]],
           [[4, 0], [5, 0], [5, 1], [6, 1]],
           [[4, 0], [4, 1], [5, 1], [5, 2]]
       ],
       [
           [[4, 1], [5, 1], [5, 0], [6, 0]],
           [[5, 0], [5, 1], [4, 1], [4, 2]],
           [[4, 1], [5, 1], [5, 0], [6, 0]],
           [[5, 0], [5, 1], [4, 1], [4, 2]]
       ]
       )

colors = ["white", "green", "red", "blue", "yellow", "orange", "purple", "magenta"]

while not difficulty == 0 and not difficulty == 1 and not difficulty == 2:
    asklist_var = Input.asklist("Difficulty", "Easy", "Medium", "Hard")
    try:
        difficulty = asklist_var[0]
    except:
        pass

print (difficulty)

if difficulty == 0:
    tick = 0.7
elif difficulty == 1:
    tick = 0.5
elif difficulty == 2:
    tick = 0.35

frame = Frame("Tetris", 500, 1000, 10, 20, True)

print("Press 'space' to start game")

for event in frame.get_events():
    if event.type == "key":
        if event.key == "space":
            print("Game starts")
            break

for event in frame.get_events(tick):

    deny_rotation = False

    # Check for input
    if event.type == "key":
        if event.key == "Right":
            if not right_wall:
                right = True
        if event.key == "Left":
            if not left_wall:
                left = True
        if event.key == "Down":
            drop = True
        if event.key == "m":
            rotate_clockwise = True
        if event.key == "n":
            rotate_counterclockwise = True
        if debug:
            if event.key == "r":
                reprint = True
            if event.key == "t":
                new_obj = True
                reprint = True

    if event.type == "tick":

        # Check for death
        if death_test > 1:
            break

        # Spawn new object
        if new_obj:
            obj_nr = randint(1, len(obj) - 1)
            color = colors[obj_nr]
            current_obj = deepcopy(obj[obj_nr])
            if debug:
                print("New current_obj")
            rotation = 0
            points += 2
            new_obj = False
            for tile in current_obj[rotation]:
                frame.set_color(tile[0], tile[1], color)


        # Reset field test bools
        field_on_right = False
        field_on_left = False

        # Check if already placed block is next to obj (right)
        for tile in current_obj[rotation]:
            if not right_wall:
                if field[tile[1] + 1][tile[0] + 1] != 0:
                    field_on_right = True
                    if debug:
                        print("Field on the right side of obj")

        # Check if already placed block is next to obj (left)
        for tile in current_obj[rotation]:
            if not left_wall:
                if field[tile[1] + 1][tile[0] - 1] != 0:
                    field_on_left = True
                    if debug:
                        print("Field on the left side of obj")

        # Clear color of the current obj
        for tile in current_obj[rotation]:
            frame.set_color(tile[0], tile[1], "white")

        # Move obj to the right if 'Right' key is pressed
        if right and not right_wall and not field_on_right:
            for obj_all_rotations in current_obj:
                for tile in obj_all_rotations:
                    tile[0] += 1
                    right = False

        # Move obj to the left if 'Left' key is pressed
        if left and not left_wall and not field_on_left:
            for obj_all_rotations in current_obj:
                for tile in obj_all_rotations:
                    tile[0] -= 1
                    left = False

        # Rotate the obj clockwise
        if rotate_clockwise:
            for tile in current_obj[rotation + 1 if rotation < 3 else 0]:
                if tile[0] > len(field[0]) - 1 or tile[0] < 0:
                    if debug:
                        print("Can't rotate because of wall")
                    deny_rotation = True
                elif tile[1] >= len(field) - 1:
                    if debug:
                        print("Can't rotate because of bottom")
                    deny_rotation = True
                elif field[tile[1] + 1][tile[0]] != 0:
                    if debug:
                        print("Can't rotate because of already placed blocks")
                    deny_rotation = True
            if rotation < 3 and not deny_rotation:
                rotation += 1
            elif rotation == 3 and not deny_rotation:
                rotation = 0
            if debug and not deny_rotation:
                print("Rotated clockwise")
            rotate_clockwise = False
            deny_rotation = False

        # Rotate the obj counterclockwise
        if rotate_counterclockwise:
            for tile in current_obj[rotation - 1 if rotation > 0 else 3]:
                if tile[0] > len(field[0]) - 1 or tile[0] < 0:
                    if debug:
                        print("Can't rotate because of wall")
                    deny_rotation = True
                elif tile[1] >= len(field) - 1:
                    if debug:
                        print("Can't rotate because of bottom")
                    deny_rotation = True
                elif field[tile[1] + 1][tile[0]] != 0:
                    if debug:
                        print("Can't rotate because of already placed blocks")
                    deny_rotation = True
            if rotation > 0 and not deny_rotation:
                rotation -= 1
            elif rotation == 0 and not deny_rotation:
                rotation = 3
            if debug and not deny_rotation:
                print("Rotated counterclockwise")
            rotate_counterclockwise = False
            deny_rotation = False

        # Check if obj is at the right wall
        for tile in current_obj[rotation]:
            if tile[0] == len(field[0]) - 1:
                right_wall = True
                if debug:
                    print("At right wall")
                break
            else:
                right_wall = False

        # Check if obj is at the left wall
        for tile in current_obj[rotation]:
            if tile[0] == 0:
                left_wall = True
                if debug:
                    print("At left Wall")
                break
            else:
                left_wall = False

        # Move obj one down and color it
        if not drop:
            for obj_all_rotations in current_obj:
                for tile in obj_all_rotations:
                    tile[1] += 1
            for tile in current_obj[rotation]:
                frame.set_color(tile[0], tile[1], color)

        # Drop the obj faster if drop = True ("Down" button pressed)
        if drop:
            store_empty = 0
            for line in field:
                if line == field[0]:
                    store_empty += 1
            lowest_tile = 0
            for tile in current_obj[rotation]:
                if tile[1] > lowest_tile:
                    lowest_tile = tile[1]
            drop_amount = store_empty - lowest_tile - 2
            if drop_amount > 0:
                for obj_all_rotations in current_obj:
                    for tile in obj_all_rotations:
                        tile[1] += drop_amount
                        if debug:
                            print(f"Dropped {drop_amount}")
                for tile in current_obj[rotation]:
                    frame.set_color(tile[0], tile[1], color)
            else:
                if debug:
                    print("Can't drop")
                for obj_all_rotations in current_obj:
                    for tile in obj_all_rotations:
                        tile[1] += 1
                for tile in current_obj[rotation]:
                    frame.set_color(tile[0], tile[1], color)
            drop = False

        # Check if the obj is at the bottom of the field or on top of a previous obj
        for tile in current_obj[rotation]:
            if tile[1] == 19 and not new_obj or field[tile[1] + 1][tile[0]] != 0 and not new_obj:
                new_obj = True
                for inner_tile in current_obj[rotation]:
                    field[inner_tile[1]][inner_tile[0]] = obj_nr
                if debug:
                    print("Added bottom tiles to field")
                death_test += 1
                break
            else:
                death_test = 0

        # Remove full lines
        for y in field:
            if y[0] != 0 and y[1] != 0 and y[2] != 0 and y[3] != 0 and y[4] != 0 and y[5] \
                    != 0 and y[6] != 0 and y[7] != 0 and y[8] != 0 and y[9] != 0:
                field.remove(y)
                if debug:
                    print(f"Removed line {y}")
                field.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                points += 10
                reprint = True

        # Reprint the already placed objs
        if reprint:
            frame.clear()
            for x in range(0, len(field[0])):
                for y in range(0, len(field)):
                    if field[y][x] != 0:
                        frame.set_color(x, y, colors[field[y][x]])
            if debug:
                print("Reprinted")
            reprint = False

Return.messagebox("Tetris", f"You got {points} points")
