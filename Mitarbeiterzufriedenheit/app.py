from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

# Antwortoptionen
options = [
    "Trifft fast gar nicht zu",
    "Trifft überwiegend nicht zu",
    "Teils/teils",
    "Trifft überwiegend zu",
    "Trifft fast völlig zu"
]

# Alle 65 Fragen der Umfrage
questions = [
    "1. Ich bekomme die notwendigen Mittel und die Ausstattung, um meine Arbeit gut zu erledigen.",
    "2. Die körperliche Sicherheit am Arbeitsplatz ist gewährleistet.",
    "3. Jeder hat hier die Möglichkeit, Aufmerksamkeit und Anerkennung zu bekommen.",
    "4. Die Mitarbeitenden hier sind bereit, zusätzlichen Einsatz zu leisten, um die Arbeit zu erledigen.",
    "5. Man kann sich darauf verlassen, dass die Mitarbeitenden zusammenarbeiten.",
    "6. Die Führungskräfte machen ihre Erwartungen klar und deutlich.",
    "7. Ich kann mich mit jeder vernünftigen Frage an die Führungskräfte wenden und erhalte eine direkte und offene Antwort.",
    "8. Mir wird Weiterbildung und Unterstützung für meine berufliche Entwicklung angeboten.",
    "9. Die Führungskräfte zeigen Anerkennung für gute Arbeit und besonderen Einsatz.",
    "10. Die Mitarbeitenden werden hier für die geleistete Arbeit angemessen bezahlt.",
    "11. Meine Arbeit hat für mich besondere Bedeutung und Sinn – sie ist weit mehr als ein 'Job'.",
    "12. Wenn Mitarbeitende innerhalb der Organisation ihre Funktion oder die Abteilung wechseln, werden sie gut aufgenommen und integriert.",
    "13. Die Führungskräfte sind gut erreichbar und unkompliziert anzusprechen.",
    "14. Die Führungskräfte erkennen an, dass bei der Arbeit auch Fehler passieren können.",
    "15. Die Führungskräfte suchen und beantworten ernsthaft Vorschläge und Ideen der Mitarbeitenden.",
    "16. Ich bin stolz auf das, was wir hier gemeinsam leisten.",
    "17. Ich denke, ich werde angemessen am Erfolg des Unternehmens beteiligt.",
    "18. Die Führungskräfte halten mich über wichtige Themen und Veränderungen auf dem Laufenden.",
    "19. Die Führungskräfte haben klare Vorstellungen von den Zielen der Organisation und davon, wie diese erreicht werden können.",
    "20. Die Führungskräfte vertrauen auf die gute Arbeit der Mitarbeitenden, ohne sie ständig zu kontrollieren.",
    "21. Die Führungskräfte beziehen die Mitarbeitenden in Entscheidungen ein, die ihre Arbeit oder das Arbeitsumfeld betreffen.",
    "22. Die Führungskräfte vermeiden die Bevorzugung einzelner Mitarbeitenden.",
    "23. Ich bin zufrieden mit der Art und Weise, in der wir einen Beitrag für die Gesellschaft leisten.",
    "24. Die Führungskräfte leisten gute Arbeit bei der Zuweisung von Aufgaben und der Koordination der Mitarbeitenden.",
    "25. Den Mitarbeitenden wird hier viel Verantwortung übertragen.",
    "26. Die psychische und emotionale Gesundheit ist an diesem Arbeitsplatz gewährleistet.",
    "27. Die Mitarbeitenden werden unabhängig von ihrem Alter fair behandelt.",
    "28. Befördert werden diejenigen Mitarbeitenden, die es am meisten verdienen.",
    "29. Die Mitarbeitenden kommen gerne zur Arbeit.",
    "30. Ich kann hier 'ich selbst sein' und brauche mich nicht zu verstellen.",
    "31. Die Führungskräfte halten ihre Versprechen ein.",
    "32. Die Mitarbeitenden werden unabhängig von Nationalität oder ethnischer Herkunft fair behandelt.",
    "33. Die Mitarbeitenden kümmern sich hier umeinander.",
    "34. Die Führungskräfte lassen ihren Worten Taten folgen.",
    "35. Unsere Gebäude und die Einrichtungen tragen zu einer guten Arbeitsumgebung bei.",
    "36. Die Mitarbeitenden werden unabhängig von ihrem Geschlecht fair behandelt.",
    "37. Ich bin stolz, anderen erzählen zu können, dass ich hier arbeite.",
    "38. Besondere Ereignisse werden bei uns gefeiert.",
    "39. Ich glaube, dass die Führungskräfte Kündigungen nur als letzten Ausweg wählen.",
    "40. Die Mitarbeitenden unterlassen verdeckte Machenschaften und Intrigen, um etwas zu erreichen.",
    "41. Die Mitarbeitenden werden ermutigt, einen guten Ausgleich zwischen Berufs- und Privatleben zu finden.",
    "42. Die Mitarbeitenden werden unabhängig von ihrer sexuellen Orientierung fair behandelt.",
    "43. Die Führungskräfte machen ihre Arbeit kompetent.",
    "44. Wenn ich ungerecht behandelt werde und mich beschwere, bin ich überzeugt, dass damit fair umgegangen wird.",
    "45. Wir haben besondere und attraktive Sozialleistungen.",
    "46. Die Geschäftspraktiken der Führungskräfte sind ehrlich und ethisch vertretbar.",
    "47. Die Führungskräfte zeigen aufrichtiges Interesse an mir als Person und nicht nur als Arbeitskraft.",
    "48. Ich möchte hier noch lange arbeiten.",
    "49. Ich werde hier unabhängig von meiner Position als vollwertiges Mitglied behandelt.",
    "50. Ich kann mir Zeit frei nehmen, wenn ich es für notwendig halte.",
    "51. Ich glaube, ich kann hier einen wichtigen Beitrag leisten.",
    "52. Neue Mitarbeitende fühlen sich hier willkommen.",
    "53. Wir haben hier Spaß bei der Arbeit.",
    "54. Die Führungskräfte stellen Mitarbeitende ein, die gut hierher passen.",
    "55. Freunden und Familie würde ich meine Organisation als sehr guten Arbeitgeber empfehlen.",
    "56. Ich glaube, unsere Kunden finden unsere Dienstleistungen und Produkte exzellent.",
    "57. Die oberen Führungskräfte leben die besten Eigenschaften unserer Organisation vor.",
    "58. Wir schätzen hier besonders, wenn man versucht, Dinge neu oder besser zu machen – auch wenn es nicht klappt.",
    "59. Die Mitarbeitenden stellen sich schnell auf Veränderungen ein, wenn das für den Erfolg unserer Organisation notwendig ist.",
    "60. Offenes und ehrliches Feedback ist selbstverständlicher Teil unserer Arbeit.",
    "61. Ich kann meine Fähigkeiten hier optimal einbringen.",
    "62. Die Mitarbeitenden erhalten hilfreiche Maßnahmen zur Förderung der Gesundheit.",
    "63. Wir fühlen uns hier wie eine 'Familie' bzw. haben einen guten Teamgeist.",
    "64. Wir ziehen hier alle an einem Strang.",
    "65. Alles in allem kann ich sagen, dies hier ist ein sehr guter Arbeitsplatz."
]

# Alle 22 Fragen zur direkten Führungskraft und zum unmittelbaren Arbeitsbereich
direct_leadership_questions = [
    "1. In meinem Team hat jeder die Möglichkeit, Aufmerksamkeit und Anerkennung zu bekommen.",
    "2. In meinem Team sind die Mitarbeitenden bereit, zusätzlichen Einsatz zu leisten, um die Arbeit zu erledigen.",
    "3. Meine Führungskraft macht ihre Erwartungen klar und deutlich.",
    "4. Ich kann mich mit jeder vernünftigen Frage an meine Führungskraft wenden und erhalte eine direkte und offene Antwort.",
    "5. Meine Führungskraft achtet darauf, dass mir Weiterbildung und Unterstützung für meine berufliche Entwicklung angeboten wird.",
    "6. Meine Führungskraft zeigt Anerkennung für gute Arbeit und besonderen Einsatz.",
    "7. Meine Führungskraft ist gut erreichbar und unkompliziert anzusprechen.",
    "8. Meine Führungskraft erkennt an, dass bei der Arbeit auch Fehler passieren können.",
    "9. Meine Führungskraft sucht und beantwortet ernsthaft Vorschläge und Ideen der Mitarbeitenden.",
    "10. Ich bin stolz auf das, was wir in meinem Team gemeinsam leisten.",
    "11. Meine Führungskraft hält mich über wichtige Themen und Veränderungen auf dem Laufenden.",
    "12. Meine Führungskraft vertraut auf die gute Arbeit der Mitarbeitenden, ohne sie ständig zu kontrollieren.",
    "13. Meine Führungskraft bezieht die Mitarbeitenden in Entscheidungen ein, die ihre Arbeit oder das Arbeitsumfeld betreffen.",
    "14. Meine Führungskraft vermeidet die Bevorzugung einzelner Mitarbeitenden.",
    "15. Meine Führungskraft leistet gute Arbeit bei der Zuweisung von Aufgaben und der Koordination der Mitarbeitenden.",
    "16. Ich kann in meinem Team 'ich selbst sein' und brauche mich nicht zu verstellen.",
    "17. Meine Führungskraft lässt ihren Worten Taten folgen.",
    "18. In meinem Team fühlen wir uns wie eine 'Familie' bzw. haben einen guten Teamgeist.",
    "19. Besondere Ereignisse werden bei uns im Team gefeiert.",
    "20. Meine Führungskraft macht ihre Arbeit kompetent.",
    "21. Wir ziehen in meinem Team alle an einem Strang.",
    "22. Meine Führungskraft zeigt aufrichtiges Interesse an mir als Person und nicht nur als Arbeitskraft."
]

# Funktion zum Überprüfen, ob der Mitarbeiter bereits teilgenommen hat
def has_participated(employee_id):
    if not os.path.exists('responses.csv'):
        return False
    with open('responses.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and row[0] == employee_id:
                return True
    return False

# Route für die Startseite
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        if has_participated(employee_id):
            return render_template('already_participated.html')
        else:
            return redirect(f'/survey/{employee_id}')
    return render_template('index.html')

# Route für die Umfrage
@app.route('/survey/<employee_id>', methods=['GET', 'POST'])
def survey(employee_id):
    if has_participated(employee_id):
        return render_template('already_participated.html')
    if request.method == 'POST':
        responses = [employee_id]
        # Allgemeine Fragen
        for i in range(len(questions)):
            response = request.form.get(f'question_{i}')
            if response is None:
                response = ''
            responses.append(response)
        # Fragen zur direkten Führungskraft
        for i in range(len(direct_leadership_questions)):
            response = request.form.get(f'dl_question_{i}')
            if response is None:
                response = ''
            responses.append(response)
        with open('responses.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(responses)
        return render_template('thank_you.html')
    return render_template(
        'survey.html',
        employee_id=employee_id,
        questions=questions,
        options=options,
        direct_leadership_questions=direct_leadership_questions
    )

if __name__ == '__main__':
    app.run(debug=True)
