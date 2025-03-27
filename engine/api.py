import requests

def get_joke():
    """Fetch a random joke from JokeAPI, excluding adult content."""
    url = "https://v2.jokeapi.dev/joke/Any"
    params = {
        'type': 'single',             # 'single' for a one-liner joke
        'blacklistFlags': 'nsfw,racist,sexist,explicit',  # Filter out adult and inappropriate content
        'lang': 'en'                  # Language (English)
    }
    response = requests.get(url, params=params)
    joke_data = response.json()
    
    if joke_data['type'] == 'single':
        return joke_data['joke']
    else:
        return "Could not retrieve a joke at this time."

def get_news(api_key, query='latest'):
    """Fetches news headlines based on the query using World News API."""
    try:
        base_url = f"https://api.worldnewsapi.com/search-news?text={query}&api-key={api_key}"
        response = requests.get(base_url)

        # Debugging logs
        print(f"API Response Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            
            # Print full API response for debugging
            print("Full API Response:", data)

            # Check if the expected key exists in the JSON response
            if "news" in data and isinstance(data["news"], list):
                articles = data["news"]
                
                if articles:
                    # Extract top 3 headlines with descriptions
                    headlines = [f"{article['title']}: {article.get('text', 'No description available.')}" for article in articles[:3]]
                    news_summary = " ".join(headlines)

                    # Limit the summary to 2-3 sentences
                    sentences = news_summary.split('.')
                    limited_summary = '. '.join(sentences[:3]) + '.'

                    return f"Here are some headlines about {query}: {limited_summary}"
                else:
                    return f"No news articles found about {query}."
            else:
                return "Unexpected API response format. Check the 'news' key in response."
        else:
            return f"Error: Unable to fetch news data. Status Code: {response.status_code}, Response: {response.text}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_weather(city, api_key):
    """Fetches weather information for a specific city using Weatherstack API."""
    try:
        base_url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
        response = requests.get(base_url)
        print(f"API Response Status Code: {response.status_code}")  # Debug statement
        print(f"API Response Text: {response.text}")  # Debug statement

        if response.status_code == 200:
            data = response.json()
            current = data['current']
            temperature = current['temperature']
            weather_description = current['weather_descriptions'][0]  # List of descriptions
            humidity = current['humidity']
            wind_speed = current['wind_speed']

            weather_report = (f"The weather in {city} is currently {weather_description}, "
                              f"with a temperature of {temperature}°C, "
                              f"humidity at {humidity}%, "
                              f"and wind speed of {wind_speed} km/h.")
            return weather_report
        else:
            return f"Error: {data.get('error', {}).get('info', 'Unable to fetch weather data')}"
    except Exception as e:
        return f"An error occurred: {str(e)}"