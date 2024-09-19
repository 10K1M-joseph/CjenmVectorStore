from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

from VectorStore.prompt import SYSTEM_MESSAGE

load_dotenv()

model = ChatOpenAI(model="gpt-4o")


def user_input_gpt(user_input):

    llm_results = model.invoke(
        [
            SystemMessage(content=SYSTEM_MESSAGE),
            HumanMessage(content=user_input),
        ]
    )

    return llm_results.content


# print(user_input_gpt("바다풍겨"))
