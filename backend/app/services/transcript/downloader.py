import httpx
import os
import os
import yt_dlp
import httpx
import tempfile

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




def download_audio_from_url(audio_url):

    print(
        f"[INFO] Downloading audio from: {audio_url[:100]}..."
    )

    tmp = tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    )

    with httpx.stream(
        "GET",
        audio_url,
        timeout=600
    ) as response:

        response.raise_for_status()

        print(
            f"[INFO] Audio status: {response.status_code}"
        )

        for chunk in response.iter_bytes():

            if chunk:
                tmp.write(chunk)

    tmp.close()

    print(
        f"[INFO] Saved audio: {tmp.name}"
    )

    return tmp.name