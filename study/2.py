import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

def get_movie_links(url: str) -> Optional[List[str]]:
    """
    Retrieves all unique movie links from a given URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        Optional[List[str]]: A list of unique movie links, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.startswith("https://yts.mx/movies/"):
                links.append(href)
        return list(set(links))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_movie_details(url: str) -> Optional[Dict[str, str]]:
    """
    Fetches movie details from a YTS movie page URL.

    Args:
        url (str): The URL of the YTS movie page.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing movie details, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        title_tag = soup.find("h1", class_="title")
        title = title_tag.text.strip() if title_tag else None

        download_link = None
        download_section = soup.find("p", class_="hidden-md hidden-lg")
        if download_section:
            for link in download_section.find_all("a", rel="nofollow"):
                href = link.get("href")
                if href and href.startswith("https://yts.mx/torrent/download/"):
                    resolution = link.text.strip().split(".")[0]
                    if resolution.lower() == "1080p":
                        download_link = href
                        break

        return {"title": title, "download_link": download_link}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # URL for the movie listing page
    browse_url = "https://yts.mx/browse-movies/0/all/animation/0/downloads/0/all"
    
    # Get all unique movie links
    print("Fetching movie links...")
    movie_links = get_movie_links(browse_url)
    
    if not movie_links:
        print("No movie links found.")
        return

    print(f"Found {len(movie_links)} unique movies. Fetching details...\n")
    
    # Process each movie link
    for index, movie_url in enumerate(movie_links, 1):
        print(f"Processing movie {index}/{len(movie_links)}: {movie_url}")
        
        movie_details = get_movie_details(movie_url)
        if movie_details:
            title = movie_details["title"]
            download_link = movie_details["download_link"]

            if title:
                print(f"Title: {title}")
            if download_link:
                print(f"1080p Download Link: {download_link}")
            else:
                print("1080p download link not found.")
        else:
            print("Could not retrieve movie details.")
        print("-" * 80)  # Separator line

if __name__ == "__main__":
    main()