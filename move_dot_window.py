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
from graphics import *

window_size = 500 

# the "draw size" for our ball in pixels 
player_radius = 5

###################################
# Main loop 
###################################
player_color = color_rgb(0,255,255)
win = GraphWin("dot motion", window_size, window_size)
win.setBackground('black')

# player starts in the middle of the screen
player_x = window_size / 2 
player_y = window_size / 2

player = Circle(Point(player_x, player_y), player_radius)
player.setOutline(player_color)
player.setFill(player_color)
player.draw(win)


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
     if player_y > player_radius:
        player_y = player_y - 1
        player.move(0,-1)

  if current_dir == "left":
     # only move the player if there is room to go left.
     if player_x > player_radius:
        player_x = player_x - 1
        player.move(-1,0)

  if current_dir == "down":
     # only move the player if there is room to go down.
     if player_y < window_size - player_radius: 
        player_y = player_y + 1
        player.move(0,1)

  if current_dir == "right":
     # only move the player if there is room to go right.
     if player_x < window_size - player_radius:
        player_x = player_x + 1
        player.move(1,0)

  #time.sleep(.05)

###################################
# Reset the terminal on exit
###################################
win.close()
termios.tcsetattr(fd, termios.TCSANOW, oldterm)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
