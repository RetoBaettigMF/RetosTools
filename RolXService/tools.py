import pandas as pd
from pandasql import sqldf
import datetime
import json

class Tools:
    def __init__(self, rolx):
        self.rolx = rolx

    def get_rolx_data(self, sql_query):
        try:
            result = self.rolx.get_data(sql_query) 
        except Exception as e:
            return json.dumps({"error": str(e)})
        
        return result

    def get_tools(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_rolx_data",
                    "description": "Gets timesheet data from the RolX database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": """
The SQL query for the table 'data'.
The fields of the timesheet database include:
date, firstName, lastName, projectNumber, subprojectNumber, activityNumber, orderNumber (in the form of #0123.456 where 123 is the projectNumber and 456 is the subprojectNumber), customerName, projectName, subprojectName, activityName, durationHours, billabilityName, isBillable (1 for billable, 0 for non-billable), comment.
If you have to calculate the billability, do the following:
- get all hours where billabilityName!=Abwesenheit as Anwesenheit
- get all hours where isBillable = 1 as Billable
- calculate the billability as Billable/Anwesenheit

If ever possible, do the calculations in the SQL statement.
Wrap all dates in the query with the DATE() function.
""",
                            }
                        },
                        "required": ["query"]
                    },
                }
            }]
        return tools
    
    def call_function(self, function_name, function_to_call, function_args):
        if function_name == "get_rolx_data":
            function_response = function_to_call(
                sql_query=function_args.get("query")
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
            "get_rolx_data": self.get_rolx_data
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


