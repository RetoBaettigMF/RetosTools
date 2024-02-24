import pandas as pd
from settings import EXCELDATA

class ExcelData:
    df = None

    def read_excel(self):
        # Excel-Datei einlesen
        print("Lese Daten aus Excel-Datei ", EXCELDATA, "ein...")
        self.df = pd.read_excel(EXCELDATA)

        # Daten im DataFrame anzeigen
        # print(self.df)

    def __init__(self):
        self.read_excel()
        pass
