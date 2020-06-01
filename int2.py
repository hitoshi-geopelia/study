import sys
args = sys.argv

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

# print(int2(int(args[1])))
for i in range(0, 272, 16):
  print(int2(i), int2(i + 1), int2(i + 2), int2(i + 3),
        int2(i + 4), int2(i + 5), int2(i + 6), int2(i + 7),
        int2(i + 8), int2(i + 9), int2(i + 10), int2(i + 11),
        int2(i + 12), int2(i + 13), int2(i + 14), int2(i + 15))
