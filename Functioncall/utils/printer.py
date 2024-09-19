class ColorPrinter:
    _color_mapping = {
        "system": "\033[33m",  # Yellow
        "tool_call_id": "\033[33m",
        "user": "\033[32m",  # Green
        "tool": "\033[34m",  # Blue
        "assistant": "\033[35m",  # Purple
        "header": "\033[36m",  # Cyan
        "undefined": "\033[37m",  # White
        "closing_tag": "\033[00m",
    }

    # 정적 메소드
    @staticmethod
    def _color_text_line(message) -> str:
        # 메시지 뒤에 색상을 리셋하기 위한 종료 태그를 검색
        color_closing_tag = ColorPrinter._color_mapping["closing_tag"]

        # 메시지가 dictionary인지 확인하고 role, content 추출
        if isinstance(message, dict):
            # 메시지에서 role 가져오며, 찾을 수 없는 경우 "undefined"로 설정
            role = message.get("role", "undefined")
            # 메시지에서 content 가져오며, 찾을 수 없는 경우 "No content"로 설정
            content = message.get("content", "No content")
        else:
            # 메시지가 dictionary가 아닌 경우 속성을 직접 가져옴
            role = getattr(message, 'role', 'undefined')
            content = getattr(message, 'content', 'No content')

        # 메시지 role에 기반한 색상 코드 태그를 가져오며, role을 찾을 수 없는 경우 undefined 색상으로 설정
        color_open_tag = ColorPrinter._color_mapping.get(role, ColorPrinter._color_mapping["undefined"])

        # 색상이 적용된 텍스트 라인을 반환
        return f"{color_open_tag}{role} : {content}{color_closing_tag}"

    # 정적 메소드
    @staticmethod
    def color_print(messages) -> None:
        # 헤더와 종료 태그에 대한 색상 코드를 검색
        cyan_open_tag = ColorPrinter._color_mapping["header"]
        color_closing_tag = ColorPrinter._color_mapping["closing_tag"]
        # 대화 기록의 헤더를 출력
        print(f"\n{cyan_open_tag}###### Conversation History ######{color_closing_tag}")
        # 각 메시지를 순회하며 색상 코딩하여 출력
        for message in messages:
            print(ColorPrinter._color_text_line(message))
        # 대화 기록 출력합니다.
        print(f"{cyan_open_tag}##################################{color_closing_tag}\n")