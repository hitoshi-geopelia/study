import curses
import random
from collections import deque

def loop(stdscr, *args, **kwds) :
  barea = BattleArea()
  barea.init(stdscr)
  win0.clear()
  #TODO: ランダム配置または任意の配置を選択できるようにする
  ryx = barea.randcoordinate(4)
  s = [
    Piece(0, ryx[0], ryx[1], 1, 3),
    Piece(1, ryx[2], ryx[3], 2, 1),
    Piece(2, ryx[4], ryx[5], 2, 1),
    Piece(3, ryx[6], ryx[7], 2, 1)]
  global caret
  caret = Caret(s[0].y, s[0].x)
  global operand
  operand = -1
  while True:
    # draw background
    barea.draw()
    # draw individual ships
    for s1 in s:
      s1.draw()
    # (test)draw caret
    caret.draw()
    # (test)draw logs
    barea.info("P)os " +
      int2abc(caret.x) + str(caret.y) + " (" + str(caret.y) + ", " + str(caret.x) + ")"
      " <" + str(operand) + ">")
    barea.prompt("Order or '?'(Guide)")
    stdscr.refresh()
    #print("\007")
    ch = stdscr.getch()
    if ch != -1 :
      if ch == curses.KEY_UP:
        if (caret.x + 1) % 2 < caret.y:
          caret.y -= 1
      elif ch == curses.KEY_DOWN:
        if caret.y < barea.max_y - 1:
          caret.y += 1
      elif ch == curses.KEY_LEFT:
        if 0 < caret.y and 0 < caret.x:
          caret.x -= 1
      elif ch == curses.KEY_RIGHT:
        if 0 < caret.y and caret.x < barea.max_x - 1:
          caret.x += 1
      elif "0" <= chr(ch) and chr(ch) <= "3":
        i = ch - ord("0")
        operand, caret.y, caret.x = s[i].id, s[i].y, s[i].x
      elif chr(ch) == "m":
        caret.y, caret.x = s[3].y, s[3].x
      elif chr(ch) == "?":
        barea.info("_" * 20)
        barea.info("Q)uit")
        barea.info("-) unmark")
        barea.info("+) mark")
        barea.info("    #0 Only")
        barea.info("S)pecial weapon")
        barea.info("N)ormal attack")
        barea.info("M)ove to")
        barea.info(" specify a unit")
        barea.info("0, 1, 2, or 3)")
        barea.info("_" * 20)
      elif chr(ch) == "q":
        break
      else :
        pass

class BattleArea:
  map = []
  log = deque()
  LOG_WIDTH = 1 + 6 # 1 : 列数を奇数にする, 6 : ログ表示桁数を更に18桁増やす
  max_height = 25
  max_width = 80
  max_y = (max_height - 1) // 2
  max_x = ((max_width - 1) // 3) - (((max_width - 1) // 3) % 2) - 1 - 6

  def init(self, stdscr):
    global win0
    win0 = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_CYAN)
    BattleArea.max_height, BattleArea.max_width = win0.getmaxyx()
    BattleArea.max_y = (BattleArea.max_height - 1) // 2
    x = (BattleArea.max_width - 1) // 3
    BattleArea.max_x = x - (x % 2) - 1 - 6
    map = [[0] * BattleArea.max_x for i in range(BattleArea.max_y) for j in range(2)]

  def draw(self):
    global win0
    for x in range(0, BattleArea.max_x):
      if (26 <= x) or (x % 2 == 0):
        win0.addstr(0, x * 3 + 3, int2abc(x))
      else:
        win0.addstr(0, x * 3 + 3, (int2abc(x) + "_")[:2])
      b0 = ["\__/  "] * 100
    b1 = "".join(b0)
    win0.addstr(1, 0, " 0")
    for y in range(0, BattleArea.max_y):
      win0.addstr((y * 2) + 1, 2, b1[0:(BattleArea.max_x) * 3 + 1])
      if y < BattleArea.max_y - 1:
        win0.addstr((y * 2) + 2, 0, ("  " + str(y + 1))[-2:])
      win0.addstr((y * 2) + 2, 2, b1[3:(BattleArea.max_x) * 3 + 4])

  def info(self, msg):
    ''' ログを1行目以降に表示する '''
    global win0
    m = (msg + (" " * 20))[:(BattleArea.LOG_WIDTH * 3 - 1)]
    BattleArea.log.append(m)
    if (BattleArea.max_y + 1)* 2 < len(BattleArea.log):
      BattleArea.log.popleft()
    l = len(BattleArea.log) - 1
    for iy in range(1, l):
      win0.addstr(iy, BattleArea.max_x * 3 + 4, BattleArea.log[l - iy], curses.color_pair(0))

  def prompt(self, msg):
    ''' プロンプトを0行目に表示する '''
    global win0
    m = (msg + (" " * 20))[:(BattleArea.LOG_WIDTH * 3 - 1)]
    win0.addstr(0, BattleArea.max_x * 3 + 4, m, curses.color_pair(2))

  def randcoordinate(self, n):
    ''' 指定数のユニットが重ならないように座標を乱数で決める '''
    yx = []
    for i in range(0, n * 2, 2):
      y, x = 0, 0
      while y == 0 and x % 2 == 0:
        y = random.randint(0, BattleArea.max_y - 1)
        x = random.randint(0, BattleArea.max_x - 1)
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
    win0.addstr(self.y * 2 + (self.x % 2), self.x * 3 + 3, "S" + str(self.id), curses.color_pair(4))

class Caret:
  y, x = 1, 1
  def __init__(self, y, x):
    Caret.y, Caret.x = y, x

  def draw(self):
    # win0.addstr(self.y * 2 - 1 + (self.x % 2), self.x * 3 + 3, "__", curses.color_pair(7))
    win0.addstr(self.y * 2 + (self.x % 2), self.x * 3 + 2, "/", curses.color_pair(7))
    win0.addstr(self.y * 2 + (self.x % 2), self.x * 3 + 5, "\\", curses.color_pair(7))
    win0.addstr(self.y * 2 + 1 + (self.x % 2), self.x * 3 + 2, "\__/", curses.color_pair(7))

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

if __name__ == '__main__':
  curses.wrapper(loop)
