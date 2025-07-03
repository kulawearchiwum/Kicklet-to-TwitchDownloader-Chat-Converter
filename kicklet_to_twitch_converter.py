import json
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import random

def random_color():
    # Generate a random hex color
    return "#%06x" % random.randint(0, 0xFFFFFF)

def convert_kick_to_twitch(kick_data, stream_start_iso, stream_duration_seconds):
    twitch_comments = []
    try:
        stream_start = datetime.fromisoformat(stream_start_iso.replace("Z", "+00:00"))
    except Exception as e:
        raise ValueError(f"Invalid stream start time format: {e}")

    for i, msg in enumerate(kick_data):
        try:
            # Parse message timestamp
            created_at = datetime.fromisoformat(msg.get("createdAt").replace("Z", "+00:00"))
            # Calculate offset in seconds from stream start
            offset = (created_at - stream_start).total_seconds()
            # Clamp offset to stream duration range
            if offset < 0: 
                offset = 0
            elif offset > stream_duration_seconds:
                offset = stream_duration_seconds

            comment = {
                "_id": f"kick_{i:06}",
                "created_at": msg.get("createdAt"),
                "content_offset_seconds": int(offset),
                "commenter": {
                    "display_name": msg.get("username", ""),
                    "name": msg.get("username", "")
                },
                "message": {
                    "body": msg.get("content", ""),
                    "fragments": [
                        {
                            "text": msg.get("content", ""),
                            "emoticon": None
                        }
                    ],
                    "user_badges": [],
                    "user_color": random_color(),
                    "emoticons": []
                }
            }
            twitch_comments.append(comment)
        except Exception as e:
            print(f"Error processing message #{i}: {e}")
    return twitch_comments

def load_and_convert():
    input_path = filedialog.askopenfilename(title="Select Kick Chat JSON File", filetypes=[("JSON Files", "*.json")])
    if not input_path:
        return

    stream_start_iso = entry_start.get().strip()
    duration_str = entry_duration.get().strip()

    if not stream_start_iso or not duration_str:
        messagebox.showerror("Error", "Please enter both stream start time and stream duration.")
        return

    try:
        h, m, s = map(int, duration_str.split(":"))
        stream_duration_seconds = h * 3600 + m * 60 + s
    except Exception:
        messagebox.showerror("Error", "Invalid duration format. Use HH:MM:SS.")
        return

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            kick_data = json.load(f)

        twitch_data = {
            "FileInfo": {
                "Version": {"Major": 1, "Minor": 4, "Patch": 0},
                "CreatedAt": datetime.utcnow().isoformat() + "Z",
                "UpdatedAt": "0001-01-01T00:00:00"
            },
            "streamer": {"name": "KulaweArchiwum", "login": "KulaweArchiwum", "id": 0},
            "clipper": None,
            "video": {
                "title": "Kick stream export",
                "id": "kick_generated_001",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "start": 0,
                "end": stream_duration_seconds,
                "length": stream_duration_seconds,
                "viewCount": 0,
                "game": "Just Chatting",
                "chapters": []
            },
            "comments": convert_kick_to_twitch(kick_data, stream_start_iso, stream_duration_seconds)
        }

        output_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")], title="Save Converted File As")
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(twitch_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Success", f"Conversion complete! File saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

root = tk.Tk()
root.title("Kick → Twitch Chat JSON Converter")
root.geometry("480x260")
root.resizable(False, False)

tk.Label(root, text="Convert Kick chat to TwitchDownloader format", font=("Arial", 12)).pack(pady=10)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=5)

tk.Label(frame_inputs, text="Stream Start Time (ISO 8601):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_start = tk.Entry(frame_inputs, width=30)
entry_start.grid(row=0, column=1, padx=5, pady=5)
entry_start.insert(0, "2025-07-01T19:02:55Z")

tk.Label(frame_inputs, text="Stream Duration (HH:MM:SS):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_duration = tk.Entry(frame_inputs, width=30)
entry_duration.grid(row=1, column=1, padx=5, pady=5)
entry_duration.insert(0, "07:10:37")

btn_convert = tk.Button(root, text="Select Kick Chat JSON and Convert", font=("Arial", 11), command=load_and_convert)
btn_convert.pack(pady=20)

root.mainloop()
