YTS Movie Downloader Help

This script downloads 1080p torrent files of animation movies from YTS.

Setup and Usage:

1. Save the Python script (f1.py), requirements.txt, setup_and_run.bat, and this help.txt file in the same directory.
2. Double-click the setup_and_run.bat file.

The batch script will:

* Check if Python is installed.
* Create a virtual environment (if it doesn't exist).
* Activate the virtual environment.
* Install the required Python packages (requests, beautifulsoup4).
* Run the f1.py script.
* (Optionally) Deactivate the virtual environment.

Torrent files will be downloaded to a "movies" folder created in the same directory as the script.

Troubleshooting:

* If you encounter errors, make sure you have a stable internet connection.
* Check if the YTS website structure has changed, as this might require updates to the f1.py script.
* If you get a "Python is not installed" message, download and install Python from https://www.python.org/downloads/
* If you get a "venv is not available message" you have an older version of python install a newer version 3.3 or higher.
