import requests

def search_web(query):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "AbstractText" in data and data["AbstractText"]:
        return data["AbstractText"]
    else:
        return "No relevant web results found."