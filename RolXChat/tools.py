import pandas as pd
from pandasql import sqldf
import datetime
import json
from rolx_connector import rolX

class Tools:
    def __init__(self):
        try:
            rolx = rolX()
            self.data = rolx.get_last_num_days(60)
        except Exception as e:
            print("Could not connect to rolX database: ", str(e))
            print("Using example data instead.")
            self.data = pd.read_excel("rolx_example.xlsx")
        
        print(self.data.head().to_string())
        self.data.to_excel('rolx_example.xlsx', index=False)
    

    def get_data(self, sql_query):
        try:
            result = sqldf(sql_query, self.__dict__)
        except Exception as e:
            return json.dumps({"error": str(e)})
        
        result = result.to_json(orient="records")
        return result

    def get_now(self):
        now = datetime.datetime.now()
        str = now.strftime("%d.%m.%Y %H:%M:%S")
        return json.dumps({"datetime": str})

    def get_tools(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_now",
                    "description": "Gets the actual date and time",
                    "parameters": {}
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_data",
                    "description": "Calls a SQL query on the data and returns the result as JSON\n"\
                        "The header and first line of table=\"data\" looks like this:\n"\
                        + self.data.head(1).to_string() + "\n",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The SQL query to call on the data",
                            }
                        },
                        "required": ["query"]
                    },
                }
            }]
        return tools
    
    def handle_tool_call(self, tool_call, messages):
        if not tool_call:
            return None
        
        available_functions = {
            "get_now": self.get_now,
            "get_data": self.get_data
        }  

        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)

        print("Calling function: ", function_name, " with args: ", function_args)

        if function_name == "get_now":
            function_response = function_to_call()
        elif function_name == "get_data":
            function_response = function_to_call(
                sql_query=function_args.get("query")
            )

        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            }
        )  # extend conversation with function response
