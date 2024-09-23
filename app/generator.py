import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")


def response_generator(msg):
    for line in msg.splitlines(keepends=True):
        for word in line.split():
            yield word + " "
            time.sleep(0.05)
        yield "\n"

class GeminiClient():
    def __init__(self):
        self.messages = [
            {
                "role": "model",
                "parts": [
                    "You are an AI assistant that helps people find information"
                ]
            },
            {
                "role": "user",
                "parts": [""]
            }
        ]

        self.generation_config = genai.types.GenerationConfig(
                                    candidate_count=1,
                                    max_output_tokens=1000,
                                    temperature=0.7
                                )
        self.topic = ""
        self.item = ""
       
        
    def create_messages(self, prompt):
        messages = self.messages
        messages[1]["parts"][0] = prompt
        
        return messages
    
    
    def related_topic_generator(self, topic):
        prompt = f"""
        以下の制約条件のもとにユーザーのインプットに関連するITのトピックを挙げてください。
        
        ## 制約条件
        トピックは5つ挙げること
        結果フォーマットに従うこと
        
        ## 結果フォーマット(下記のみ出力してください)
        1. "1つ目のトピック名"
        2. "2つ目のトピック名"
        3. "3つ目のトピック名"
        4. "4つ目のトピック名"
        5. "5つ目のトピック名"
        
        ## ユーザーのインプット
        {topic}
        """
        
        self.topic = topic
        
        response = model.generate_content(
                            self.create_messages(prompt),
                            generation_config=self.generation_config
                        )
        return response.text
        
    
    def item_setter(self, item):
        self.item = item
    

    def recomend_generator(self, trending_article, user_request):
        prompt = f"""
        以下の制約条件のもとに最近のトレンド記事の中からおすすめの記事を紹介してください。
        
        ## 制約条件
        ユーザーが気になるトピックに関連していること
        関連している記事がない場合はそう出力すること
        ユーザーの要望を考慮すること
        紹介文は200文字以内であること
        文頭におすすめの理由を短く書くこと
        段落ごとに改行を入れること
        URLは必ず出力すること
        
        ## 最近のトレンド記事(JSON形式です)
        {trending_article}
        
        ## ユーザーが気になるトピック
        {self.item}
        
        ## ユーザーの要望
        {user_request}
        """
        
        response = model.generate_content(
                            self.create_messages(prompt),
                            generation_config=self.generation_config
                        )
        return response.text
        