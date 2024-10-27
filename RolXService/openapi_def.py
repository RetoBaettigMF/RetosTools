OPENAPI_DEF = """
    {
  "openapi": "3.1.0",
  "info": {
    "title": "Get timesheet entries",
    "description": "Retrieves timesheet entries for the company",
    "version": "v1.0.0"
  },
  "servers": [
    {
      "url": "https://baettig.org"
    }
  ],
  "paths": {
    "/rolx/sqlquery": {
      "get": {
        "description": "Get timesheet data",
        "operationId": "SQLQuery",
    
        "parameters": [
          {
            "name": "query",
            "in": "query",
            "description": "The SQL query for the table 'data'.
The fields of the timesheet database include:
date, firstName, lastName, projectNumber, subprojectNumber, activityNumber, orderNumber (in the form of #0123.456 where 123 is the projectNumber and 456 is the subprojectNumber), customerName, projectName, subprojectName, activityName, durationHours, billabilityName, isBillable (1 for billable, 0 for non-billable), comment.
If you have to calculate the billability, do the following:
- get all hours where billabilityName!=Abwesenheit as Anwesenheit
- get all hours where isBillable = 1 as Billable
- calculate the billability as Billable/Anwesenheit

If ever possible, do the calculations in the SQL statement.",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        
        "deprecated": false
      }
    }
  },
  "components": {
    "schemas": {}
  }
}"""