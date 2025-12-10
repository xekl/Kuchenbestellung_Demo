
# info texts
info_text_en = """This demonstrator shows how AI can help optimize cake ordering by using past sales patterns and additional data. It demonstrates the challenge we tackled in the Green-AI-Hub project ["KI-basierte Prognosen für Lebensmittelproduktion"](https://www.green-ai-hub.de/pilotprojekte/pilotprojekt-brammibals-donuts-foodtracks): How to reduce food waste while maximizing sales?

## How to use?

Below, you can view information on what kind of day tomorrow will be and place an order for tomorrow's cakes. To the right, you can request AI assistance for the order, from a simple heuristic to advanced machine learning. Once you have placed an order, press the button to end the day and see results based on that day's demand. 

Feel free to experiment with order decisions, compare AI suggestions, and see how changes impact food waste and sales. Switch on historic data in the sidebar to deep-dive into past sales and weather trends to understand demand patterns. 

## A note on realism
The data used in this demonstrator is created automatically on startup. You can create new data and reset the date by reloading the page. Due to its synthetic origin, the data is simpler and cleaner than you would see in a real sales system, but its patterns are modeled after actual bakery sales we encountered in the project. 

Of course, in a real interface, you would not see the **missed potential** when you are sold out. In actual past sales data, this lack of information makes it difficult to estimate the error, as you don't know how many more cakes could have been sold, making sold-out days both a success and a challenge. 

In the demonstrator, an **unexpected event** represents a sudden change in demand that was not predictable from historical trends, weather, or holidays. This could be an unplanned school closure reducing foot traffic, or a supply chain issue limiting stock. In real life, such events pose challenges for AI models, as they introduce anomalies that standard forecasting methods struggle to capture. Additionally, there usually is no way to log such events in past sales and thus for algorithms to learn from them. Recognizing and handling unexpected events is key to improving forecasting accuracy and decision-making.
"""
info_text_de = """Dieser Demonstrator zeigt, wie KI dabei helfen kann, Kuchenbestellungen zu optimieren, indem sie vergangene Verkaufsdaten und zusätzliche Faktoren analysiert. Er veranschaulicht die Herausforderung, die wir im Green-AI-Hub-Projekt ["KI-basierte Prognosen für Lebensmittelproduktion"](https://www.green-ai-hub.de/pilotprojekte/pilotprojekt-brammibals-donuts-foodtracks) untersucht haben: Wie kann man Lebensmittelverschwendung reduzieren und gleichzeitig den Umsatz maximieren?
## Wie funktioniert es?

Unten sehen Sie Informationen darüber, was für ein Tag morgen sein wird, und können eine Kuchenbestellung für morgen aufgeben. Rechts haben Sie die Möglichkeit, KI-Unterstützung anzufordern – von einer einfachen Heuristik bis hin zu fortschrittlichem maschinellen Lernen. Sobald Sie Ihre Bestellung aufgegeben haben, drücken Sie den Button, um den Tag zu beenden und zu sehen, wie sich Ihre Entscheidung auf die tatsächliche Nachfrage auswirkt.

Experimentieren Sie mit Ihren Bestellentscheidungen, vergleichen Sie die KI-Vorschläge und beobachten Sie, wie sich Änderungen auf Lebensmittelverschwendung und Umsatz auswirken. Aktivieren Sie die historischen Daten in der Seitenleiste, um tiefere Einblicke in vergangene Verkaufszahlen und Wettertrends zu erhalten und Nachfrage-Muster besser zu verstehen.

## Hinweis zum Realismus

Die in diesem Demonstrator verwendeten Daten werden beim Start automatisch generiert. Sie können neue Daten erzeugen und das Datum zurücksetzen, indem Sie die Seite neu laden. Da die Daten synthetisch erstellt wurden, sind sie schlichter und sauberer als echte Verkaufsdaten. Ihre Muster basieren jedoch auf realen Bäckereiverkäufen, die wir im Projekt untersucht haben.

Natürlich würde man in einer echten Verkaufsoberfläche die **verpasste Nachfrage** bei einem Ausverkauf nicht sehen. In realen Verkaufsdaten erschwert dieser Informationsmangel die Fehlerabschätzung, da unklar bleibt, wie viele zusätzliche Kuchen hätten verkauft werden können. Das bedeutet, dass ausverkaufte Tage sowohl einen Erfolg als auch eine Herausforderung darstellen.

Im Demonstrator steht ein **unerwartetes Ereignis** für eine plötzliche Nachfrageänderung, die nicht aus historischen Trends, dem Wetter oder Feiertagen vorhersehbar war. Dies könnte beispielsweise eine ungeplante Schulschließung sein, die die Kundenfrequenz reduziert, oder ein Lieferkettenproblem, das die Verfügbarkeit einschränkt. In der Realität sind solche Ereignisse eine Herausforderung für KI-Modelle, da sie Anomalien darstellen, die von herkömmlichen Prognosemethoden nur schwer erfasst werden können. Zudem gibt es oft keine Möglichkeit, solche Ereignisse systematisch in den Verkaufsdaten zu erfassen, sodass Algorithmen nicht daraus lernen können. Die Identifikation und Berücksichtigung unerwarteter Ereignisse ist daher entscheidend für eine verbesserte Prognosegenauigkeit und fundiertere Entscheidungen.
"""

# Translations
def get_localized_string(text, lang="Deutsch"):
    translations = {

        # streamlit page 
        "pagetitle": {"Deutsch": "KI-Kuchenbestellung", "English": "AI Cake Ordering"}, 
        "heading1": {"Deutsch": "🍰 KI gegen Lebensmittelverschwendung", "English": "🍰 Fight Food Waste with AI"},
        "introtext": {"Deutsch": "Wie kann KI dabei helfen Kuchenbestellung zu optimieren und Verschwendung zu reduzieren?", "English": "How can AI assist optimizing cake ordering and reducing food waste?"},
        "orderingtitle": {"Deutsch": "Bestellung für morgen", "English": "Order for tomorrow"},
        "tomorrow": {"Deutsch": "Morgen ist", "English": "Tomorrow is"},
        "ordercommand": {"Deutsch": "Wie viele Kuchen bestellen?", "English": "How many cakes to order?"},
        "endday": {"Deutsch": "Tag beenden & Ergebnisse sehen", "English": "End the Day & See Results"},
        "resultsummary": {"Deutsch": "Ergebnisse", "English": "Results"},
        "options": {"Deutsch": "Optionen", "English": "Options"},
        "showhistory": {"Deutsch": "Verkaufshistorie anzeigen", "English": "Show Sales History"},
        "showinfo": {"Deutsch": "Info & Erklärung", "English": "Show Info & Explanation"},
        "infotext": {"Deutsch": info_text_de, "English": info_text_en},
        "feedbackTooMany": {"Deutsch": "Es sind viele Kuchen übrig geblieben. Verschwendung lässt sich reduzieren durch kleinere Bestellungen.", "English": "You ordered too many cakes for today. Consider reducing your order tomorrow."},
        "feedbackTooFew": {"Deutsch": "Es waren zu wenig Kuchen da. KundInnen mussten ohne Kuchen nach Hause gehen.", "English": "You ordered too few cakes for today. Customers left without a purchase."},
        "feedbackJustRight": {"Deutsch": "Gut gemacht! Bestellung und Bedarf waren annähernd gleich.", "English": "Great job! Your order matched demand well."},
        "salesHistory": {"Deutsch": "Verkaufshistorie", "English": "Sales History"},
        "weatherHistory": {"Deutsch": "Wetter", "English": "weather"},
        "salesAxis": {"Deutsch": "verkaufte Kuchen", "English": "sold cakes"},
        "orderAxis": {"Deutsch": "Bestellung", "English": "Order"},
        "dateAxis": {"Deutsch": "Datum", "English": "Date"},
        "temperatureAxis": {"Deutsch": "Temperatur °C", "English": "temperature °C"},
        "weatherAxis": {"Deutsch": "Wetter", "English": "weather"},
        "aiHelp": {"Deutsch": "KI-Vorhersage", "English": "AI prediction"},
        "modelLabel": {"Deutsch": "Vorhersagemodell", "English": "prediction model"},
        "modelHeu": {"Deutsch": "Heuristik", "English": "heuristic"},
        "modelKNN": {"Deutsch": "KNN", "English": "KNN"},
        "modelXGB": {"Deutsch": "XGBoost", "English": "XGBoost"},
        "explainButton": {"Deutsch": "Erklärung anzeigen", "English": "Show explanation"},    
        "budgetExplanation": {"Deutsch": "Kuchen kosten bei der Bestellung 2€ und lassen sich für 3€ verkaufen", "English": "Cakes cost €2 and sell for €3"},

        # data fields 
        "sales": {"Deutsch": "Verkauft", "English": "Sold"},
        "weather": {"Deutsch": "Wetter", "English": "Weather"},
        "temperature": {"Deutsch": "Temperatur", "English": "Temperature"},
        "daytype": {"Deutsch": "Tagestyp", "English": "Day Type"},
        "resultsold": {"Deutsch": "Nachfrage", "English": "Demand"},
        "resultleftover": {"Deutsch": "Übrig", "English": "Leftover"},
        "resultmissed": {"Deutsch": "Verpasste Verkäufe", "English": "Missed sales"},
        "unexpectedevent": {"Deutsch": "Unerwartetes Ereignis!", "English": "Unexpected event!"},
        "Monday": {"Deutsch": "Montag", "English": "Monday"},
        "Tuesday": {"Deutsch": "Dienstag", "English": "Tuesday"},
        "Wednesday": {"Deutsch": "Mittwoch", "English": "Wednesday"},
        "Thursday": {"Deutsch": "Donnerstag", "English": "Thursday"},
        "Friday": {"Deutsch": "Freitag", "English": "Friday"},
        "Saturday": {"Deutsch": "Samstag", "English": "Saturday"},
        "Sunday": {"Deutsch": "Sonntag", "English": "Sunday"},
        "Montag": {"Deutsch": "Montag", "English": "Monday"},
        "Dienstag": {"Deutsch": "Dienstag", "English": "Tuesday"},
        "Mittwoch": {"Deutsch": "Mittwoch", "English": "Wednesday"},
        "Donnerstag": {"Deutsch": "Donnerstag", "English": "Thursday"},
        "Freitag": {"Deutsch": "Freitag", "English": "Friday"},
        "Samstag": {"Deutsch": "Samstag", "English": "Saturday"},
        "Sonntag": {"Deutsch": "Sonntag", "English": "Sunday"},
        
        # unexpected events
        "holidayevent": {"Deutsch": "Feiertag - Laden geschlossen", "English": "Holiday - store closed"},
        "unexpEventConstruction": {"Deutsch": "Baustelle vorm Eingang", "English": "Construction site in front of store"},
        "unexpEventDemo": {"Deutsch": "Demonstration für Kuchenfreunde in der Nähe", "English": "Cake Lovers demonstration nearby"},
        "unexpEventFlea": {"Deutsch": "Flohmarkt in der Straße", "English": "Fleamarket on same street"},
        "unexpEventOffer": {"Deutsch": "Sonderangebot der Konkurrenz", "English": "Special offer at a competitor's store"},
        "unexpEventStrike": {"Deutsch": "Streik im öffentlichen Nahverkehr", "English": "Public transportation strike"},
        "unexpEventSportsGood": {"Deutsch": "Lokalmannschaft gewinnt Spiel", "English": "Local team wins match"},
        "unexpEventSportsBad": {"Deutsch": "Lokalmannschaft verliert Spiel", "English": "Local team loses match"},
        "unexpEventBirthday": {"Deutsch": "Großbestellung für Geburtstagsparty", "English": "Special order for a birthday"},
         
        # model infos
        "modelExplanation": {"Deutsch": "Erklärung für KI-Vorhersage", "English": "Explanation for AI prediction"},
        "noModelExplanationAvailable": {"Deutsch": "Noch keine Modellvorhersage für morgen angefordert", "English": "No model prediction for tomorrow to explain, yet"}, 
        "modelInfoHeuristic": {"Deutsch": "Beim heuristischen Vorhersageansatz wird das Muster ausgenutzt, dass gleiche Wochentage häufig ähnliche Verkaufszahlen aufweisen. Durch einen Blick auf die Verkäufe der zurückliegenden gleichen Wochentage ist eine Einschätzung der morgigen Verkäufe möglich. Die Heuristik berechnet den Mittelwert aus den letzten 4 selben Wochentagen und sagt diesen voraus. Diese Tage sind:", "English": "The heuristic forecasting approach takes advantage of the pattern that the same weekdays often show similar sales numbers. By looking at sales from past occurrences of the same weekday, it is possible to estimate tomorrow's sales. The heuristic calculates the average of the last four occurrences of the same weekday and uses that as the prediction. These days are:"},
        "modelInfoKNN": {"Deutsch": "Der k-nächste-Nachbarn-Algorithmus (k-NN) sucht in den historischen Verkaufsdaten nach vergangenen Tagen, die vorherzusagenden Tag am ähnlichsten sind. Dabei werden Faktoren wie Wochentag, Wetter und Feiertage berücksichtigt. Die vorhergesagte Verkaufszahl ist der Durchschnitt der Verkaufszahlen der ähnlichsten vergangenen Tage:", "English": "The k-nearest neighbors (k-NN) algorithm searches historical sales data for past days that are most similar to tomorrow. It takes into account factors such as weekday, weather, and special days. The predicted sales number is the average of the sales figures from the most similar past days:"},
        "modelInfoXGB": {"Deutsch": "XGBoost ist ein komplexes Machine-Learning-Modell, das Vorhersagen basierend auf Mustern in historischen Daten trifft. Im Gegensatz zu einfacheren Methoden liefert es keine leicht verständlichen Erklärungen für seine Prognosen.", "English": "XGBoost is a complex machine learning model that makes predictions based on patterns in historical data. Unlike simpler methods, it does not provide easily interpretable reasons for its predictions."},

    }
    return translations.get(text, {}).get(lang, text)
