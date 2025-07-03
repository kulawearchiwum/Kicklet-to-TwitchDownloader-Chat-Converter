# Kicklet-to-TwitchDownloader-Chat-Converter
Kicklet to TwitchDownloader Chat Converter

# Kicklet to TwitchDownloader Chat Converter

A simple Python GUI tool created by **KulaweArchiwum** to convert Kicklet.app chat JSON files (which lack timestamps formatted for TwitchDownloader) into a fully compatible TwitchDownloader chat renderer JSON format.

## Features

- Converts Kicklet chat JSON into TwitchDownloader-compatible JSON format.
- Allows entering the stream's **start time** and **duration** to correctly calculate timestamps and message offsets.
- User-friendly GUI with file selector and input fields for time data.
- Outputs a JSON file ready to use with TwitchDownloader chat renderer.
- Minimal dependencies; uses Python’s built-in `tkinter` and `json`.

## Usage

1. Run the GUI script.
2. Select your Kicklet chat JSON file.
3. Enter the stream start time in ISO format, e.g. `2025-07-01T19:02:55`.
4. Enter the stream duration in seconds (e.g., `25837` for 7h10m37s).
5. Click Convert and save the output file.

## Format Explanation

- **Stream Start Time**: The exact starting time of the stream in ISO format.
- **Stream Duration**: Length of the stream in seconds.
  
These inputs help convert the chat timestamps properly to sync with the VOD.

## License

This project is licensed under the MIT License — free for anyone to use, modify, and distribute.

---

Created by **KulaweArchiwum**
