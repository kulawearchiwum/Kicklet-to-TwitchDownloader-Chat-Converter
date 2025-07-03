


<p align="center">
  <img src="https://raw.githubusercontent.com/lay295/TwitchDownloader/master/TwitchDownloaderWPF/Images/Logo.png" alt="TwitchDownloader Logo" width="80" />
  <span style="font-size: 24px; font-weight: bold; margin: 0 15px;">X</span>
  <img src="https://kicklet.app/img/logo.87ab9afc.png" alt="Kicklet Logo" width="80" />
</p>



# Kicklet to TwitchDownloader Chat Converter

This tool converts chat JSON files downloaded from [kicklet.app](https://kicklet.app) into a format compatible with the [TwitchDownloader](https://github.com/lay295/TwitchDownloader) chat renderer.

## Features

- Converts Kicklet chat JSON into TwitchDownloader-compatible JSON format.
- Allows setting stream start time and duration for accurate timestamp alignment.
- Randomizes username colors for better chat visualization.
- Simple GUI built with Python and Tkinter.
- Outputs fully compatible chat files for TwitchDownloader.

## Usage

1. Run the GUI application.
2. Load your Kicklet JSON chat file.
3. Enter the stream's first message time in ISO 8601 format (e.g. `2025-07-01T17:02:27Z`).
4. Enter the stream duration in HH:MM:SS (e.g. `07:10:37` for 7 hours, 10 minutes, and 37 seconds).
5. Convert and save the TwitchDownloader-compatible chat JSON file.
6. Load the resulting chat file into TwitchDownloader’s chat renderer for viewing.

## Installation

- Requires Python 3.x.
- No external dependencies (uses built-in `tkinter` and `json` modules).

## License

This project is licensed under the [MIT License](LICENSE).  
Created by KulaweArchiwum.

## References

- TwitchDownloader: https://github.com/lay295/TwitchDownloader  
- Kicklet: https://kicklet.app

---
