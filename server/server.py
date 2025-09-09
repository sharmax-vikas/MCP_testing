# weather_server.py
from fastmcp import FastMCP
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv('API_KEY')
mcp = FastMCP("Real Weather Server")

@mcp.tool
def get_weather(city: str) -> dict:
    """Get real current weather for a city"""
    
    try:
        url = "https://weather-api167.p.rapidapi.com/api/weather/current"

        querystring = {"lat":"0","place":f"{city},IN","units":"standard","lang":"en","mode":"json"}

        headers = {
            "x-rapidapi-key": "c62ac3f3c4msh82617baf453783ap1dc2b3jsn69388b15ee85",
            "x-rapidapi-host": "weather-api167.p.rapidapi.com",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        return data
                    
    except Exception as e:
        return {"error": f"Failed to get weather: {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8000)