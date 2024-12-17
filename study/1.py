import requests
from bs4 import BeautifulSoup

def get_movie_details(url):
    """
    Fetches movie details from a YTS movie page URL.

    Args:
        url (str): The URL of the YTS movie page.

    Returns:
        dict: A dictionary containing movie details (e.g., title, download link), 
              or None if an error occurs.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract movie title (example)
        title_tag = soup.find("h1", class_="title")
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = None

        # Extract download link (assuming only one 1080p link)
        download_link = None
        download_section = soup.find("p", class_="hidden-md hidden-lg")
        if download_section:
            for link in download_section.find_all("a", rel="nofollow"):
                href = link.get("href")
                if href and href.startswith("https://yts.mx/torrent/download/"):
                    resolution = link.text.strip().split(".")[0]
                    if resolution.lower() == "1080p":  # Check for lowercase "1080p"
                        download_link = href
                        break  # Exit the loop after finding the first 1080p link

        return {"title": title, "download_link": download_link}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    movie_url = "https://yts.mx/movies/the-lion-king-2019"
    movie_details = get_movie_details(movie_url)

    if movie_details:
        title = movie_details["title"]
        download_link = movie_details["download_link"]

        if title:
            print(f"Movie Title: {title}")

        if download_link:
            print("1080p Download Link:", download_link)
        else:
            print("1080p download link not found.")
    else:
        print("Could not retrieve movie details.")