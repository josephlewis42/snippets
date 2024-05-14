#!/usr/bin/env python3

from bs4 import BeautifulSoup
from functools import cache
import requests
import click
import os
import time
import uuid
import os.path as path


HEAD = """
<html>
<head>
<style>
.post {
    border-top: 1px dotted gray;
    margin-top: 1em;
    padding: 1em;
}

.signature {
    display: none;
}

.back2top {
    display: none;
}

.postprofile {
    display: none;
}
</style>
</head>
<body>
"""

TAIL = """
</body>
</html>
"""

class InvalidResponse(Exception):
    pass



def _get_page(url: str) -> requests.Response:
    try:
        response = requests.get(url)
        if (status := response.status_code) != 200:
            raise InvalidResponse(f"Response for {url} was {status}")
    except Exception as e:
        raise InvalidResponse(f"Error fetching {url}: {e}")
    return response

from urllib.parse import urlparse, parse_qs

def parse_params(url: str) -> str:
    parsed = urlparse(url)
    query_string = parse_qs(parsed.query)
    
    forum_id = ""
    if "f" in query_string:
        forum_id = query_string["f"][0]
    
    thread_id = query_string["t"][0]
    
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?f={forum_id}&t={thread_id}&start="

def dirname(url: str) -> str:
    parsed = urlparse(url)
    query_string = parse_qs(parsed.query)
    thread_id = query_string["t"][0]
    
    return f"{parsed.netloc}_thread{thread_id}"

def download_image_cached(output_dir: str, fully_qualified_url: str) -> str:
    parsed = urlparse(fully_qualified_url)
    image_id = str(uuid.uuid5(uuid.NAMESPACE_URL, fully_qualified_url))
    output_path = path.join(output_dir, image_id)
    
    if os.path.isfile(output_path):
        print(f"Already have {fully_qualified_url} cached as {image_id} ")
        return image_id

    print(f"Downloading image: {fully_qualified_url} as {image_id}")    
    with open(output_path, 'wb') as fd:
        result = _get_page(fully_qualified_url)
        for chunk in result.iter_content(chunk_size=1024):
            fd.write(chunk)
    return image_id
    
def download_image(output_dir: str, page_url: str, src: str) -> str:
    fully_qualified_url = requests.compat.urljoin(page_url, src)
    try:
        return download_image_cached(output_dir, fully_qualified_url)
    except InvalidResponse as e:
        print(e)
        return fully_qualified_url


@click.command("phpbb-download")
@click.version_option("0.1.0", prog_name="hello")
@click.argument("url", help="Full URL to a viewtopic.php page including the f and t query params.")
@click.argument("last", type=int, help="Offset of the last page, found in the start= query param of the last page.")
@click.argument("by", type=int, help="How many posts are shown on per page.")
def download_topic(url: str, last: int, by: int) -> None:
    """Downloads the text and images from a phpBB forum thread."""

    output_dir = dirname(url)
    os.makedirs(output_dir, exist_ok=True)
    
    raw_url = parse_params(url)
    

    posts = []
    
    for idx in range(0, last+1, by):
        page_url = f"{raw_url}{idx}"
        print(f"Fetching: {page_url}")
        response = _get_page(page_url)
        soup = BeautifulSoup(response.text, features="html.parser")
        page_posts = soup.find_all("div", class_="post")
        posts.extend(page_posts)
        
        for post in page_posts:
            # Make all images absolute
            for img in post.find_all("img"):
                if "src" in img.attrs:
                    src = img.attrs["src"]
                    img.attrs["src"] = "./" + download_image(output_dir, page_url, src)
            
        time.sleep(.5)
        
    with open(path.join(output_dir, "thread.html"), 'wt') as out:
        out.write(HEAD)
        for post in posts:
            out.write(str(post))
            out.write('\n')
        out.write(TAIL)


if __name__ == "__main__":
    download_topic()
