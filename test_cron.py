
import sys
from datetime import datetime  
args = sys.argv

def fonction(args):
    myFile = open('append.txt', 'a')  
    myFile.write('\nAccessed on ' + str(datetime.now()) + 'with args = ' + args[1])