import webbrowser
import sys

def open_website(url):
    """
    Opens a URL in the default browser.
    """
    print(f"Opening browser: {url}")
    try:
        # Check if python has headers for browser
        if not url.startswith('http'):
            url = 'https://' + url
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error opening browser: {e}")
        return False

def open_youtube_video(query=None):
    """
    Opens YouTube. Optionally searches.
    """
    if query:
        url = f"https://www.youtube.com/results?search_query={query}"
    else:
        url = "https://www.youtube.com"
    open_website(url)
    return True
