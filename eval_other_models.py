from __future__ import division
import os,sys

files1=os.listdir("Data")
files=["Data"+os.path.sep+x for x in files1 if x.startswith("results")]

for f in files:
    disclaimer=0#counting disclaimers of AI
    
    with open(f,"r", encoding='utf-8') as r:
        con=r.read()
    dreams_info=con.split("---end---")
    size=0
    for dream in dreams_info:
        try:
            
            data=dream.split(";")[1]
            if data.startswith("I'm") or \
                (data.startswith("As an AI") and "\n\n" not in data):
                disclaimer+=1
            size+=1
        except Exception as e:
            continue
    print(f," answered ",str(1-(disclaimer/size))," of the dream requests.") 
