import subprocess
import os


subprocess.check_output("gcloud projects list > ./artifacts/temp.txt", shell=True)

with open('./artifacts/temp.txt','r') as file:
    flag = 0
    for line in file:      
        word = line.split()  
        if str(word[0]) != "PROJECT_ID":
            print(word[0])

os.remove("./artifacts/temp.txt")

