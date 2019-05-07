###############################
#  Imports for reading keyboard
##############################
import sys, os
import termios, fcntl

# used to slow down our main loop
import time

################################
#  Initialize keyboard reading. 
#  Save the old terminal configuration, and
#  tweak the terminal so that it doesn't echo, and doesn't block.
################################
fd = sys.stdin.fileno()
newattr = termios.tcgetattr(fd)

oldterm = termios.tcgetattr(fd)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)

newattr[3] = newattr[3] & ~termios.ICANON
newattr[3] = newattr[3] & ~termios.ECHO

fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

termios.tcsetattr(fd, termios.TCSANOW, newattr)

##################################
# Non-blocking character read function.
#################################
def getch_noblock():
  try:
    return sys.stdin.read()
  except (IOError, TypeError) as e:
    return None

###################################
# Graphics imports, constants and structures
###################################
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw

# our led matrix is 64x64.
matrix_size = 64

# the "draw size" for our ball in pixels 
sprite_size = 5

options = RGBMatrixOptions()
options.rows = matrix_size 
options.cols = matrix_size 
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

###################################################
# show_player
#    passed parameter determines whether to draw or erase the sprite.
################################################## 
def show_player(show):
  if show:
    player_color = (0,255,0)
  else:
    player_color = (0,0,0)

  temp_image = Image.new("RGB", (sprite_size, sprite_size))
  temp_draw = ImageDraw.Draw(temp_image)

  # Start with a player being a circle.
  temp_draw.ellipse((0,0,sprite_size-1,sprite_size-1), outline=player_color, fill=player_color)
  
  matrix.SetImage(temp_image, player_x, player_y)

###################################
# Main loop 
###################################

# player starts in the middle of the screen
player_x = matrix_size / 2 
player_y = matrix_size / 2
show_player(True)

# player starts without motion
current_dir = "stop"

print "controls:  i=up, j=left, k=down, l=right, s=stop, q=quit"
while True:
  key = getch_noblock()

  if key == 'q':
     break    
  if key == 'i':
    current_dir = "up" 
  if key == 'k':
    current_dir = "down" 
  if key == 'j':
    current_dir = "left" 
  if key == 'l':
    current_dir = "right" 
  if key == 's':
    current_dir = "stop"

  if current_dir == "up":
     # only move the player if there is room to go up.
     if player_y > 0:
        show_player(False)
        player_y = player_y - 1
        show_player(True)

  if current_dir == "left":
     # only move the player if there is room to go left.
     if player_x > 0:
        show_player(False)
        player_x = player_x - 1
        show_player(True)

  if current_dir == "down":
     # only move the player if there is room to go down.
     if player_y < matrix_size - sprite_size: 
        show_player(False)
        player_y = player_y + 1
        show_player(True)

  if current_dir == "right":
     # only move the player if there is room to go right.
     if player_x < matrix_size - sprite_size:
        show_player(False)
        player_x = player_x + 1
        show_player(True)

  time.sleep(.05)


###################################
# Reset the terminal on exit
###################################
termios.tcsetattr(fd, termios.TCSANOW, oldterm)

fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
