import requests
from bs4 import BeautifulSoup
import os

def get_movie_details(url):
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
                if href and href.startswith("https://yts.mx/movies/"):
                    resolution = link.text.strip().split(".")[0].lower()
                    if resolution == "1080p":
                        download_link = href
                        break
        return {"title": title, "download_link": download_link}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def download_file(url, filename, download_folder="downloads"):
    os.makedirs(download_folder, exist_ok=True)
    filepath = os.path.join(download_folder, filename)
    if os.path.exists(filepath):
        print(f"File '{filename}' already exists. Skipping download.")
        return
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded '{filename}' successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading '{filename}': {e}")

if __name__ == "__main__":
    movie_url = "https://yts.mx/movies/the-lion-king-2019"
    movie_details = get_movie_details(movie_url)

    if movie_details:
        title = movie_details["title"]
        download_link = movie_details["download_link"]

        if title and download_link:
            print(f"Movie Title: {title}")
            print("1080p Download Link:", download_link)
            filename = download_link.split("/")[-1]
            download_file(download_link, filename)
        elif not download_link:
            print("1080p download link not found.")
    else:
        print("Could not retrieve movie details.")