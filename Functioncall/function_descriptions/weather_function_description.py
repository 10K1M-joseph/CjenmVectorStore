weather_function = [  

    {
            "type": "function",
            "function": {
                "name": "weather_forecast",
                "description": "현재 위치에 대한 날씨를 기상청에게 데이터를 받아 알려주는 기능합니다. 위치정보가 들어오지 않았을 경우 '위치정보를 알려달라는 메시지를 호출합니다.'",
                "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "서울 날씨 알려줘, 대구 날씨 어때?, 부산에 비와?, 대전에 눈와?" 
                    },
                    "location": {
                        "type": "string",
                        "description": "지역 이름, 예를 들면: '서울', '부산', '대구'. '대전', '인천'"
                    }
                },
                "required":["location", "text"]
            }
        }
    }

    


]