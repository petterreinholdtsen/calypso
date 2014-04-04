import xml.etree.ElementTree as ET
from . import config, paths
from .xmlutils_generic import _tag

class Resource(object):
    """Resources initially were pseudo-collections/items (so they could be
    included in the propfind loop), but currently are objects that represent
    resources on the server that are not collectons / collection items.

    Their interfaces for propfind could possibly be inherited to Collection and
    collection Item in the future."""

    def propfind(self, tag, element):
        """If self can respond to a propfind request on a tag, update the
        prepared response element with child nodes."""

    def propfind_children(self, depth):
        """Return a list of resources / collections / items that are to be
        responded with to a propfind of a given depth"""
        return [self]

    urlpath = None # this should be present ... implement as abstract property?

class Principal(Resource):
    def __init__(self, username):
        self.username = username
        self.urlpath = config.get("server", "user_principal") % {"user": self.username} # it's currently hardcoded anyway

    def propfind(self, tag, element):
        super(Principal, self).propfind(tag, element)

        # maybe move those out to generic resources; kaddressbook doesn't query
        # for current-user-princial and ask there, but plain go to the
        # requested url and propfind for home-sets
        if tag == _tag("C", "calendar-home-set"):
            tag = ET.Element(_tag("D", "href"))
            tag.text = self.urlpath + CalendarHomeSet.type_dependent_suffix + '/'
            element.append(tag)
        elif tag == _tag("A", "addressbook-home-set"):
            tag = ET.Element(_tag("D", "href"))
            tag.text = self.urlpath + AddressbookHomeSet.type_dependent_suffix + '/'
            element.append(tag)

class HomeSet(Resource):
    def __init__(self, username):
        self.username = username
        self.urlpath = config.get("server", "user_principal") % {"user": self.username} + self.type_dependent_suffix + "/" # it's currently hardcoded anyway

    def propfind_children(self, depth):
        # FIXME ignoring depth

        collection_name = paths.collection_from_path(self.username + "/" + self.single_collection)
        from calypso import collection_singleton
        collection = collection_singleton(collection_name)
        items = [collection] # + collection.items # FIXME sequence matters, see parentcollectionhack
        return super(HomeSet, self).propfind_children(depth) + items

class AddressbookHomeSet(HomeSet):
    type_dependent_suffix = "addressbooks"
    single_collection = "addresses"

class CalendarHomeSet(HomeSet):
    type_dependent_suffix = "calendars"
    single_collection = "calendar"
