import tkinter as tk
from tkinter import messagebox

# (center_x, center_y):slot in grid
grid_dict = {(75,75):0,
             (250,75):1,
             (425,75):2,
             (75,250):3,
             (250,250):4,
             (425,250):5,
             (75,425):6,
             (250,425):7,
             (425,425):8}

x, y = 0, 0
x1, x2, x3, x4, high = 150, 175, 325, 350, 500
square_width = 150
c_1 = x1 / 2
c_2 = (x3 + x2) / 2
c_3 = (high + x4) / 2

def check_slot(x, y):
  grid_ind = grid_dict[(x, y)]
  if grid[grid_ind] == '':
    if count % 2 == 0:
      temp = 'X'
    else:
      temp = 'O'
    grid[grid_ind] = temp
  else:
    return 'bad'

def handle_click():
  x_c = 0
  y_c = 0
  if 0 < x and x < x1:
    x_c = c_1
  elif x2 < x and x < x3:
    x_c = c_2
  elif x4 < x and x < 500:
    x_c = c_3

  if 0 < y and y < x2:
    y_c = c_1
  elif x2 < y and y < x3:
    y_c = c_2
  elif x4 < y and y < 500:
    y_c = c_3
  
  return x_c, y_c

def game_over():
  var = ''
  
  if grid[3] == grid[4] and grid[5] == grid[4] and grid[4] != '':
    var = 4
  if grid[1] == grid[4] and grid[7] == grid[4] and grid[4] != '':
    var = 4
  if grid[0] == grid[4] and grid[8] == grid[4] and grid[4] != '':
    var = 4
  if grid[2] == grid[4] and grid[6] == grid[4] and grid[4] != '':
    var = 4
  
  if grid[1] == grid[0] and grid[2] == grid[0] and grid[0] != '':
    var = 0
  if grid[3] == grid[0] and grid[6] == grid[0] and grid[0] != '':
    var = 0

  if grid[2] == grid[8] and grid[5] == grid[8] and grid[8] != '':
    var = 8
  if grid[6] == grid[8] and grid[7] == grid[8] and grid[8] != '':
    var = 8

  if var != '':
    return grid[var] + ' Wins', True
  elif count == 9:
    return 'Tie', True
  else:
    return '', False

def game():
  global grid, count
  grid = [''] * 9
  count = 0

  def draw_x(x_coord, y_coord):
    canvas.create_line(x_coord-65, y_coord-65, x_coord+65, y_coord+65, fill='white', width = 5)
    canvas.create_line(x_coord-65, y_coord+65, x_coord+65, y_coord-65, fill='white', width = 5)

  def draw_o(x_coord, y_coord):
    canvas.create_oval(x_coord-65, y_coord-65, x_coord+65, y_coord+65, fill='white')
    canvas.create_oval(x_coord-60, y_coord-60, x_coord+60, y_coord+60, fill='black')

  def mouse_click_coord(eventorigin):
    global x,y,count
    x = eventorigin.x
    y = eventorigin.y
    center_x, center_y = handle_click()
    
    if check_slot(center_x, center_y) == 'bad':
      return
    
    if count % 2 == 0:
      draw_x(center_x, center_y)
    else:
      draw_o(center_x, center_y)
    count += 1

    msg, over = game_over()
    if over == True:
      messagebox.showinfo("Game", msg)
      root.destroy()

  root = tk.Tk()
  root.geometry('500x500')

  # draw board
  canvas = tk.Canvas(root, width=500, height=500)
  canvas.configure(bg='black')
  canvas.create_rectangle(x1, 0, x2, 500, fill="white")
  canvas.create_rectangle(x3, 0, x4, 500, fill="white")
  canvas.create_rectangle(0, x1, 500, x2, fill="white")
  canvas.create_rectangle(0, x3, 500, x4, fill="white")

  canvas.pack()

  root.bind("<Button 1>",mouse_click_coord)

  root.mainloop()

base = tk.Tk()
base.geometry('400x400')
b1 = tk.Button(base, text='New Game', command=game, width=45, height=12)
b2 = tk.Button(base, text='Quit', command=base.destroy, width=45, height=12)
b1.pack(side=tk.TOP)
b2.pack(side=tk.BOTTOM)
base.mainloop()