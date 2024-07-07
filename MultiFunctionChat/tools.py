import pandas as pd
from pandasql import sqldf
import datetime
import json
from rolx import get_rolx_data
import subprocess
from scrape import scrape
from googlesearch import google_search

class Tools:
    def __init__(self):
        self.data = get_rolx_data()

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
    
    def search(self, query):
        results = google_search(query)
        return json.dumps({"results": results})

    def scrape(self, url):
        str = scrape(url)
        return json.dumps({"result": str})
    
    def execute_python_code(self, code):
        
        try:
            print("Executing code: ", code)
            print("\nIs this ok? (y/n)")
            if input() != "y":
                return json.dumps({"error": "Code execution aborted"})
            
            for file in code:
                with open("run\\"+file["filename"], "w", encoding="utf-8") as f:
                    f.write(file["content"])
            
            result = subprocess.run('runsafe.bat', shell=True, capture_output=True, text=True, check=True, timeout=60)
            print("stdout:",result.stdout)
            print("stderr:",result.stderr)
            return json.dumps({"stdout": result.stdout, "stderr": result.stderr})
        except subprocess.TimeoutExpired:
            print("Das Programm wurde abgebrochen, da es länger als 1 Minute gedauert hat.")
            return json.dumps({"error": "Timeout > 1 Minute"})
        except Exception as e:
            print("Exception: ", str(e))
            return json.dumps({"Exception": str(e)})

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
                    "name": "get_timesheet_entries",
                    "description": "Calls a SQL query on the timesheet entries and returns the result as JSON\n"\
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
                    "name": "scrape",
                    "description": "Scrapes a website and returns the contents as markup\n",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The url to scrape",
                            }
                        },
                        "required": ["url"]
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "google_search",
                    "description": "Executes a google search and returns title, link and snippet of the top 10 results.\n",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The query to search for",
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
                    "description": "Executes a given batch script on a windows PC and the given python code and returns the output"\
                       "The files and installed libraries remain in the project folder for subsequent calls and run.bat will be executed after each call.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "program_files": {
                                "type": "string",
                                "description": "A JSON list of files in the format [{\"filename\":\"main.py\", \"content\":\"print('hello world')\"}, "\
                                     "\"filename\":\"run.bat\", \"content\":\"pip install requests \npython main.py\",  ...}\n"\
                                    "The files will be written do a directory and run.bat will be executed.\n"\
                                    "The stdout and stderr output will be returned.\n",
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
            "get_timesheet_entries": self.get_data,
            "execute_python_code": self.execute_python_code,
            "scrape": self.scrape,
            "google_search": self.search
        }  

        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)

        print("Calling function: ", function_name, " with args: ", function_args)

        if function_name == "get_now":
            function_response = function_to_call()
        elif function_name == "get_timesheet_entries":
            function_response = function_to_call(
                sql_query=function_args.get("query")
            )
        elif function_name == "execute_python_code":
            function_response = function_to_call(
                code=function_args.get("program_files")
            )
        elif function_name == "scrape":
            function_response = function_to_call(
                url=function_args.get("url")
            )
        elif function_name == "google_search":
            function_response = function_to_call(
                query=function_args.get("query")
            )

        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            }
        )  # extend conversation with function response
