import os
import yt_dlp

TEMP_DIR = "temp"

os.makedirs(TEMP_DIR, exist_ok=True)

def download_audio(url):

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{TEMP_DIR}/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=True
        )

        file_path = ydl.prepare_filename(info)

    if not os.path.exists(file_path):

        raise Exception(
            "Audio download failed"
        )

    return file_path
