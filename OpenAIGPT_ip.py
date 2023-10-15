import random
import requests
import json
from retrying import retry

requests.packages.urllib3.disable_warnings() #negalect the warnings

class OpenAIGPT:
    def __init__(self, model_name="gpt-3.5-turbo", keys_path=None):
        self.model_name = model_name
        with open(keys_path, encoding="utf-8", mode="r") as fr:
            self.keys = [line.strip() for line in fr if len(line.strip()) >= 4]
        
    def __post_process(self, response):
        try:
            content = response["choices"][0]["message"]["content"]
            flag = True
        except:
            content = response["error"]["code"]
            flag = False
        return flag, content
    
    
    @retry(wait_fixed=200, stop_max_attempt_number=10)
    def __call__(self, message):
        if message is None or message == "":
            return False, "Your input is empty."
        
        current_key = random.choice(self.keys)
        
        random_integer = random.randint(1, 1000)
        proxies = {
            "http": "127.0.0.1:"+str(24000+random_integer),
            "https": "127.0.0.1:"+str(24000+random_integer)
        }
        
        raw_response = requests.post(
            url= "https://api.openai.com/v1/chat/completions", # if use VPN set to 'https://api.openai.com/v1/chat/completions'
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {current_key}",
                # "OpenAI-Organization": ""   # if use GPT-4
            },
            json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": message}],  # Do prompt engineering here
                "temperature": 0.6,
                "top_p": 0.8,
                "frequency_penalty": 0.6,
                "presence_penalty": 0.8,
                "n": 1
            },
            # proxies=proxies  # Use the selected proxy for this request
        )
        
        response = json.loads(raw_response.content.decode("utf-8"))
        return self.__post_process(response)
    

if __name__ == '__main__':
    # test code
    igpt=OpenAIGPT(keys_path="gpt3keys.txt")
    flag, answer=igpt("怎么了")
    print(answer)