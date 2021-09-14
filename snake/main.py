from frame import *
import random
from tkinter import messagebox

head_x = 1
head_y = 0
direction = "Right"
snake = [[0, 0], [1, 0]]
last_cell = []
snake.insert(0, [head_x, head_y])
fruit_existent = False
collected = False
death = False
direction_change = False
tick = 0.1
dimension = 20
windowsize = 1200
points = 0
frame = Frame("Mouse Click", windowsize, dimension, True)


for pos in snake:
    frame.set_color(pos[0], pos[1], "green")
# |                                        |
# |   Alles was jeden Tick passieren soll  |
#\ /                                      \ /
for event in frame.get_events(tick):
    if event.type == "key" and not direction_change:
        if event.key == "Up" or event.key == "Down" or event.key == "Left" or event.key == "Right":
            if event.key == "Left" and direction == "Right" or event.key == "Right" and direction == "Left" or\
                    event.key == "Up" and direction == "Down" or event.key == "Down" and direction == "Up":
                pass
            else:
                direction = event.key
                direction_change = True
        if event.key == "w" or event.key == "s" or event.key == "a" or event.key == "d":
            if event.key == "a" and direction == "d" or event.key == "d" and direction == "a" or\
                    event.key == "w" and direction == "s" or event.key == "s" and direction == "w":
                pass
            else:
                direction = event.key
                direction_change = True
    if event.type == "tick":
        direction_change = False
        # Bewege den Kopf um 1 pro tick
        if direction == "Left" or direction == "a":
            head_x -= 1
        elif direction == "Right" or direction == "d":
            head_x += 1
        elif direction == "Up" or direction == "w":
            head_y -= 1
        elif direction == "Down" or direction == "s":
            head_y += 1

        # Töte die Schlange bei Selbstkollision
        for x in range(0, len(snake) - 1):
            if head_x == snake[x][0] and head_y == snake[x][1]:
                death = True

        # Töte die Schlange bei kollosion mit Wand
        if head_x < 0 or head_x > dimension - 1 or head_y < 0 or head_y > dimension -1 :
            death = True
        if death:
            break

        # Verändere die Schlange mit jedem Tick
        snake.insert(0, [head_x, head_y])
        if not collected:
            last_cell = snake.pop()
        else:
            collected = False
        for pos in snake:
            frame.set_color(pos[0], pos[1], "green")
        frame.set_color(last_cell[0], last_cell[1], "white")

        # Generiere die Frucht falls nicht existent
        if not fruit_existent:
            while not fruit_existent:
                fruit_x = random.randint(0, dimension - 1)
                fruit_y = random.randint(0, dimension - 1)
                for x in snake:
                    if frame.get_color(fruit_x, fruit_y) == "green":
                        fruit_existent = False
                    else:
                        fruit_existent = True
            frame.set_color(fruit_x, fruit_y, "red")
        # Prüfe, ob sich der Kopf auf der Frucht befindet
        if head_x == fruit_x and head_y == fruit_y:
            collected = True
            fruit_existent = False
            points += 1

Return.messagebox("Snake", f"{points} Points")