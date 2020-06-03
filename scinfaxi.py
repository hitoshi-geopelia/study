import curses

def main(stdscr):
  barea = BattleArea()
  barea.init(stdscr)
  win0.clear()
  barea.drawGround()
  barea.info('URGENT MESSAGE.')
  stdscr.refresh()
  stdscr.getch()

class BattleArea:
  max_height = 25
  max_width = 80
  max_y = (max_height - 1) // 2
  max_x = ((max_width - 1) // 3) - (((max_width - 1) // 3) % 2) - 1

  def init(self, stdscr):
    global win0
    win0 = curses.initscr()
    self.max_height, self.max_width = win0.getmaxyx()
    self.max_y = (self.max_height - 1) // 2
    x = (self.max_width - 1) // 3
    self.max_x = x - (x % 2) - 1

  def drawGround(self):
    global win0
    for x in range(0, self.max_x):
      if (x < 26) and (x % 2 == 1):
        win0.addstr(0, x * 3 + 3, (int2abc(x) + '_')[:2])
      else:
        win0.addstr(0, x * 3 + 3, int2abc(x))
      b0 = ['\__/  '] * 100
    b1 = ''.join(b0)
    for y in range(0, self.max_y):
      win0.addstr((y * 2) + 1, 2, b1[0:(self.max_x) * 3 + 1])
      win0.addstr((y * 2) + 1, 0, ('  ' + str(y + 1))[-2:])
      win0.addstr((y * 2) + 2, 2, b1[3:(self.max_x) * 3 + 4])
      # if y < self.max_y - 1:
      #   win0.addstr((y * 2) + 2, 0, ('  ' + str(y + 1))[-2:])

  def info(self, msg):
    global win0
    l = len(msg)
    win0.addstr(self.max_height - 1, 0, msg)

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
      # print('  {} {} {}'.format(in1, BASE ** col, blist))
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
