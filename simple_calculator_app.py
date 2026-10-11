from langchain_core.messages import AIMessage,HumanMessage,SystemMessage,ToolMessage
from langchain_core.tools import tool,InjectedToolArg
from typing import Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Create Tools

@tool
def multiplication_tool(first_number:int,second_number:int)->int:
    """given two numbers function return their product"""
    print("multiplication tool called")
    return first_number*second_number

@tool
def division_tool(first_number:int,second_number:int)->int:
    """given two numbers function return their division"""
    print("division tool called")
    return first_number/second_number

@tool
def addition_tool(first_number:int,second_number:int)->int:
    """given two numbers function return their addition"""
    print("addition tool called")
    return first_number+second_number

@tool
def substraction_tool(first_number:int,second_number:int)->int:
    """given two numbers function return their substraction"""
    print("substraction tool called")
    return first_number-second_number

@tool
def discount_calculation_tool(base_amount:Annotated[float,InjectedToolArg],discount_percentage:float)->float: # type: ignore
    """given base_ammount and discount_percentage function returns the calculated discount amount"""
    print("discount tool called")
    base_amount=float(base_amount)
    # print(type(base_amount))
    # print(type(discount_percentage))
    return (base_amount-(base_amount*discount_percentage)/100)

messages=[]

llm=ChatOpenAI()

llm_with_tool=llm.bind_tools([multiplication_tool,division_tool,addition_tool,substraction_tool,discount_calculation_tool])


user_query=HumanMessage(content="""what will be the output of 5 plus by 60 and then their calculate the discount amount for 10 discount percentage""")
messages.append(user_query)
ai_message=llm_with_tool.invoke(messages)

messages.append(ai_message)
print(ai_message)
print("=="*50)
for tool_call in ai_message.tool_calls:
    if tool_call['name']=='multiplication_tool':
        
        mul_tool_message=multiplication_tool.invoke(tool_call)
        messages.append(mul_tool_message)
        # print(mul_tool_message)
        # print(mul_tool_message.content)
        mul_tool_arg=add_tool_message.content
    if tool_call['name']=='addition_tool':
            
            add_tool_message=addition_tool.invoke(tool_call)
            messages.append(add_tool_message)
            # print(mul_tool_message)
            # print(mul_tool_message.content)
            mul_tool_arg=add_tool_message.content
    if tool_call['name']=='discount_calculation_tool':
        # print("Helooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        tool_call['args']['base_amount']=mul_tool_arg
        # print(tool_call)
        dis_tool_message=discount_calculation_tool.invoke(tool_call)
        # print(dis_tool_message)
        messages.append(dis_tool_message)

print('=='*50)

# print(messages)
final_result=llm_with_tool.invoke(messages)

print(final_result.content)