from icrawler.builtin import GoogleImageCrawler
from config import IMAGES_FOLDER


def google_image_search(query, num_images):
    google_crawler = GoogleImageCrawler(storage={'root_dir': IMAGES_FOLDER})
    google_crawler.crawl(keyword=query, max_num=num_images)

    # rename the image files to match the query
    # for image in google_crawler.storage.list_files():
    #     new_name = image.replace(query, '')
    #     google_crawler.storage.rename_file(image, new_name)