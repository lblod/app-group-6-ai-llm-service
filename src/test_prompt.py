import requests
import json

# Define the URL for the Ollama API
url = "http://localhost:11434/api/generate"

# Function to reformulate and order information
def reformulate_information(data):
    title = data.get("title", "")
    description = data.get("description", "")
    requirements = data.get("requirementDescription", "")
    procedure = data.get("procedureDescription", "")
    
    prompt = f"""
    Given the following information in Dutch:
    
    -Title (is the name of the product or service): {title}
    -Description (is the description of the product or service): {description}
    -Requirements (pre-requisites, requirements or to whom is directed): {requirements}
    -Procedure (procedure or steps that the user should take or consider regarding the product or service): {procedure}
    
    Please reformulate the information in a way that is comprehensive considering that it is official governmental information for citizens. The output should also be in Dutch.
    Take into account the following points:

    1. Highlight the service or product related to the query based on the title, summarizing the description (if any) of that product or service.
    2. Mention the requirements or prerequisites (if any) related to the product or service using simple bullet points that are easy to follow. Note that you can find additional description points in the requirements. Pay attention to the information to present it clearly.
    3. Mention the procedure or steps (if any) that the user should consider or take. Note that the procedure is complementary to requirements and/or prerequisites and, in some cases, could not add additional relevant info. If no procedure is mentioned, state: "No additional procedure found"
    4. Try not to repeat information, and also spot relevant fields that can be mentioned separately based on the information, like to whom it is specifically directed, special notes, etc.
    5. You may find symbols or HTML links that are not relevant and should be avoided in the response/output. So, add relevant information, be careful if the information has no sense based on the context.
    6. Important: DO NOT ADD additional information if is not provided in the data. Avoid adding information that was not given, if there is no specific information that is relevant, better to mention that "There is no more relevant info".
    7. Important: the output should be in the Dutch language.

    This is an example:

    title = "Europese blauwe kaart voor hoogopgeleide vreemdelingen",
    description = "Hoogopgeleide buitenlanders kunnen onder bepaalde voorwaarden gedurende meer dan 90 dagen in Vlaanderen wonen en werken. In dat geval kan hun toekomstige werkgever een Europese blauwe kaart voor hen aanvragen..",
    requirement = "Europese blauwe kaart kan een werknemer die niet de nationaliteit van een lidstaat van de EER</a> of Zwitserland heeft, meer dan 90 dagen in België werken en verblijven. De regelgeving is de omzetting van de Europese Richtlijn (van 2009/50 van 25 mei 2009) voor de voorwaarden voor toegang en verblijf van onderdanen van derde landen met het oog op een hooggekwalificeerde baan."
    procedure = "De toekomstige werkgever vraagt de Europese blauwe kaart"

    An output for this data could be something like:

    "Europese blauwe kaart voor hoogopgeleide vreemdelingen.

    Dankzij deze dienst kunnen hoogopgeleide buitenlanders onder bepaalde voorwaarden langer dan 90 dagen in Vlaanderen wonen en werken. Je toekomstige werkgever kan dit aanvragen.

    Doelgroep / Vereisten:

    - Buitenlandse werknemer die lid is van de EER of Zwitserland.

    Procedure:

    - De toekomstige werkgever moet de Europese blauwe kaart aanvragen.

    Andere relevante informatie:

    De verordening is de omzetting van de Europese richtlijn (van 2009/50 van 25 mei 2009) betreffende de voorwaarden voor toegang en verblijf van onderdanen van derde landen met het oog op een hooggekwalificeerde baan."

    """

    payload = {
        "model": "llama3.2",  # Ensure this is the correct model name
        "prompt": prompt,
        "parameters": {
            "temperature": 0.0
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, stream=True)

    full_response = ""  # Initialize an empty string to store the complete response

    for chunk in response.iter_lines():
        if chunk:
            try:
                decoded_chunk = chunk.decode('utf-8')
                json_response = json.loads(decoded_chunk)
                full_response += json_response.get("response", "")  # Extract and append the 'response' field
            except json.decoder.JSONDecodeError as e:
                print("Failed to decode JSON:", e)

    return full_response

# Example JSON data
json_data = '''
[
    {
        "title": "Aanvraag vergunning Autovrij Gebied",
        "description": "Een bouwvergunning is vereist voor het bouwen of verbouwen van een woning of ander gebouw.",
        "requirementDescription": "1. Volledig ingevuld aanvraagformulier. 2. Bouwtekeningen en plannen. 3. Betaling van de aanvraagkosten.",
        "procedureDescription": "1. Verzamel alle vereiste documenten. 2. Dien de aanvraag in bij de gemeente. 3. Wacht op goedkeuring van de gemeente."
    }
]
'''

# Parse the JSON data
data_list = json.loads(json_data)

# Process each data set
for data in data_list:
    result = reformulate_information(data)
    print(result)
