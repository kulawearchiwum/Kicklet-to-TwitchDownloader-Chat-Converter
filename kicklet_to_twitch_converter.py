import json
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta

def parse_iso_datetime(iso_str):
    try:
        return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    except Exception:
        return None

def convert_kick_to_twitch(kick_data, start_time, duration_seconds):
    twitch_comments = []
    for msg in kick_data:
        created_at_str = msg.get("createdAt")
        created_at = parse_iso_datetime(created_at_str)
        if not created_at:
            # If timestamp invalid, fallback to None
            offset_seconds = None
        else:
            offset = created_at - start_time
            offset_seconds = max(0, int(offset.total_seconds()))

        # Clip offset to stream duration to avoid going past the end
        if offset_seconds is not None and offset_seconds > duration_seconds:
            # Skip messages past duration
            continue

        comment = {
            "_id": f"kick_{len(twitch_comments):06}",
            "created_at": created_at_str,
            "content_offset_seconds": offset_seconds if offset_seconds is not None else 0,
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
                "user_color": "#FFFFFF",
                "emoticons": []
            }
        }
        twitch_comments.append(comment)
    return twitch_comments

def load_and_convert():
    input_path = filedialog.askopenfilename(
        title="Select Kick Chat JSON File",
        filetypes=[("JSON Files", "*.json")]
    )
    if not input_path:
        return

    start_time_str = start_time_entry.get().strip()
    duration_str = duration_entry.get().strip()

    if not start_time_str:
        messagebox.showerror("Error", "Please enter the Stream Start Time in ISO format (e.g. 2025-07-01T19:02:55Z)")
        return
    if not duration_str.isdigit():
        messagebox.showerror("Error", "Please enter the Stream Duration in seconds (e.g. 25200 for 7 hours)")
        return

    start_time = parse_iso_datetime(start_time_str)
    if not start_time:
        messagebox.showerror("Error", "Stream Start Time is not a valid ISO datetime.")
        return

    duration_seconds = int(duration_str)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            kick_data = json.load(f)

        twitch_data = {
            "FileInfo": {
                "Version": {"Major": 1, "Minor": 4, "Patch": 0},
                "CreatedAt": datetime.utcnow().isoformat() + "Z",
                "UpdatedAt": "0001-01-01T00:00:00"
            },
            "streamer": {"name": "REPLACE_ME", "login": "REPLACE_ME", "id": 0},
            "clipper": None,
            "video": {
                "title": "Kick stream export",
                "id": "kick_generated_001",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "start": 0,
                "end": duration_seconds,
                "length": duration_seconds,
                "viewCount": 0,
                "game": "Just Chatting",
                "chapters": []
            },
            "comments": convert_kick_to_twitch(kick_data, start_time, duration_seconds)
        }

        output_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Converted File As"
        )
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(twitch_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Success", f"Conversion complete! File saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# GUI setup
root = tk.Tk()
root.title("Kick → Twitch Chat JSON Converter with Duration")
root.geometry("480x280")
root.resizable(False, False)

tk.Label(root, text="Convert Kick chat to TwitchDownloader format", font=("Arial", 14)).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="Stream Start Time (ISO):", font=("Arial", 11), width=20, anchor="w").grid(row=0, column=0, padx=10, pady=5)
start_time_entry = tk.Entry(frame, width=30, font=("Arial", 11))
start_time_entry.grid(row=0, column=1, padx=10, pady=5)
start_time_entry.insert(0, "2025-07-01T19:02:55Z")

tk.Label(frame, text="Stream Duration (seconds):", font=("Arial", 11), width=20, anchor="w").grid(row=1, column=0, padx=10, pady=5)
duration_entry = tk.Entry(frame, width=30, font=("Arial", 11))
duration_entry.grid(row=1, column=1, padx=10, pady=5)
duration_entry.insert(0, "25200")

btn = tk.Button(root, text="Select Kick Chat JSON and Convert", font=("Arial", 12), command=load_and_convert)
btn.pack(pady=20)

root.mainloop()
