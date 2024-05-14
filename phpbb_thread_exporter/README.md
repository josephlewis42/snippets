# phpBB thread downloader

Helps you export a phpBB thread's text and images as a single HTML page so it can
be archived or turned into a PDF.

## Usage

1. Find the URL of the thread to download, this is the first parameter.
1. Navigate to the last page of the thread, look grab the value of the `start` query parameter, this is the second parameter.
1. Look at the pagination links to determine how many items are incremented per page, this is the third parameter.
1. Run the command, it'll download the text and images and convert `<img>` tags to reference the downloaded images. Images are stored by UUID5s.

Example:

```sh
phpbb-download.py https://www.tnttt.com/viewtopic.php?f=50&t=45917 465 15
```