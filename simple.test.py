#!/usr/bin/env python3
"""
Quick test to see if YouTube extraction works with updated yt-dlp
"""
import yt_dlp


def test_youtube_extraction():
    print("Testing YouTube extraction with updated yt-dlp...")

    # Configure yt-dlp with your proxy and anti-detection
    ydl_opts = {
        "quiet": False,  # Show output for debugging
        "skip_download": True,
        "proxy": "socks5h://127.0.0.1:10808",
        "noplaylist": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android"],
                "player_skip": ["webpage", "configs"],
            }
        },
        "http_headers": {
            "User-Agent": "com.google.android.youtube/17.36.4 (Linux; U; Android 12; GB) gzip",
        },
    }

    test_url = "https://youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll

    try:
        print(f"Extracting: {test_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)

        print(f"✅ SUCCESS!")
        print(f"Title: {info.get('title')}")
        print(f"Formats available: {len(info.get('formats', []))}")

        # Show some format details
        formats = info.get('formats', [])
        progressive = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') != 'none']
        adaptive = [f for f in formats if f.get('acodec') == 'none' or f.get('vcodec') == 'none']

        print(f"Progressive streams: {len(progressive)}")
        print(f"Adaptive streams: {len(adaptive)}")

        if progressive:
            print("\nSample progressive formats:")
            for f in progressive[:3]:
                print(f"  - {f.get('format_id')}: {f.get('ext')} {f.get('resolution', 'N/A')}")

        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


if __name__ == "__main__":
    success = test_youtube_extraction()

    if success:
        print("\n🎉 YouTube extraction is working!")
        print("You can now use your Flask app with confidence.")
    else:
        print("\n😞 Still having issues. Let's try a different approach...")
        print("The problem might be YouTube's latest bot detection updates.")