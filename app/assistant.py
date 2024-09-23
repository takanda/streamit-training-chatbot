from qiita_client import QiitaClient


CONVERSATION_LIST = [
    """
    最近気になるITのトレンドは何ですか？""",
    """
    以下の項目で一番気になる項目は何ですか？""",
    """
    最新のトレンドの中で{item}学習におすすめな記事をお探しします。\n
    最後にあなたの要望を自由にお聞かせください！""",
    """
    検索が完了しました。 \n""",
]


def assistant_response(conversation_number, session_state, input):
            
        if conversation_number == 1:
            response = CONVERSATION_LIST[conversation_number]
            response +=  "\n" + session_state.client.related_topic_generator(input)
            return response 
            
        elif conversation_number == 2:
            session_state.client.item_setter(input)
            response = CONVERSATION_LIST[conversation_number].format(
                topic = session_state.client.topic,
                item = session_state.client.item, 
            )
            return response
        
        elif conversation_number == 3:
           client = QiitaClient()
           response = CONVERSATION_LIST[conversation_number] 
           response += "\n" +  session_state.client.recomend_generator(client.get_trending_articles(), input)
           return response
           
        else:
            return None
        