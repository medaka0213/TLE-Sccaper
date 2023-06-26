# tlescraper\scraper.py
import urllib.request
import os
import logging

logger = logging.getLogger(__name__)

CERESTRACK_BASE_URL = "https://celestrak.com/NORAD/elements/"


def save_tle(CATNR: str, output_dir) -> str:
    """Saves the TLE of a satellite to a file"""
    url = f"{CERESTRACK_BASE_URL}/gp.php?CATNR={CATNR}"

    filename = os.path.join(output_dir, f"{CATNR}.txt")

    # Get TLE from URL
    logger.debug(f"Loading {url} to {filename}")
    response = urllib.request.urlopen(url)

    # raise Exception
    if response.getcode() != 200:
        raise Exception(f"Error loading {url}: {response.getcode()}")

    content = response.read().decode("utf-8")
    content = "\n".join(content.splitlines()) + "\n"
    logger.debug(f"Content: {content}")

    if len(content.splitlines()) != 3:
        raise Exception(f"Error loading {url}: {content}")

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, "w", encoding="ascii") as f:
        f.write(content)
    return content
