import curses
import random
from collections import deque
from multiprocessing import Process
import time

def loop(stdscr, *args, **kwds):
  global barea
  barea = BattleArea()
  barea.init(stdscr)
  global win0
  win0.clear()
  #TODO: ランダム配置または任意の配置を選択できるようにする
  ryx = barea.randcoordinate(4)
  s = [
    Piece(0, ryx[0], ryx[1], 1, 3),
    Piece(1, ryx[2], ryx[3], 2, 1),
    Piece(2, ryx[4], ryx[5], 2, 1),
    Piece(3, ryx[6], ryx[7], 2, 1)]
  # draw background
  barea.draw()
  # draw individual ships
  for s1 in s:
    s1.draw()
  global caret
  caret = Caret(ryx[0], ryx[1])
  caret.start()
  global operand
  operand = -1
  chex = chr(0)
  while True:
    # draw background
    barea.draw()
    # draw individual ships
    for s1 in s:
      s1.draw()
    # get keyboard input
    ch = getcho() if kbhit() else 0
    if ch != 0:
      if ch == ord('q') or ch == 3: # ETX テキスト終了
        break
      elif ch == ord('?'):
        barea.info("_" * 20)
        barea.info("Q)uit")
        barea.info("-) unmark")
        barea.info("+) mark")
        barea.info(" #0 Only")
        barea.info("S)pecial weapon")
        barea.info("N)ormal attack")
        barea.info("M)ove to")
        barea.info(" specify a unit")
        barea.info("0, 1, 2, or 3)")
        barea.info("_" * 20)
      elif ord('0') <= ch and ch <= ord('3'):
        i = ch - ord('0')
        operand, Caret.y, Caret.x = s[i].id, s[i].y, s[i].x
      elif ch == ord('m'):
        Caret.y, Caret.x = s[3].y, s[3].x
      elif ch == 27: # ESC エスケープ
        ch = getcho()
        if ch == ord('['):
          ch = getcho()
        else:
          continue

      if ch == ord('A') and ((Caret.x + 1) % 2 < Caret.y): # KEY_UP:
        Caret.y -= 1
      elif ch == ord('B') and (Caret.y < barea.max_y - 1): # KEY_DOWN:
        Caret.y += 1
      elif ch == ord('C') and (0 < Caret.y and Caret.x < barea.max_x - 1): # KEY_RIGHT:
        Caret.x += 1
      elif ch == ord('D') and (0 < Caret.y and 0 < Caret.x): # KEY_LEFT:
        Caret.x -= 1
    # print log messages
    if chex != ch:
      if 0 != ch:
        barea.info("P)os[" + str(operand) + "]" +
          "(" + str(Caret.y) + "," + str(Caret.x) + ")" +
          ":" + str(chex) + ":" + str(ch) + ":")
        barea.prompt("[{}{}]Order or '?'".format(int2abc(Caret.x), str(Caret.y)))
        #print("\007")
        win0.refresh()
      chex = ch 

class BattleArea:
  LOG_WIDTH = 7 # ログ表示桁数を(7 * 3 - 1)桁にする
  LOG_WIDTH = LOG_WIDTH + (LOG_WIDTH % 2) 

  def init(self, stdscr):
    global win0
    win0 = curses.initscr()
    curses.start_color()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED,     curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN,   curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW,  curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE,    curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN,    curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK,   curses.COLOR_CYAN)
    BattleArea.max_height, BattleArea.max_width = win0.getmaxyx()
    BattleArea.max_y = (BattleArea.max_height - 1) // 2
    x = (BattleArea.max_width - 1) // 3
    BattleArea.max_x = x - (x % 2 - 1) - BattleArea.LOG_WIDTH
    BattleArea.map = [[0] * BattleArea.max_x for i in range(BattleArea.max_y) for j in range(2)]
    BattleArea.log = deque([], (BattleArea.max_y + 1) * 2)

  def draw(self):
    global win0
    for x in range(0, BattleArea.max_x):
      win0.addstr(0, x * 3 + 3, int2abc(x))
      if (x < 26) and (x % 2 != 0):
        win0.addstr(0, x * 3 + 4, '_', curses.color_pair(4))
      b0 = ["\__/  "] * 100
    b1 = "".join(b0)
    win0.addstr(1, 0, " 0")
    for y in range(0, BattleArea.max_y):
      win0.addstr((y * 2) + 1, 2, b1[0:(BattleArea.max_x) * 3 + 1], curses.color_pair(4))
      if y < BattleArea.max_y - 1:
        win0.addstr((y * 2) + 2, 0, ("  " + str(y + 1))[-2:])
      win0.addstr((y * 2) + 2, 2, b1[3:(BattleArea.max_x) * 3 + 4], curses.color_pair(4))

  def info(self, msg):
    ''' ログを1行目以降に表示する '''
    global win0
    m = (msg + (" " * (BattleArea.LOG_WIDTH * 3)))[:((BattleArea.LOG_WIDTH - 1) * 3)]
    BattleArea.log.append(m)
    l = len(BattleArea.log) - 1
    for iy in range(1, l):
      win0.addstr(iy, BattleArea.max_x * 3 + 4, BattleArea.log[l - iy], curses.color_pair(0))

  def prompt(self, msg):
    ''' プロンプトを0行目に表示する '''
    global win0
    m = (msg + (" " * (BattleArea.LOG_WIDTH * 3)))[:((BattleArea.LOG_WIDTH - 1) * 3)]
    win0.addstr(0, BattleArea.max_x * 3 + 4, m, curses.color_pair(3))

  def randcoordinate(self, n):
    ''' 指定数のユニットが重ならないように座標を乱数で決める '''
    yx = []
    for i in range(0, n):
      y, x = 0, 0
      while y == 0 and x % 2 == 0:
        y = random.randint(0, BattleArea.max_y - 1)
        x = random.randint(0, BattleArea.max_x - 1)
        if 0 < i:
          for j in range(0, i - 1):
            if y == yx[j * 2] and x == yx[j * 2 + 1]:
              y, x = 0, 2
              break
      yx.append(y)
      yx.append(x)
    return yx

class Piece:
  def __init__(self, id, y, x, speed, range):
    self.id = id
    self.y = y
    self.x = x
    self.speed = speed
    self.range = range

  def draw(self):
    global win0
    win0.addstr(self.y * 2 + (self.x % 2), self.x * 3 + 3, "S" + str(self.id), curses.color_pair(2))

class Caret(Process):
  x = 0
  y = 0
  def __init__(self, y, x):
    Process.__init__(self)
    self.daemon = True
    Caret.y, Caret.x = y, x

  def run(self):
    global win0
    global barea
    caret_color = [curses.color_pair(3), curses.color_pair(4), curses.color_pair(6)]
    cc = 0
    while True:
      win0.addstr(Caret.y * 2 + 1 + (Caret.x % 2), Caret.x * 3 + 3, "__", caret_color[(2 + cc) % 3])
      win0.addstr(Caret.y * 2 + 1 + (Caret.x % 2), Caret.x * 3 + 2, "\\", caret_color[(1 + cc) % 3])
      win0.addstr(Caret.y * 2 + (Caret.x % 2), Caret.x * 3 + 2, "/", caret_color[cc % 3])
      if 0 < Caret.y:
        win0.addstr(Caret.y * 2 - 1 + (Caret.x % 2), Caret.x * 3 + 3, "__", caret_color[(2 + cc) % 3])
      elif (0 < Caret.y) or (0 == Caret.y and Caret.x < 26):
        win0.addstr(Caret.y * 2 - 1 + (Caret.x % 2), Caret.x * 3 + 4, "_", caret_color[(2 + cc) % 3])
      win0.addstr(Caret.y * 2 + (Caret.x % 2), Caret.x * 3 + 5, "\\", caret_color[(1 + cc) % 3])
      win0.addstr(Caret.y * 2 + 1 + (Caret.x % 2), Caret.x * 3 + 5, "/", caret_color[cc % 3])
      cc = cc + 1 if cc < 2 else 0
      barea.prompt("[{}{}]Order or '?'".format(int2abc(Caret.x), str(Caret.y)))
      win0.refresh()
      time.sleep(0.33)

def int2abc(in1):
  BASE = 26
  blist = [BASE]
  l = len(blist) - 1
  while blist[l] <= in1:
    l = len(blist)
    blist.append(BASE ** (l + 1) + blist[l - 1])
  abc = ""
  for col in range(len(blist) - 1, -1, -1):
    if 1 < col:
      a = (in1 - blist[col - 2]) // (BASE ** col)
    else:
      a = in1 // (BASE ** col)
    if 0 < col:
      abc += ("" + chr(a + 64))
    else:
      abc += ("" + chr(a + 65))
    in1 -= a * (BASE ** col)
  return abc

def getcho():
  cho = ord(getch())
  return cho

# kbhit http://code.activestate.com/recipes/572182-how-to-implement-kbhit-on-linux
import sys, termios, atexit
from select import select

# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

# switch to normal terminal
def set_normal_term():
  termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

# switch to unbuffered terminal
def set_curses_term():
  termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def putch(ch):
  sys.stdout.write(ch)

def getch():
  return sys.stdin.read(1)

def getche():
  ch = getch()
  putch(ch)
  return ch

def kbhit():
  dr,dw,de = select([sys.stdin], [], [], 0)
  return dr != []

if __name__ == '__main__':
  atexit.register(set_normal_term)
  set_curses_term()
  curses.wrapper(loop)
