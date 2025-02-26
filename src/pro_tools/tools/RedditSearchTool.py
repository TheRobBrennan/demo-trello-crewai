import os
from typing import Type, Dict, Any, List, Optional
import json
import requests

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr


class SerpApiSearchToolInput(BaseModel):
    query: str = Field(..., description="The query to search the web for.")
    max_results: int = Field(3, description="The maximum number of results to return.")


class RedditSerpApiSearchTool(BaseTool):
    name: str = "Reddit Search Tool"
    description: str = "Search Reddit and the web for information"
    args_schema: Type[BaseModel] = SerpApiSearchToolInput
    _api_key: str = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._api_key = os.getenv("SERPAPI_API_KEY")
        if not self._api_key:
            print("Warning: SERPAPI_API_KEY environment variable not set. Search will return placeholder results.")

    def _run(self, query: str, max_results: int = 3) -> str:
        if not self._api_key:
            return self._get_placeholder_results(query)
        
        try:
            return self._search_with_serpapi(query, max_results)
        except Exception as e:
            print(f"Error using SerpApi: {str(e)}")
            return self._get_placeholder_results(query)

    def _search_with_serpapi(self, query: str, max_results: int) -> str:
        # Base URL for SerpApi
        base_url = "https://serpapi.com/search"
        
        # Parameters for the search
        params = {
            "api_key": self._api_key,
            "q": query,
            "engine": "google",
            "num": max_results
        }
        
        # Make the request
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # Parse the response
        results = response.json()
        
        # Format the results
        formatted_results = self._format_results(results, max_results)
        
        return formatted_results

    def _format_results(self, results: Dict[str, Any], max_results: int) -> str:
        if "organic_results" not in results or not results["organic_results"]:
            return "No results found."
        
        organic_results = results["organic_results"][:max_results]
        
        formatted_text = f"Search results for: {results.get('search_parameters', {}).get('q', 'Unknown query')}\n\n"
        
        for i, result in enumerate(organic_results, 1):
            title = result.get("title", "No title")
            link = result.get("link", "No link")
            snippet = result.get("snippet", "No description")
            
            formatted_text += f"{i}. {title}\n"
            formatted_text += f"   URL: {link}\n"
            formatted_text += f"   Description: {snippet}\n\n"
        
        return formatted_text

    def _get_placeholder_results(self, query: str) -> str:
        return f"[Placeholder] Research results for query: {query}\n\n" + \
               "1. SerpApi API key not configured. Please set the SERPAPI_API_KEY environment variable.\n" + \
               "2. The core Trello functionality remains operational.\n" + \
               "3. For actual research results, please configure a valid SerpApi API key."
