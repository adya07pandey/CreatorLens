import os
import yt_dlp

TEMP_DIR = "temp"

os.makedirs(TEMP_DIR, exist_ok=True)

import httpx
import tempfile

def download_audio_from_url(
    audio_url
):

    tmp = tempfile.NamedTemporaryFile(
        suffix=".m4a",
        delete=False
    )

    with httpx.stream(
        "GET",
        audio_url,
        timeout=300
    ) as response:

        response.raise_for_status()

        for chunk in response.iter_bytes():

            tmp.write(chunk)

    tmp.close()

    return tmp.name


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

