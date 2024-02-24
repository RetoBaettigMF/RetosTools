from docxtpl import DocxTemplate
from settings import WORDTEMPLATE
from gpt import get_single_completion
import json

class WordFiller:
    doc = None
    df = None

    def getAIData2(self, challenge, angebot, referenzen):
        print("Generiere Texte für folgende Challenge: "+challenge)
        if not isinstance(referenzen, str):
            referenzen = ""
        prompt = "Du bist ein Marketing-Experte und musst für die Webseite des Software-Dienslteisters CUDOS ihr Angebot beschreiben."\
        "CUDOS bietet Individualsoftwareentwicklung, Beratung und Personalverleih für Unternehmen (B2B) an."\
        "Du kriegst kurz zusammengefasst ein Kundenbedürfnis, ein mögliches Angebot dazu und Referenzbeispiele"\
        "Generiere auch einen Filenamen, um dieses Angebot in ein Word-Dokument zu speichern."\
        "Liefere daraus ein JSON zurück mit ausformulierten Texten für die Webseite in folgendem Format"\
        "{\"Titel\": ..., \"Challenge\", \"Angebot\": .., \"Vorgehen\": ..., \"Referenzen\": ..., \"Filename\": ...}"\
        "Hier die Infos:\n---\n"\
        "Challenge:"+challenge+"\n"\
        "Angebot:"+angebot+"\n"\
        "Referenzen:"+referenzen+"\n---"
        answer = get_single_completion(prompt)
        return json.loads(answer)

    def getAIData(self, row):
        data = self.getAIData2(row["Kundenbedürfnis"], row["Angebote"], row["Beispiele"])    
        return data

    def fill_word(self, row):
        # Daten in die Vorlage einfügen
        context = self.getAIData(row)
        self.doc.render(context)
        
        # Word-Dokument speichern
        print("Speichere Angebot in Word-Dokument "+context.get("Filename")+"...")
        self.doc.save(context.get("Filename"))

    def fill_words(self):
        for index, row in self.df.iterrows():
            print("Generiere "+str(index+1)+". Angebot...")
            self.fill_word(row)

    def __init__(self, exceldata):
        self.df = exceldata.df
        self.doc = DocxTemplate(WORDTEMPLATE)
        pass
