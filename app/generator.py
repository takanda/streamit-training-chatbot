import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")


def response_generator(msg):
    return model.generate_content(msg).text


def response_writer(msg):
    for word in msg.split():
        yield word + " "
        time.sleep(0.05)
        