import requests
import json


url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama3.2",  # Make sure this is the correct model name
    "prompt": "Do you know Dutch language?",
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
            # print(json_response)  # Print the entire JSON response
            full_response += json_response.get("response", "")  # Extract and append the 'response' field
        except json.decoder.JSONDecodeError as e:
            print("Failed to decode JSON:", e)

print(full_response)  # Print the concatenated response
