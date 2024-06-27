import pandas as pd
from pandasql import sqldf
import datetime
import json
from rolx_connector import rolX
import sys
import io

class Tools:
    def __init__(self):
        try:
            rolx = rolX()
            self.data = rolx.get_last_num_days(60)
            #self.data = rolx.get_month(2024, 2)           
            self.data.to_excel('rolx_example.xlsx', index=False)
        except Exception as e:
            print("Could not connect to rolX database: ", str(e))
            print("Using example data instead.")
            self.data = pd.read_excel("rolx_example.xlsx")
    

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
    
    def execute_python_code(self, code):
        
        try:
            print("Executing code: ", code)
            print("\nIs this ok? (y/n)")
            if input() != "y":
                return json.dumps({"error": "Code execution aborted"})
            
            for file in code:
                with open("run\\"+file["filename"], "w") as f:
                    f.write(file["content"])
        
            
            original_stdout = sys.stdout  # Save a reference to the original standard output
            captured_output = io.StringIO()  # Create a StringIO object to capture output
            sys.stdout = captured_output  # Redirect stdout to the StringIO object
            exec(code)
            sys.stdout = original_stdout  # Reset redirection
            print("Captured:", captured_output.getvalue())  # Display captured output
            return json.dumps({"output": captured_output.getvalue()})
            
        except Exception as e:
            return json.dumps({"error": str(e)})
        return json.dumps({"result": "Code executed successfully"})

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
                        "For dates, use the format 'YYYY-MM-DD\n"\
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
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_python_code",
                    "description": "Executes the given python code and returns the output",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "program_files": {
                                "type": "string",
                                "description": "A JSON list of files in the format [{\"filename\":\"main.py\", \"content\":\"print('hello world')\"}, ...}\n"\
                                    "The files will be written do a directory and main.py will be executed.\n"\
                                    "The console output will be returned.\n",
                            }
                        },
                        "required": ["code"]
                    },
                }
            }]
        return tools
    
    def handle_tool_call(self, tool_call, messages):
        if not tool_call:
            return None
        
        available_functions = {
            "get_now": self.get_now,
            "get_data": self.get_data,
            "execute_python_code": self.execute_python_code
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
        elif function_name == "execute_python_code":
            function_response = function_to_call(
                code=function_args.get("program_files")
            )

        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            }
        )  # extend conversation with function response
