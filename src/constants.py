MD_IMAGE_DETECTION_REGEX = r"(!\[[^\[\]]*\]\((?:(?:http|https)://)?(?:www.)?(?:[a-zA-Z0-9@:%._\+~#?&/=]{2,256}\.[a-z]{2,6}\b)?(?:[-a-zA-Z0-9@:%._\+~#?&//=]*)\))"
MD_LINK_DETECTION_REGEX = r"(\[[^\[\]]+\]\((?:(?:http|https)://)?(?:www.)?(?:[a-zA-Z0-9@:%._\+~#?&/=]{2,256}\.[a-z]{2,6}\b)?(?:[-a-zA-Z0-9@:%._\+~#?&//=]*)\))"
MD_LINK_EXTRACTION_REGEX = r"\[([^\[\]]+)\]\(((?:(?:http|https)://)?(?:www.)?(?:[a-zA-Z0-9@:%._\+~#?&/=]{2,256}\.[a-z]{2,6}\b)?(?:[-a-zA-Z0-9@:%._\+~#?&//=]*))\)"
MD_IMAGE_EXTRACTION_REGEX = r"!\[([^\[\]]*)\]\(((?:(?:http|https)://)?(?:www.)?(?:[a-zA-Z0-9@:%._\+~#?&/=]{2,256}\.[a-z]{2,6}\b)?(?:[-a-zA-Z0-9@:%._\+~#?&//=]*))\)"
MD_BLOCK_SPLITTER = r"[\n\r]{2,}"
BLOCKTYPE_IDENTIFIER = r"((?P<Heading>^\#{1,6}\s)|(?P<Code>^```.*```$)|(?P<Quote>^\>)|(?P<Unordered_List>^[\*\-]\s)|(?P<Ordered_List>^\d+\.\s)|(?P<Paragraph>^(?![\*\-]\s|\#{1,6}\s|```|\d+\.\s|\>)))"
BLOCKTYPE_CLEANERS = [("Heading", r"^\#{1,6}\s+"), ("Code", r"^```|```$"), ("Quote", r"^\>"), ("Unordered_List", r"^[\*\-]\s+"), ("Ordered_List", r"^\d+\.\s+"), ("Paragraph", r"")]
BLOCKTYPE_GET_STYLE = [("Heading", r"^(\#{1,6})\s"), ("Code", r""), ("Quote", r""), ("Unordered_List", r"^([\*\-])\s"), ("Ordered_List", r""), ("Paragraph", r"")]