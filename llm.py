import os 
import utils
import openai

from typing import List
from requests import post
from json import dumps

gemini_key = os.environ.get("GEMINI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

class Model:
    
    @staticmethod
    def prompt_chat(context:List[str]) ->str:
        # Prompts the gpt-3.5-turbo model. Not recommended for slow networks.
        content = utils.contextify(context)
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role":'system', "content":context[0]},
                    {"role":'user', "content":content},
                    ], 
                temperature=1,
                request_timeout=30
            )
        return response["choices"][0]["message"]['content'].replace("RESPONSE:", "")
    
    @staticmethod
    def prompt_text(context:List[str]) ->str:
        """Prompts the text-davinci-003 model for a response given the recorded text"""
        content = utils.contextify(context, True)
        response = openai.Completion.create(
            model="text-davinci-003", 
            prompt=content, 
            temperature=1,
            request_timeout=40,
            max_tokens=1000
            )
        return response["choices"][0]['text'].replace("RESPONSE:", "")
    
    @staticmethod
    def prompt_gemini(context:List[str]) ->str:
        """Prompts the gemini-ai model for a response given the recorded text"""
        content = utils.contextify(context, True)
        
        response = post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}",
            headers={"Content-Type": "application/json"},
            data=dumps({
                "contents": [
                    {"role": "model", "parts": [{"text": context[0]}]},
                    {"role": "user", "parts": [{"text": content}]}
                ]
            })
        )
        
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    
models = {
    "chat": Model.prompt_chat,
    "text": Model.prompt_text,
    "gemini": Model.prompt_gemini
}