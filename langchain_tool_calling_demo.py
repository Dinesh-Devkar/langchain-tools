from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage,SystemMessage

load_dotenv()

llm=ChatOpenAI(model='gpt-4o')

#tool creation
@tool
def multiply(a:int,b:int):
    """the function takes two integer values as input parameter and return their product"""
    return a*b

# tool binding

llm_with_tool=llm.bind_tools([multiply])

messages=[]

# print(llm.invoke("what is the capital of india"))

# print(llm_with_tool.invoke("what is 2 multiply by 50"))
# print("=="*40)
# print(llm_with_tool.invoke("what is 2 multiply by 50").tool_calls)

user_query=HumanMessage(content="what is 50 multiply by 5")
messages.append(user_query)


ai_message=llm_with_tool.invoke(messages)

messages.append(ai_message)

tool_message=multiply.invoke(ai_message.tool_calls[0])
messages.append(tool_message)

final_result=llm_with_tool.invoke(messages)
print(final_result)
print(type(final_result))