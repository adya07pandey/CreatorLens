import os
import gc
import time
import httpx
import yt_dlp
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

        info = ydl.extract_info(url, download=True)

        file_path = ydl.prepare_filename(info)

    if not os.path.exists(file_path):
        raise Exception("Audio download failed")

    print(f"[INFO] Audio saved: {file_path}")

    return file_path


def download_audio_from_url(audio_url):

    print(f"[INFO] Downloading audio from: {audio_url[:100]}...")

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", dir=TEMP_DIR, delete=False)

    try:

        with httpx.stream("GET", audio_url, timeout=600) as response:

            response.raise_for_status()

            print(f"[INFO] Audio status: {response.status_code}")

            for chunk in response.iter_bytes():

                if chunk:
                    tmp.write(chunk)

        tmp.close()

        print(f"[INFO] Saved audio: {tmp.name}")

        return tmp.name

    except Exception:

        tmp.close()

        if os.path.exists(tmp.name):
            os.remove(tmp.name)

        raise


def delete_audio_file(audio_path):

    try:

        gc.collect()

        time.sleep(1)

        if audio_path and os.path.exists(audio_path):

            print(f"[DELETE] {audio_path}")

            os.remove(audio_path)

            print(f"[DELETE SUCCESS] {audio_path}")

        else:

            print(f"[DELETE SKIPPED] {audio_path}")

    except Exception as e:

        print(f"[DELETE ERROR] {e}")