import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def google_search(query, num_results=3):
    """
    Performs a Google search and returns top results.
    Returns formatted search results.
    """
    try:
        # Use DuckDuckGo instant answer API as fallback (more reliable)
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        result = f"Search results for '{query}':\n\n"
        
        # Get abstract if available
        if data.get('Abstract'):
            result += f"📌 {data['Abstract']}\n\n"
        
        # Get related topics
        if data.get('RelatedTopics'):
            result += "Related information:\n"
            for i, topic in enumerate(data['RelatedTopics'][:num_results], 1):
                if isinstance(topic, dict) and 'Text' in topic:
                    result += f"{i}. {topic['Text']}\n"
        
        if len(result.strip()) <= len(f"Search results for '{query}':\n\n"):
            result = f"Search completed for '{query}'. Try asking me to search Wikipedia for more detailed information."
        
        return result
    except Exception as e:
        return f"Error searching: {e}"

def wikipedia_query(topic):
    """
    Searches Wikipedia and returns a summary.
    Returns Wikipedia summary or error message.
    """
    try:
        # Wikipedia API
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            title = data.get('title', topic)
            extract = data.get('extract', 'No summary available.')
            
            result = f"📖 {title}\n\n{extract}"
            
            # Limit length for voice output
            if len(result) > 500:
                result = result[:500] + "... (summary truncated)"
            
            return result
        else:
            return f"Could not find Wikipedia article for '{topic}'"
    except Exception as e:
        return f"Error querying Wikipedia: {e}"

def get_weather(city):
    """
    Gets current weather for a city using wttr.in service.
    Returns weather information.
    """
    try:
        # wttr.in is a free weather service
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            temp_c = current['temp_C']
            temp_f = current['temp_F']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind_speed = current['windspeedKmph']
            
            result = f"🌤️ Weather in {city}:\n"
            result += f"Temperature: {temp_c}°C ({temp_f}°F)\n"
            result += f"Condition: {desc}\n"
            result += f"Humidity: {humidity}%\n"
            result += f"Wind Speed: {wind_speed} km/h"
            
            return result
        else:
            return f"Could not get weather for '{city}'"
    except Exception as e:
        return f"Error getting weather: {e}"

def get_news(category="general", country="us", num_articles=5):
    """
    Gets latest news headlines.
    Note: For production, you'd want to use a proper news API with an API key.
    This is a simplified version.
    """
    try:
        # Using gnews.io free tier (no auth required for limited requests)
        url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country={country}&max={num_articles}&apikey=demo"
        
        # Note: 'demo' key is limited. For production, get a free API key from gnews.io
        # Or use another news API
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            if not articles:
                return "No news articles found."
            
            result = f"📰 Latest {category} news:\n\n"
            for i, article in enumerate(articles, 1):
                title = article.get('title', 'No title')
                result += f"{i}. {title}\n"
            
            return result
        else:
            # Fallback message
            return "News service temporarily unavailable. Please try again later or visit a news website."
    except Exception as e:
        return f"Error getting news: {e}"

def define_word(word):
    """
    Gets definition of a word using Free Dictionary API.
    Returns definition or error message.
    """
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and len(data) > 0:
                entry = data[0]
                word_text = entry.get('word', word)
                
                # Get first meaning
                if entry.get('meanings') and len(entry['meanings']) > 0:
                    meaning = entry['meanings'][0]
                    part_of_speech = meaning.get('partOfSpeech', '')
                    
                    if meaning.get('definitions') and len(meaning['definitions']) > 0:
                        definition = meaning['definitions'][0].get('definition', '')
                        example = meaning['definitions'][0].get('example', '')
                        
                        result = f"📖 {word_text}"
                        if part_of_speech:
                            result += f" ({part_of_speech})"
                        result += f"\n\n{definition}"
                        if example:
                            result += f"\n\nExample: {example}"
                        
                        return result
            
            return f"No definition found for '{word}'"
        else:
            return f"Word '{word}' not found in dictionary"
    except Exception as e:
        return f"Error looking up definition: {e}"

def get_quick_fact(query):
    """
    Gets a quick fact or answer using DuckDuckGo instant answers.
    Returns instant answer or redirects to other search.
    """
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # Try different fields
        if data.get('Answer'):
            return f"💡 {data['Answer']}"
        elif data.get('AbstractText'):
            return f"💡 {data['AbstractText']}"
        elif data.get('Definition'):
            return f"💡 {data['Definition']}"
        else:
            return f"No quick answer found. Try searching Wikipedia for '{query}' instead."
    except Exception as e:
        return f"Error getting fact: {e}"
