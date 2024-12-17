import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
from typing import Dict, List, Optional
import time
import re

def get_movie_links(url: str) -> Optional[List[str]]:
    """Retrieves all unique movie links from a given URL."""
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)  # Allow redirects, add timeout
        response.raise_for_status()
        print(f"Fetched URL: {response.url}") # Print the fetched URL for debugging
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.startswith("https://yts.mx/movies/"):
                links.append(href)
        return list(set(links))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching links: {e}")
        return None
    except Exception as e:
        print(f"A general error occurred during link fetching: {e}")
        return None

def get_movie_details(url: str) -> Optional[Dict[str, str]]:
    """Fetches movie details and 1080p download link."""
    try:
        response = requests.get(url, timeout=10)  # Add timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        title = None
        title_tag = soup.find("h1", class_="title")
        if title_tag:
            title = title_tag.text.strip()
        if not title:
            try:
                title = re.search(r"/movies/([^/]+)$", url).group(1).replace("-", " ").title()
            except AttributeError:
                print(f"Could not extract title from URL: {url}")
                return None

        download_link = None
        download_section = soup.find("p", class_="hidden-md hidden-lg")
        if download_section:
            for link in download_section.find_all("a", rel="nofollow"):
                href = link.get("href")
                if href and href.startswith("https://yts.mx/torrent/download/"):
                    text = link.text.strip().lower()
                    if "1080p" in text:
                        download_link = href
                        break
        return {"title": title, "download_link": download_link}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details: {e}")
        return None
    except Exception as e:
        print(f"A general error occurred during movie detail fetching: {e}")
        return None

def download_torrent(url: str, title: str, download_folder: Path) -> bool:
    """Downloads a torrent file."""
    try:
        safe_title = re.sub(r"[^a-zA-Z0-9\s_\-\(\)]", "", title).strip()
        filename = f"{safe_title}.torrent"
        filepath = download_folder / filename

        if filepath.exists():
            print(f"File already exists: {filename}")
            return True

        print(f"\nDownloading: {filename}")
        response = requests.get(url, stream=True, timeout=30)  # Add timeout
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filepath, 'wb') as f:
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)
                f.write(data)
                if total_size != 0:
                    progress = int(50 * downloaded / total_size)
                    print(f"\rProgress: [{'=' * progress}{' ' * (50-progress)}] {downloaded}/{total_size} bytes", end='', flush=True)

        print(f"\nSaved to: {filepath}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error during download: {e}")
        return False
    except Exception as e:
        print(f"A general error occurred during download: {e}")
        return False

def main():
    current_dir = Path.cwd()
    downloads_folder = current_dir / "movies"
    downloads_folder.mkdir(exist_ok=True)
    print(f"Files will be saved to: {downloads_folder}")

    base_browse_url = "https://yts.mx/browse-movies/0/all/animation/0/downloads/0/all"
    all_movie_links = set()
    page = 1

    while True:
        browse_url = f"{base_browse_url}" if page == 1 else f"{base_browse_url}?page={page}" # Correct page construction
        print(f"\nFetching movie links from: {browse_url}") # Print the constructed URL
        movie_links = get_movie_links(browse_url)

        if not movie_links:
            print("No movie links found on this page or error occurred. Stopping.")
            break

        new_links = set(movie_links) - all_movie_links
        if not new_links:
            print("No *new* movie links found on this page. Stopping.")
            break

        all_movie_links.update(new_links)
        print(f"Found {len(new_links)} *new* movies on page {page}.")

        for movie_url in new_links:
            print(f"\nProcessing movie: {movie_url}")
            movie_details = get_movie_details(movie_url)
            if movie_details:
                title = movie_details["title"]
                download_link = movie_details["download_link"]
                if title and download_link:
                    print(f"Title: {title}")
                    success = download_torrent(download_link, title, downloads_folder)
                    if success:
                        print("Download completed successfully")
                    else:
                        print("Download failed")
                else:
                    print("Missing title or download link")
            time.sleep(1)
            print("-" * 80)

        page += 1
        time.sleep(2)  # Delay between page requests

    print("\nFinished processing all pages.")

if __name__ == "__main__":
    main()