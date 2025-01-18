import requests
import json

class GoogleSearchService:
    """
    Handles Google search functionality using Google Custom Search JSON API.
    """

    def __init__(self, api_key: str = None, cx: str = None):
        """
        Initialize the GoogleSearchService with API key and CX ID.
        """
        # API key and Custom Search Engine ID
        self.GOOGLE_API_KEY = api_key
        self.CX = cx
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search_google(self, query: str, num_results: int = 5):
        """
        Perform a Google search and return the top results.

        :param query: The search query.
        :param num_results: Number of results to return.
        :return: A list of search results or an error message.
        """
        if not query:
            return {"error": "Query parameter is required"}, 400

        # Construct the API request URL
        url = f'{self.base_url}?q={query}&key={self.GOOGLE_API_KEY}&cx={self.CX}&num={num_results}'

        try:
            # Perform the HTTP request
            response = requests.get(url)

            # Check if the response status code is 200 (success)
            if response.status_code != 200:
                return {"error": "Failed to fetch search results"}, response.status_code

            # Extract the results from the response JSON
            results = response.json().get("items", [])
            print(json.dumps(results, indent=4))

            search_results = [
                {"title": item["title"], "link": item["link"]}
                for item in results
            ]
            return search_results, 200

        except Exception as e:
            # Handle any exceptions
            return {"error": f"Error performing Google search: {e}"}, 500


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    # Load API key and search engine ID from environment variables
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    cx = os.getenv("GOOGLE_SEARCH_CX_ID")

    gs = GoogleSearchService(api_key, cx)
    query = "What is the meaning of life?"
    results, status_code = gs.search_google(query, num_results=1)

    if status_code == 200:
        print("Search Results:", results)
    else:
        print("Error:", results)