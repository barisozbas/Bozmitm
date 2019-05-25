import os
import sys

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
        command =  "alias "+name + "='cd "+location+" && sudo python3 bozmitm.py'"
        com = "echo "+ "\""+ command + "\""+ ">> ~/.bash_aliases"
        print(com)
        #subprocess.run(["echo "],[command])
        #print("done1")
        os.system(com)
        print(command)

    except Exception as e: print(e)   #print whatever the error is


