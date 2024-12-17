import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
from typing import Dict, List, Optional
import time

def get_movie_links(url: str) -> Optional[List[str]]:
    """Retrieves all unique movie links from a given URL."""
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
    except Exception as e:
        print(f"Error fetching links: {e}")
        return None

def get_movie_details(url: str) -> Optional[Dict[str, str]]:
    """Fetches movie details and download link."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Try multiple ways to find the title
        title = None
        
        # Method 1: Try finding h1 with class title
        title_tag = soup.find("h1", class_="title")
        if title_tag:
            title = title_tag.text.strip()
        
        # Method 2: Try extracting from the URL if title not found
        if not title:
            title_from_url = url.split('/')[-1].replace('-', ' ')
            # Extract year if present
            if title_from_url:
                parts = title_from_url.split()
                if parts[-1].isdigit() and len(parts[-1]) == 4:  # If last part is a 4-digit year
                    year = parts[-1]
                    name = ' '.join(parts[:-1])
                    title = f"{name.title()} ({year})"  # Capitalize each word
                else:
                    title = title_from_url.title()

        # Try to find the download link
        download_link = None
        for link in soup.find_all("a", rel="nofollow"):
            href = link.get("href")
            if href and href.startswith("https://yts.mx/torrent/download/"):
                text = link.text.strip()
                if "1080p" in text.lower():
                    download_link = href
                    break

        return {"title": title, "download_link": download_link}
    except Exception as e:
        print(f"Error fetching details: {e}")
        return None

def download_torrent(url: str, title: str, download_folder: Path) -> bool:
    """Downloads a torrent file to the specified folder."""
    try:
        # Create safe filename from title
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_', '(', ')')).strip()
        filename = f"{safe_title}.torrent"
        filepath = download_folder / filename

        # Check if file already exists
        if filepath.exists():
            print(f"File already exists: {filename}")
            return True

        # Download the file with progress indicator
        print(f"\nDownloading: {filename}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for data in response.iter_content(chunk_size=4096):
                    downloaded += len(data)
                    f.write(data)
                    progress = int(50 * downloaded / total_size)
                    print(f"\rProgress: [{'=' * progress}{' ' * (50-progress)}] {downloaded}/{total_size} bytes", 
                          end='', flush=True)
        
        print(f"\nSaved to: {filepath}")
        return True

    except Exception as e:
        print(f"Error downloading {title}: {e}")
        return False

def main():
    # Set up movies folder in current working directory
    current_dir = Path.cwd()  # Get current working directory
    downloads_folder = current_dir / "movies"
    downloads_folder.mkdir(exist_ok=True)
    
    print(f"Files will be saved to: {downloads_folder}")
    
    # URL for the movie listing page
    browse_url = "https://yts.mx/browse-movies/0/all/animation/0/downloads/0/all"
    
    print("Fetching movie links...")
    movie_links = get_movie_links(browse_url)
    
    if not movie_links:
        print("No movie links found.")
        return

    print(f"Found {len(movie_links)} movies. Starting downloads...\n")
    
    # Process each movie
    for index, movie_url in enumerate(movie_links, 1):
        print(f"\nProcessing movie {index}/{len(movie_links)}")
        print(f"URL: {movie_url}")
        
        movie_details = get_movie_details(movie_url)
        if not movie_details:
            continue
            
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
        
        # Add a small delay between downloads
        time.sleep(1)
        print("-" * 80)

if __name__ == "__main__":
    main()