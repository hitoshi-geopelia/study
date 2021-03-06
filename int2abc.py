import sys
args = sys.argv

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

# print(int2abc(int(args[ 1 ])))
for i in range(0, 800, 13):
  print('{}'.format(('    ' + int2abc(i))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 1))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 2))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 3))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 4))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 5))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 6))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 7))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 8))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 9))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 10))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 11))[-4:]) +
        '{}'.format(('    ' + int2abc(i + 12))[-4:]))
