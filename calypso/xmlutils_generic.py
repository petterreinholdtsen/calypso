"""Common XML constructs"""

NAMESPACES = {
    "C": "urn:ietf:params:xml:ns:caldav",
    "A": "urn:ietf:params:xml:ns:carddav",
    "D": "DAV:",
    "E": "http://apple.com/ns/ical/",
    "CS": "http://calendarserver.org/ns/"}

def _tag(short_name, local):
    """Get XML Clark notation {uri(``short_name``)}``local``."""
    return "{%s}%s" % (NAMESPACES[short_name], local)
