#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree
from RDMOEntities.RDMOEntities import RDMOEntities


class Attribute(RDMOEntities):
    """
    Attribute class with question attribute variables for the domain.
    """

    def __init__(self,
                 ns="{}",
                 uri=None,
                 uri_prefix=None,
                 key=None,
                 path=None,
                 comment=None,
                 parent=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.path = path
        self.comment = comment
        self.parent = parent

    def make_element(self):
        """
        Make an etree element of an attribute entry.

        :return: Attribute element
        """

        attribute = etree.Element("attribute")
        if self.uri:
            attribute.set(self.ns + "uri", self.uri)
        etree.SubElement(attribute, "uri_prefix").text = self.uri_prefix
        etree.SubElement(attribute, "key").text = self.key
        etree.SubElement(attribute, "path").text = self.path
        etree.SubElement(attribute, self.ns + "comment").text = self.comment
        if self.parent:
            etree.SubElement(attribute, "parent", {self.ns + "uri": self.parent})
        else:
            etree.SubElement(attribute, "parent")

        return attribute
