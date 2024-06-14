import time,random,os,sys
from openai import OpenAI
#add you key here
API_KEY='API KEY'
client = OpenAI(api_key=API_KEY)
#model to check
MODELS=["gpt-3.5-turbo",
       "gpt-3.5-turbo-0613",
       "gpt-3.5-turbo-16k-0613",
       "gpt-3.5-turbo-1106",
       "gpt-4o"]

def get_resp_4o(prompt,model_name):
    client = OpenAI(
	api_key=API_KEY,
    )
    chat_completion = client.chat.completions.create(
    messages=[
		{
			"role": "user", "content": f"{prompt}", "temperature": 0.5, "top_p": 0.5, "max_tokens": 256
		}
    ],
    model="gpt-4o",
    )

    return chat_completion.choices[0].message.content


#get resonse from ollama models/chatgpt
def get_resp(mes,model_name):
    if model_name=="gpt-4o":
        return get_resp_4o(mes,"gpt-4o")
    #get the response from chatgpt
    messages_chatgpt = [ {"role": "system", "content": 
			"You are a intelligent assistant."} ] 
    messages_chatgpt.append( 
    {"role": "user", "content": mes}, 
    ) 
    chat = client.chat.completions.create(model=model_name, messages=messages_chatgpt)
    return chat.choices[0].message.content 

#load the entities
def load_entities(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(line.strip("\n"))
    return data

DATETIME=60624
RESULTS_FILES=[]
os.makedirs("results_"+str(DATETIME), exist_ok=True)#create the folder
for m in MODELS:
    f=open("results_"+str(DATETIME)+"/results_"+m+"-simple.csv","w",buffering=1)
    RESULTS_FILES.append(f)

#tester string
tester_p1="Pretand you are "
tester_p2=". Please generate a dream that this person dreamt last night."
tester_file=open("results_"+str(DATETIME)+"/prompt.csv","w",buffering=1)
tester_file.write(tester_p1+"\n")
tester_file.write(tester_p2+"\n")
tester_file.close()

data=load_entities(sys.argv[1])
random.shuffle(data)
#iterate the data per model
for i in range(len(MODELS)):
    try:
        model=MODELS[i]
        result_file=RESULTS_FILES[i]
        for sample in data:
            test=tester_p1+sample+tester_p2
            for k in range(5):
                reply=get_resp(test,model)
                result_file.write(sample+";"+reply+"\n")
                result_file.write("---end---\n")  
    except Exception as e:
        continue



    

