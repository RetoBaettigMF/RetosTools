import json
import subprocess
import os
import shutil

first = True

def execute_code(code):
        global first
        if first:
             #delete all files in /run folder
            shutil.rmtree("run\*")
            first = False

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
