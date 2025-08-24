#!/usr/bin/env python3
"""
Test proxy connection independently
"""
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_proxy_basic():
    """Test basic proxy connectivity"""
    proxies = {
        'http': 'socks5h://127.0.0.1:10808',
        'https': 'socks5h://127.0.0.1:10808'
    }

    try:
        print("Testing proxy with httpbin.org...")
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
        print(f"✅ Proxy works! Your IP: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Proxy test failed: {e}")
        return False


def test_youtube_access():
    """Test if we can reach YouTube through proxy"""
    proxies = {
        'http': 'socks5h://127.0.0.1:10808',
        'https': 'socks5h://127.0.0.1:10808'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Testing YouTube access through proxy...")
        response = requests.get('https://www.youtube.com', proxies=proxies, headers=headers, timeout=15)
        if response.status_code == 200:
            print(f"✅ Can reach YouTube! Status: {response.status_code}")
            return True
        else:
            print(f"⚠️ YouTube responded with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot reach YouTube: {e}")
        return False


def check_ports():
    """Check if ports are accessible"""
    import socket

    print("Checking local ports...")
    ports_to_check = [10808, 10809, 1080, 1081, 7890]  # Common proxy ports

    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            print(f"✅ Port {port} is open")
        else:
            print(f"❌ Port {port} is closed")
        sock.close()


if __name__ == "__main__":
    print("=== Proxy Connectivity Test ===")
    check_ports()
    print()
    basic_works = test_proxy_basic()
    print()
    youtube_works = test_youtube_access()

    print("\n=== Recommendations ===")
    if not basic_works:
        print("1. Check if V2RayN is running")
        print("2. Verify SOCKS5 port in V2RayN settings")
        print("3. Try different ports (1080, 1081, 7890)")
    elif not youtube_works:
        print("1. Check if your V2RayN server supports YouTube")
        print("2. Try different server locations")
        print("3. Check if V2RayN routing rules block YouTube")
    else:
        print("✅ Proxy seems to be working correctly!")
        print("The yt-dlp issue might be YouTube's bot detection.")
        print("Try updating yt-dlp: pip install --upgrade yt-dlp")