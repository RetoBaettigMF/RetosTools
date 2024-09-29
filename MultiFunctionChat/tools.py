import pandas as pd
from pandasql import sqldf
import datetime
import json
from rolx import get_rolx_data
from codeexecuter import execute_code
from scrape import scrape
from googlesearch import google_search
from gmail import gmail_search

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
    
    def gmail_search(self, query):
        results = gmail_search(query)
        return json.dumps({"results": results})

    def scrape(self, url):
        str = scrape(url)
        return json.dumps({"result": str})
    
    def execute_python_code(self, code):
        result = execute_code(code)
        return result

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
                    "name": "gmail_search",
                    "description": "Executes a search in all my google mails and returns the emails\n"\
                        "The query must be in gmail search format\n",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The query to search for in gmail search format (e.g. in:sent from:reto@baettig.org)",
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
                                    "Always add a run.bat to the list of files!\n"\
                                    "The stdout and stderr output will be returned.\n",
                            }
                        },
                        "required": ["code"]
                    },
                }
            }]
        return tools
    
    def call_function(self, function_name, function_to_call, function_args):
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
        elif function_name == "gmail_search":
            function_response = function_to_call(
                query=function_args.get("query")
            )
        else:
            print("Function not found: ", function_name)
            function_response = json.dumps({"error": "function not found: "+function_name})
        return function_response

    
    def handle_tool_call(self, tool_call, messages):
        error = False
        if not tool_call:
            return None
        
        available_functions = {
            "get_now": self.get_now,
            "get_timesheet_entries": self.get_data,
            "execute_python_code": self.execute_python_code,
            "scrape": self.scrape,
            "google_search": self.search,
            "gmail_search" : self.gmail_search
        }  

        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        try:
            function_args = json.loads(tool_call.function.arguments)
        except Exception as e:
            function_args = {}
            error = str(e)
            print("Error: ", e)

        print("Calling function: ", function_name, " with args: ", function_args)

        function_response = self.call_function(function_name, function_to_call, function_args)
        
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            }
        )  # extend conversation with function response
