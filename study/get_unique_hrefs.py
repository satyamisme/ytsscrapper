import requests
from bs4 import BeautifulSoup

def get_movie_links(url):
    """
    Retrieves all unique movie links (`href` attributes) starting with 
    "https://yts.mx/movies/" from a given URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        list: A list of unique movie links, or None if an error occurs.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes

        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.startswith("https://yts.mx/movies/"):  # Filter by movie link pattern
                links.append(href)
        return list(set(links))  # Remove duplicates

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    url = "https://yts.mx/browse-movies/0/all/animation/0/downloads/0/all"  # Replace with the desired URL
    movie_links = get_movie_links(url)

    if movie_links:
        for link in movie_links:
            print(link)
    else:
        print("Could not retrieve movie links.")