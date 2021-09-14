"""
Ursprünglich habe ich dieses Speil zum spielen in der Konsole geschrieben,
jetzt aber mit frame.py so abgeändert, dass man es in einem schicken
"""

from frame import *
from tkinter import messagebox

frame = Frame("TicTacToe", 400 ,3, True)
field = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
player1 = "Green"
player2 = "Red"
saved = False
turn = 0
won = False
tie = False

# Function to print the field in the console
def printField():
  for row in range(0, 3):
    print()
    for column in range(0,3):
      print(f"{field[row][column]}", end = "")

while won == False and tie == False:
# turn initiation
  saved = False
  turn += 1
  if turn % 2 == 0:
    player = player2
  else:
    player = player1

# Player input
  while saved == False:
    print(f"\x0a\x0a{player}\x1b[0m's turn")
    for event in frame.get_events():
        if event.type=="click":
            row_selected = event.x
            column_selected = event.y
            break

# Save input
    saved = False
    if field[column_selected][row_selected] == 0:
      field[column_selected][row_selected] = 1 if player == player1 else 2
      frame.set_color(row_selected, column_selected, "green") if player == player1 else frame.set_color(row_selected, column_selected, "red")
      saved = True
    else:
      print("\x0A\x1b[1mThis field is already occupied\x1b[0m")

# check for win
  if player == player1:
    checkvar = 1
  elif player == player2:
    checkvar = 2
  for checkrow in range(0,3):
    if field[checkrow][0] == checkvar and field[checkrow][1] == checkvar and field[checkrow][2] == checkvar:
      for x in range(0,3):
        field[checkrow][x] = f"\x1b[32m{checkvar}\x1b[0m"
      won = True
  for checkcolumn in range(0,3):
    if field[0][checkcolumn] == checkvar and field[1][checkcolumn] == checkvar and field[2][checkcolumn] == checkvar:
      for x in range(0,3):
        field[x][checkcolumn] = f"\x1b[32m{checkvar}\x1b[0m"
      won = True
  if field[0][0] == checkvar and field[1][1] == checkvar and field[2][2] == checkvar:
    for x in range(0,3):
      field[x][x] = f"\x1b[32m{checkvar}\x1b[0m"
    won = True
  if field[0][2] == checkvar and field[1][1] == checkvar and field[2][0] == checkvar:
    field[0][2] = f"\x1b[32m{checkvar}\x1b[0m"
    field[1][1] = f"\x1b[32m{checkvar}\x1b[0m"
    field[2][0] = f"\x1b[32m{checkvar}\x1b[0m"
    won = True

# check for tie
  if field[0][0] != 0 and field[0][1] != 0 and field[0][2] != 0 and field[1][0] != 0 and field[1][1] != 0 and field[1][2] != 0 and field[2][0] != 0 and field[2][1] != 0 and field[2][2] != 0:
    tie = True

# show field
  printField()

# final output
if won:
  print(f"\x0a\x1b[1m{player} wins")
  messagebox.showinfo("TicTacToe", f"{player} wins")
elif tie:
  print("\x0aNobody wins")
  messagebox.showinfo("TicTacToe", f"Nobody wins")