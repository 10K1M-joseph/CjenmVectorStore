import os    
import sys   
import time  

# 상위 디렉토리에 있는 모듈을 가져오기 위해 경로를 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from pprint import pprint  
from utils.printer import ColorPrinter as Printer  # 컬러 텍스트 출력을 유틸리티

from available_functions import update_available_functions, all_functions  
from function_to_call import tool_call_function  # GPT의 tool 호출을 처리하기 위한 함수

from apis.gpt_api import gpt_4o, gpt_4o_mini, client  # GPT model

from prompt.system import SYSTEM_SETUP  # 시스템 설정



def ask_gpt_functioncall(query):
    # 사용자의 입력들을 가져오기    
    # last_questions = Input_memory.last_questions()

    try:
        start_time = time.time()  # 시작 시간을 측정

        # 페르소나 입력
        messages = [{"role": "system", "content": SYSTEM_SETUP},]
        
        messages.append({"role": "user", "content": query})

        
        tools = all_functions
        
        
        first_response = client.chat.completions.create(
            model=gpt_4o,
            messages=messages,
            temperature=0.0,
            tools=tools,
            tool_choice="auto",  # default: "auto"
        )

        # GPT의 첫 번째 응답에서 메시지만 파싱
        first_response_message = first_response.choices[0].message

        messages.append(first_response_message) 

        tool_calls = first_response_message.tool_calls
        pprint(tool_calls)
        
        
        if tool_calls:
            # 사용 가능한 함수 목록ㄴ
            available_functions = update_available_functions()
            

            # 각 함수마다 매핑된 함수를 호출
            for tool_call in tool_calls:
                tool_call_reponse = tool_call_function(tool_call, available_functions)
                
            pprint(tool_call_reponse)
            return tool_call_reponse
                
        #         if tool_call_reponse:
                    
        #             messages.append({
        #                 "tool_call_id": tool_call.id,
        #                 "role": "tool",
        #                 "name": tool_call.function.name,
        #                 "content": tool_call_reponse,
        #             })

            
        #     second_response = client.chat.completions.create(
        #         model=gpt_4o,
        #         messages=messages,
        #         temperature=0.0,
        #     )
        
        #     second_response_message = second_response.choices[0].message
            

        #     Printer.color_print(messages)
        #     pprint(second_response_message.content)
        #     end_time = time.time()  # 종료 시간을 측정
        #     print(f"걸린시간: {end_time - start_time} 초")  # 실행 시간을 출력.
        #     return second_response_message.content
        
        # pprint(first_response_message.content)
        # end_time = time.time()
        # print(f"걸린시간: {end_time - start_time} 초")
        # return first_response_message.content
    
    except Exception as e:
        
        print(f"에러메시지: {e}")
        return None     

    

try:
    while True:
        print(
            "궁금한것을 물어보세요"
        )
        user_quote = input("엔터를 눌러 입력하거나 끝내시려면 ctrl + c를 입력하세요: ")
        result = ask_gpt_functioncall(user_quote)
except KeyboardInterrupt:
    print("종료중...")