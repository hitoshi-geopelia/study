import sys
args = sys.argv

def int2abc(in1):
  BASE = 3
  col_max = 0
  b = BASE
  while b <= in1:
    col_max += 1
    b += BASE ** (col_max + 1)
  abc = ''
  for col1 in range(col_max, -1, -1):
    b = 0
    for col2 in range(col1, 0, -1):
      b += BASE ** col2
    if b <= in1:
      a = in1 // (BASE ** col1)
    else:
      a = 0
    abc += chr(a + 65)
    in1 -= a * (BASE ** col1)
    print( "\tcol1={}, {}: {}".format(col1, b, abc) )
#  a = in1
#  abc += chr(a + 65)
  return abc

def int2(in1):
  BASE = 16
  col = 0
  b = BASE
  while b <= in1:
    col += 1
    b *= BASE
  abc = ''
  for col1 in range(col, 0, -1):
    col0 = BASE ** col1
    if col0 <= in1:
      a = in1 // col0
    else:
      a = 0
    if a < 10:
      abc += chr(a + 48)
    else:
      abc += chr(a + 55)
    in1 -= a * col0
  a = in1
  if a < 10:
    abc += chr(a + 48)
  else:
    abc += chr(a + 55)
  return abc

# print(int2abc(int(args[1])))
for i in range(0, 40):
  print(str(i) + ' = ' + int2abc(i))
