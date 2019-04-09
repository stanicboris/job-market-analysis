
import sys
from datetime import datetime  
args = sys.argv

myFile = open('/home/zanea/Projets/job-market-analysis/append.txt', 'a')  
myFile.write('\nAccessed on ' + str(datetime.now()) + 'with args = ' + str(args[1])) 