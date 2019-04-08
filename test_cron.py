
import sys
from datetime import datetime  
args = sys.argv

myFile = open('append.txt', 'a')  
myFile.write('\nAccessed on ' + str(datetime.now()) + 'with args = ' + str(args[1])) 