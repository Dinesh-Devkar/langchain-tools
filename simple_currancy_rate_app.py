from langchain_core.messages import HumanMessage,AIMessage,ToolMessage,SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import requests
from langchain_core.tools import tool
import json


load_dotenv()


# Exchage Rate Tool
@tool("exchange_rate_tool")
def get_exchange_rate(base_currency_code:str,target_currency_code:str):
    """get base country and target countries currency codes and return exchange rate between them"""
    exchange_rate_api=f"https://v6.exchangerate-api.com/v6/a1ac0bfa8999996176c3a2e8/pair/{base_currency_code}/{target_currency_code}"
    response=requests.get(exchange_rate_api)
    return response.json()

#currency converter tool
@tool("convert_currency_rate")
def convert_currency_rate(base_currency_amount:float,exchange_rate:float):
    """ given a currency conversion rate this function calculates the target currency value from a given base currency value"""
    return base_currency_amount*exchange_rate


# print(get_exchange_rate.invoke({'base_currency_code':"USD","target_currency_code":"SGD"}))
# print(convert_currency_rate.invoke({'base_currency_amount':10,"exchange_rate":1.28}))

messages=[SystemMessage(
        content="""
        You are a currency conversion assistant.

        For any currency conversion request:
        1. First call exchange_rate_tool to fetch the exchange rate.
        2. Then call convert_currency_rate using that exchange rate.
        3. Do not perform currency multiplication yourself.
        4. Finally, provide the conversion rate and converted amount.
        """
    )]


llm=ChatOpenAI()

llm_with_tools=llm.bind_tools([get_exchange_rate,convert_currency_rate])

# What is the conversion factor between INR and USD, and based on that can you convert 10 inr to usd

user_query= HumanMessage(content="show the exchange rate for amount 200")

messages.append(user_query)

ai_message = llm_with_tools.invoke(messages)
messages.append(ai_message)
tool_calls= ai_message.tool_calls

print(tool_calls)

for tool_call in tool_calls:
    if tool_call['name']=='exchange_rate_tool':
        tool_message_1=get_exchange_rate.invoke(tool_call)
        messages.append(tool_message_1)

    if tool_call['name']=='currency_converter_tool':
        pass

# print("\n")
# print(messages)
# print("==="*40)
# final_result=llm.invoke(messages)

# print(final_result)












