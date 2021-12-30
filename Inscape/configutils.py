from Inscape import *

def getProperties(section,key):
    try:
        options = configParser.get(section,key)
        return options
    except: 
        print("unknown section:",section,key)
        
 



