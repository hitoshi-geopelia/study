import curses

def main(stdscr):
  barea = BattleArea()
  barea.init(stdscr)
  win0.clear()
  # test
  s = []
  s.append(Piece(0,  1, 1, 1, 3))
  s.append(Piece(1,  5, 2, 2, 1))
  s.append(Piece(2,  7, 3, 2, 1))
  s.append(Piece(3, 10, 4, 2, 1))
  # draw background
  barea.draw()
  # draw individual ships
  for s1 in s:
    s1.draw()
  # (test)draw caret
  caret.draw()
  # draw logs
  barea.info('URGENT MESSAGE.')
  stdscr.refresh()
  print('\007')
  stdscr.getch()

class BattleArea:
  map = []
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
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)
    BattleArea.max_height, BattleArea.max_width = win0.getmaxyx()
    BattleArea.max_y = (BattleArea.max_height - 1) // 2
    x = (BattleArea.max_width - 1) // 3
    BattleArea.max_x = x - (x % 2) - 1 - 6
    map = [[0] * BattleArea.max_x for i in range(BattleArea.max_y) for j in range(2)]
    global caret
    caret = Caret()

  def draw(self):
    global win0
    for x in range(0, BattleArea.max_x):
      if (26 <= x) or (x % 2 == 0):
        win0.addstr(0, x * 3 + 3, int2abc(x))
      else:
        win0.addstr(0, x * 3 + 3, (int2abc(x) + '_')[:2])
      b0 = ['\__/  '] * 100
    b1 = ''.join(b0)
    for y in range(0, BattleArea.max_y):
      win0.addstr((y * 2) + 1, 2, b1[0:(BattleArea.max_x) * 3 + 1])
      win0.addstr((y * 2) + 1, 0, ('  ' + str(y + 1))[-2:])
      win0.addstr((y * 2) + 2, 2, b1[3:(BattleArea.max_x) * 3 + 4])

  def info(self, msg):
    global win0
    l = len(msg)
    win0.addstr(0, BattleArea.max_x * 3 + 4, msg, curses.color_pair(0))

class Piece:
  def __init__(self, id, y, x, speed, range):
    self.id = id
    self.y = y
    self.x = x
    self.speed = speed
    self.range = range

  def draw(self):
    win0.addstr(self.y * 2 + (self.x % 2), self.x * 3 + 3, 'S' + str(self.id), curses.color_pair(4))

class Caret:
  y, x = 1, 1

  def draw(self):
    win0.addstr(self.y * 2 - 1 + (self.x % 2), self.x * 3 + 3, '__', curses.color_pair(2))
    win0.addstr(self.y * 2 + (self.x % 2), self.x * 3 + 2, '/', curses.color_pair(2))
    win0.addstr(self.y * 2 + (self.x % 2), self.x * 3 + 5, '\\', curses.color_pair(2))
    win0.addstr(self.y * 2 + 1 + (self.x % 2), self.x * 3 + 2, '\__/', curses.color_pair(2))

def int2abc(in1):
  BASE = 26
  blist = [BASE]
  l = len(blist) - 1
  while blist[l] <= in1:
    l = len(blist)
    blist.append(BASE ** (l + 1) + blist[l - 1])
  abc = ''
  for col in range(len(blist) - 1, -1, -1):
    if 1 < col:
      a = (in1 - blist[col - 2]) // (BASE ** col)
    else:
      a = in1 // (BASE ** col)
    if 0 < col:
      abc += ('' + chr(a + 64))
    else:
      abc += ('' + chr(a + 65))
    in1 -= a * (BASE ** col)
  return abc

if __name__ == '__main__':
  curses.wrapper(main)
