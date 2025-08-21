import shutil
import os

# Copy cookies to /tmp so yt-dlp can read them
secret_cookies = "/etc/secrets/cookies.txt"
temp_cookies = "/tmp/cookies.txt"
shutil.copy(secret_cookies, temp_cookies)

ydl_opts = {
    "cookiefile": temp_cookies,
    "quiet": True,
    "skip_download": True
}
