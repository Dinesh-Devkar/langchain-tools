from langchain_community.tools import DuckDuckGoSearchRun,ShellTool

# Built-in Tool - DuckDuckGo Search
search_tool=DuckDuckGoSearchRun()

# result=search_tool.invoke('who is virat kohli')

# print(result)

# Built-in Tool - Shell Tool

shell_tool=ShellTool()
result=shell_tool.invoke('dir')
print(result)