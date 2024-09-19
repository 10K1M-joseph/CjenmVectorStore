Users_Search_Function = [
    {
        "type": "function",
        "function": {
            "name": "keyword_search",
            "description": """ 

            # 역할: 사용자의 키워드를 받아서 우리가 정의한 키워드로 분류합니다. ,
            # 역할 설명: 사용자의 입력을 받아서 "character-action", "location", "mood" 등의 키워드로 분류 합니다.

            ### 사용 예시 ###
            # 1번 예시
            질문 =  "형사, 여학생, 사건현장"  
            답변 = "character-action: 형사, 여학생", "location: 사건 현장"


            # 2번 예시
            질문 = "남자, 부모님, 따뜻한, 슬픔"
            답변 = "character-action: 남자, 남자의 부모님", "mood: 따뜻한, 슬픈"

            # 3번 예시
            질문 = "바다, 행복한, 기쁨"
            답변 = "location: 바다", "mood: 행복한, 기쁨"
            
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": """ 사용자의 입력을 받아 키워드로 분류하여 전달합니다. """,
                    },
                    
                },
                "required": ["text"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "summary_search",
            "description": """ 

            # 역할: 사용자의 입력을 저장되어있는 글의 형태로 변환합니다. ,
            # 역할 설명: 사용자의 입력을 받아서 저장되어있는 "summary"의 형태로 변환합니다.

            ### 사용 예시 ###
            # 1번 예시
            질문 = "할머니가 구급차에 실려가는 장면인데 형사와 여학생이 실려가는 할머니를 바라보며 착잡해하는 장면 찾아줘"  
            답변 = "summary: 형사는 구급차에 실려가는 할머니를 보며 착잡한 표정을 짓고, 여학생은 구급차에 실려가는 할머니를 보며 슬퍼한다."

            # 2번 예시
            질문 = "여자 주인공이 차 안에서 뉴스를 보며 살인 사건 소식을 듣는 장면 찾아줘"
            답변 = "summary: 여자는 차 안에서 뉴스를 통해 연쇄 살인 사건의 희생자가 늘어났다는 소식을 듣고 불안해하며"

            # 3번 예시
            질문 = "범인이 어두운 곳에서 줄을 묶거나 무언가 하는 장면 찾아줘"
            답변 = "summary: 범인으로 추정되는 남자가 어두운 곳에서 줄을 묶고, 무언가를 꺼내는 모습이 보인다."
            
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": """ 사용자 입력을 저장되어있는 글의 형태로 변환하여 출력합니다. """,
                    },
                    
                },
                "required": ["text"],
            },
        },
    },



]
