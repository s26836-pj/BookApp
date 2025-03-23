import os
from io import BytesIO
from urllib.parse import quote_plus

import requests
from PIL import Image
from django.conf import settings


def is_image_valid(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        width, height = image.size

        if width < 200 or height < 300:
            return False

        if image.mode in ("1", "L", "P"):
            pixel_set = set(image.getdata())
            if len(pixel_set) < 10:
                return False

        return True
    except Exception as e:
        print(f"Image validation error: {e}")
        return False


def fetch_cover_from_google_books_local(book):
    query = quote_plus(book.title)
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{query}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        items = data.get("items")
        if not items or not isinstance(items, list):
            return

        for item in items:
            volume_info = item.get("volumeInfo", {})
            api_title = volume_info.get("title", "").lower()
            image_links = volume_info.get("imageLinks", {})

            if book.title.lower() not in api_title:
                continue

            thumbnail_url = image_links.get("thumbnail")
            if thumbnail_url and "notavailable" not in thumbnail_url:
                thumbnail_url = thumbnail_url.replace("&zoom=1", "&zoom=3")

                img_response = requests.get(thumbnail_url, timeout=5)
                img_response.raise_for_status()

                if not is_image_valid(img_response.content):
                    continue

                cover_dir = os.path.join(settings.MEDIA_ROOT, "covers")
                os.makedirs(cover_dir, exist_ok=True)

                cover_path = os.path.join(cover_dir, f"book_{book.id}.jpg")
                with open(cover_path, "wb") as f:
                    f.write(img_response.content)

                book.cover_url = f"/media/covers/book_{book.id}.jpg"
                book.save()


                return

    except Exception as e:
        print(f"Error downloading cover for {book.title}: {e}")
