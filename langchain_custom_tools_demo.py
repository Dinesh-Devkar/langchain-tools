from langchain_core.tools import tool,Tool,StructuredTool,BaseTool
from pydantic import BaseModel,Field
from langchain_core.runnables import RunnableLambda

# Using the @tool decorator
@tool
def multiplication(a:int,b:int):
    """take two numbers as input and return their multiplication"""
    return a*b

result=multiplication.invoke({'a':10,'b':4})
print(result)

@tool("number divider")
def division(a:int,b:int):
    """takes two integer numbers as input and return their division"""
    return a/b

result=division.invoke({'a':10,'b':4})
print(result)

print("=="*30)

print(multiplication.name)
print(multiplication.description)
print(multiplication.args)

print("=="*30)

print(division.name)
print(division.description)
print(division.args)

# Using StructuredTool.from_function()

def addition(a:int,b:int):
    return a+b

def substraction(a:int,b:int):
    return a-b

def calculate_discount_amount(price:float,discount_percent:float):
    return (price*discount_percent)/100

addition_tool=StructuredTool.from_function(name="Addtion Number Tool",description="takes two numbers as input and return their addition",
                                           func=addition)

substraction_tool=StructuredTool.from_function(name="Number Substraction",description="takes two iteger numbers as input and return their substraction",func=substraction)

discount_calculation_tool=StructuredTool.from_function(name='Discount Calculator',description="calculates the discount amount by taking product price and discount pecentage as input",func=calculate_discount_amount)



result=addition_tool.invoke({'a':50,'b':50})
print(result)
print("=="*40)
result=substraction_tool.invoke({'a':50,'b':20})
print(result)

result=discount_calculation_tool.invoke({'price':5000,'discount_percent':20})
print(result)

# Using the Tool class

def convert_uppercase(str:str):
    return str.upper()

uppercase_tool=Tool(name="Uppercase Tool",description="convert given string into uppercase and return",func=convert_uppercase)


result=uppercase_tool.invoke({'str':'hello world'})
print(result)

lowercase_tool=Tool(name="Lower Case Tool",description="convert the given string into lower case",func=lambda str:str.lower())

result=lowercase_tool.invoke({'str':'GOOD MORNING'})
print(result)


# Using @tool with a Pydantic input schema
class Student(BaseModel):
    name:str=Field(name="Name",description="name of the student")
    age:int=Field(name='Age',description="Age of the student",gt=0,lt=100)

def student(name:str,age:int):
    return {'name':name,'age':age}


student_tool=StructuredTool.from_function(name="Student_Tool",description="takes student name and age and return the same value in single string",func=student,args_schema=Student)

print("=="*40)
result=student_tool.invoke({'name':"Dinesh",'age':'30'})
print(result)


class MultiplyInput(BaseModel):
    a: int = Field(required=True, description="The first number to add")
    b: int = Field(required=True, description="The second number to add")

def multiply_func(a: int, b: int) -> int:
    return a * b

multiply_tool = StructuredTool.from_function(
    func=multiply_func,
    name="multiply",
    description="Multiply two numbers",
    args_schema=MultiplyInput
)
result = multiply_tool.invoke({'a':"3", 'b':"3"})

print(result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)


# Creating a custom tool by extending BaseTool

class Product(BaseModel):
    price:float=Field(description="the price of the product")
    quantity:int=Field(description="the quantity of the product")

class ProductInput(BaseTool):
    name:str="Product Input Tool"
    description:str="Take product price and quantity and return total price"
    args_schema:type[BaseModel]=Product

    def _run(self,price:float,quantity:int):
        return price*quantity

product_price_tool=ProductInput()

result=product_price_tool.invoke({'price':2000,'quantity':5})
print(result)


