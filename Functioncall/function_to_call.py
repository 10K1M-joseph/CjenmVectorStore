import json


def tool_call_function(tool_call, available_functions):

    # 호출할 함수의 이름을 추출합니다.
    function_name = tool_call.function.name

    # 해당 함수를 가져옵니다.
    function_to_call = available_functions.get(function_name)

    # 함수를 찾지 못하면 None을 반환합니다.
    if not function_to_call:
        return None

    # 함수의 arguments를 추출하고 JSON 형태로 변환합니다.
    function_args = json.loads(tool_call.function.arguments)

    if function_name.startswith("weather_"):
        # 'weather_' 함수인 경우 'location' args를 전달합니다.
        return function_to_call(location=function_args.get("location"))

    elif function_name == ("keyword_search"):
        
        return function_to_call(text=function_args.get("text"))

    elif function_name == ("summary_search"):
        
        return function_to_call(text=function_args.get("text"))

    else:
        # 다른 함수들은 모든 args를 그대로 전달하여 호출합니다.
        return function_to_call(**function_args)
