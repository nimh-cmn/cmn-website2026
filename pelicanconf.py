AUTHOR = "Center for Multimodal Neuroimaging"
SITENAME = "Center for Multimodal Neuroimaging"
SITEURL = ""

PATH = "content"
TIMEZONE = "America/New_York"
DEFAULT_LANG = "en"

THEME = "themes/cmn-2026"
STATIC_PATHS = ["images", "assets"]

PAGE_PATHS = ["pages"]
ARTICLE_PATHS = []
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
DISPLAY_PAGES_ON_MENU = False
DEFAULT_PAGINATION = False
RELATIVE_URLS = True

MARKDOWN = {
    "extensions": ["extra", "codehilite", "toc", "meta"],
    "output_format": "html5",
}

PLUGINS = ["plugins.cmn_collections"]

CMN_NAV = [
    ("Groups", "/groups/"),
    ("People", "/people/"),
    ("Projects", "/projects/"),
    ("Software", "/software/"),
    ("Publications", "/publications/"),
    ("Talks", "/talks/"),
    ("Workshops", "/posts/"),
]

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
