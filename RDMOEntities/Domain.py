#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree
from RDMOEntities.RDMOEntities import RDMOEntities


class Attribute(RDMOEntities):
    def __init__(self, ns="{}", uri=None, uri_prefix=None, key=None, path=None, comment=None, parent=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.path = path
        self.comment = comment
        self.parent = parent

    def make_element(self):
        catalog = etree.Element("catalog")
        if self.uri:
            catalog.set(self.ns + "uri", self.uri)
        etree.SubElement(catalog, "uri_prefix").text = self.uri_prefix
        etree.SubElement(catalog, "key").text = self.key
        etree.SubElement(catalog, "comment").text = self.comment
        etree.SubElement(catalog, "order").text = self.order
        if self.title:
            for i in self.title:
                etree.SubElement(catalog, "title", lang=i).text = self.title[i]

        return catalog
