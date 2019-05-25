import os
import sys

done = 0

def do():
    done = 1
    print("[useAlias] Started")
    location = os.getcwd()
    print("[useAlias] Do not change the current path of file, if so run useAlias again.")
    name = "bozmitm"
    location = os.path.abspath(location)
        
    #else:
     #   location = input("[useAlias] Enter the path of file that you want to create alias command.")
      #  name = input("[useAlias] File name: ")
       # print("[useAlias] Do not change the current path of file, if so run useAlias again.")
        #location = os.path.abspath(location)

    try:
        os.system("alias "+name + "= \"cd "+location+" && sudo python3 bozmitm.py\"")

    except Exception as e: print(e)   #print whatever the error is

if(done != 1):
    do()
