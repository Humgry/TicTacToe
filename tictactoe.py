import tkinter as tk
from tkinter import messagebox
import re

x, y = 0, 0
high = 400
x1 = round((high - (round(high*0.02))) / 3)
x2 = x1 + (round(high*0.01))
x3 = x2 + x1
x4 = x3 + (round(high*0.01))
bkg_color = '#000000'
frg_color = '#ffffff'

x_tuple = (x1,x2,x3,x4)

# (center_x, center_y):slot in grid
grid_dict = {(x1/2,x1/2):0,
             ((x3+x2)/2,x1/2):1,
             ((high+x4)/2,x1/2):2,
             (x1/2,(x3+x2)/2):3,
             ((x3+x2)/2,(x3+x2)/2):4,
             ((high+x4)/2,(x3+x2)/2):5,
             (x1/2,(high+x4)/2):6,
             ((x3+x2)/2,(high+x4)/2):7,
             ((high+x4)/2,(high+x4)/2):8}

# set and refresh allow for resize of window in options button menu
def setvars():
  root = tk.Tk()
  text_w = 34
  # window size
  l1 = tk.Label(root, text='Window Height (window is square):')
  e1 = tk.Entry(root, width=text_w)
  e1.insert(tk.END, str(high))
  l1.pack()
  e1.pack()
  
  # bkg, frg color
  l2 = tk.Label(root, text='Background color (Hexadecimal Value):')
  e2 = tk.Entry(root, width=text_w)
  e2.insert(tk.END, bkg_color)
  l2.pack()
  e2.pack()
  
  l3 = tk.Label(root, text='Foreground color (Hexadecimal Value):')
  e3 = tk.Entry(root, width=text_w)
  e3.insert(tk.END, frg_color)
  l3.pack()
  e3.pack()

  b1 = tk.Button(root, text='Save', command=lambda:refreshvars(e1.get(), e2.get(), e3.get(), root))
  b1.pack()

def refreshvars(w_size, bkgColor, frgColor, root):
  try:
    w_size = int(w_size)
  except:
    w_size = 400
  # size less than 200 breaks the board
  if w_size < 200:
    w_size = 200
  # doesn't break but too big is annoying
  elif w_size > 1000:
    w_size = 1000
  
  # check that bkg color is hexadecimal
  match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', bkgColor)

  if match:
    pass
  else:
    bkgColor = '#000000'
    
  match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', frgColor)

  if match:
    pass
  else:
    frgColor = '#ffffff'
  
  # edit all variables from function, want to do a different way, not sure how
  global high,x_tuple,grid_dict
  high = w_size
  x1 = round((high - (round(high*0.02))) / 3)
  x2 = x1 + (round(high*0.01))
  x3 = x2 + x1
  x4 = x3 + (round(high*0.01))
  
  global bkg_color, frg_color
  bkg_color = bkgColor
  frg_color = frgColor
    
  # using tuple saves me from calling 85 items in global func
  x_tuple = (x1,x2,x3,x4)

  grid_dict = {(x1/2,x1/2):0,
               ((x3+x2)/2,x1/2):1,
               ((high+x4)/2,x1/2):2,
               (x1/2,(x3+x2)/2):3,
               ((x3+x2)/2,(x3+x2)/2):4,
               ((high+x4)/2,(x3+x2)/2):5,
               (x1/2,(high+x4)/2):6,
               ((x3+x2)/2,(high+x4)/2):7,
               ((high+x4)/2,(high+x4)/2):8}
  
  # Hitting save closes settings window
  root.destroy()

# makes sure slot clicked unfilled before placing X or O
# Keeps track of whose play it is
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

# return coords of center of square clicked
def handle_click():
  x_c = 0
  y_c = 0
  
  x1,x2,x3,x4 = x_tuple
  
  if 0 < x and x < x1:
    x_c = x1/2
  elif x2 < x and x < x3:
    x_c = (x3+x2)/2
  elif x4 < x and x < high:
    x_c = (high+x4)/2

  if 0 < y and y < x2:
    y_c = x1/2
  elif x2 < y and y < x3:
    y_c = (x3+x2)/2
  elif x4 < y and y < high:
    y_c = (high+x4)/2
  
  return x_c, y_c

# checks 8 possible endings
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

# bulk of game
def game():
  global grid, count
  grid = [''] * 9
  count = 0

  x1,x2,x3,x4 = x_tuple

  def draw_x(x_coord, y_coord):
    canvas.create_line(x_coord-((x1/2)-10), y_coord-((x1/2)-10), x_coord+((x1/2)-10), y_coord+((x1/2)-10), fill=frg_color, width = 5)
    canvas.create_line(x_coord-((x1/2)-10), y_coord+((x1/2)-10), x_coord+((x1/2)-10), y_coord-((x1/2)-10), fill=frg_color, width = 5)

  def draw_o(x_coord, y_coord):
    canvas.create_oval(x_coord-((x1/2)-10), y_coord-((x1/2)-10), x_coord+((x1/2)-10), y_coord+((x1/2)-10), fill=frg_color)
    canvas.create_oval(x_coord-(((x1/2)-10)-5), y_coord-(((x1/2)-10)-5), x_coord+(((x1/2)-10)-5), y_coord+(((x1/2)-10)-5), fill=bkg_color)

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
  geo = str(high) + 'x' + str(high)
  root.geometry(geo)

  # draw board
  canvas = tk.Canvas(root, width=high, height=high)
  canvas.configure(bg=bkg_color)
  canvas.create_rectangle(x1, 0, x2, high, fill=frg_color)
  canvas.create_rectangle(x3, 0, x4, high, fill=frg_color)
  canvas.create_rectangle(0, x1, high, x2, fill=frg_color)
  canvas.create_rectangle(0, x3, high, x4, fill=frg_color)

  canvas.pack()

  root.bind("<Button 1>",mouse_click_coord)

  root.mainloop()

base = tk.Tk()
base.geometry('400x400')
b1 = tk.Button(base, text='New Game', command=game, width=15, height=5)
b2 = tk.Button(base, text='Options', command=setvars, width=15, height=5)
b3 = tk.Button(base, text='Quit', command=base.destroy, width=15, height=5)
b1.pack()
b2.pack()
b3.pack()
base.mainloop()
