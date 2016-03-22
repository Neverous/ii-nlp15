import sys

if __name__ == '__main__':
  if len(sys.argv) != 3:
     print 'Usage: %s <file1> <file2>' % (sys.argv[0],)
     print 'Both files should have equal number of lines'
     sys.exit(1)
  
  A = open(sys.argv[1]).readlines()
  B = open(sys.argv[2]).readlines()
  
  errors = 0.0
  cnt = 0.0
  
  for a,b in zip(A,B):
    aList = a.split()
    bList = b.split()
    abList = zip(aList, bList)
    
    for x,y in abList:
      cnt += 1
      if x != y:
        errors += 1
    
    if len(abList) < max(len(aList),len(bList)):
      rest = max(len(aList),len(bList)) - len(abList)
      errors += rest
      cnt += rest
      
  print 'Accuracy:', (cnt-errors) / cnt * 100,'%'
  print 'Errors:', errors      
