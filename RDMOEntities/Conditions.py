#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree
from RDMOEntities.RDMOEntities import RDMOEntities


class Condition(RDMOEntities):
    """
    Condition class with condition specific variables.
    """

    def __init__(self,
                 ns="{}",
                 uri=None,
                 uri_prefix=None,
                 key=None,
                 comment=None,
                 source=None,
                 relation=None,
                 target_text=None,
                 target_option=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.comment = comment
        self.source = source
        self.relation = relation
        self.target_text = target_text
        self.target_option = target_option

    def make_element(self):
        """
        Make an etree element of a condition entry.

        :return: Condition element
        """

        condition = etree.Element("condition")
        if self.uri:
            condition.set(self.ns + "uri", self.uri)
        etree.SubElement(condition, "uri_prefix").text = self.uri_prefix
        etree.SubElement(condition, "key").text = self.key
        etree.SubElement(condition, self.ns + "comment").text = self.comment
        if self.source:
            etree.SubElement(condition, "source", {self.ns + "uri": self.source})
        else:
            etree.SubElement(condition, "source")
        etree.SubElement(condition, "relation").text = self.relation
        etree.SubElement(condition, "target_text").text = self.target_text
        etree.SubElement(condition, "target_option").text = self.target_option

        return condition
