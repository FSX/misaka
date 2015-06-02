# Block-level extensions
EXT_TABLES = (1 << 0)
EXT_FENCED_CODE = (1 << 1)
EXT_FOOTNOTES = (1 << 2)

# Span-level extensions
EXT_AUTOLINK = (1 << 3)
EXT_STRIKETHROUGH = (1 << 4)
EXT_UNDERLINE = (1 << 5)
EXT_HIGHLIGHT = (1 << 6)
EXT_QUOTE = (1 << 7)
EXT_SUPERSCRIPT = (1 << 8)
EXT_MATH = (1 << 9)

# Other flags
EXT_NO_INTRA_EMPHASIS = (1 << 11)
EXT_SPACE_HEADERS = (1 << 12)
EXT_MATH_EXPLICIT = (1 << 13)

# Negative flags
EXT_DISABLE_INDENTED_CODE = (1 << 14)

# List flags
LIST_ORDERED = (1 << 0)
LI_BLOCK = (1 << 1)  # <li> containing block data

# Table flags
TABLE_ALIGN_LEFT = 1
TABLE_ALIGN_RIGHT = 2
TABLE_ALIGN_CENTER = 3
TABLE_ALIGNMASK = 3
TABLE_HEADER = 4

# HTML flags
HTML_SKIP_HTML = (1 << 0)
HTML_ESCAPE = (1 << 1)
HTML_HARD_WRAP = (1 << 2)
HTML_USE_XHTML = (1 << 3)

# Autolink types
AUTOLINK_NONE = 1  # Used internally when it is not an autolink
AUTOLINK_NORMAL = 2  # Normal http/http/ftp/mailto/etc link
AUTOLINK_EMAIL = 3  # E-mail link without explit mailto:
