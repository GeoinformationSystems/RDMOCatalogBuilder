#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree
from RDMOEntities.RDMOEntities import RDMOEntities


class Optionset(RDMOEntities):
    def __init__(self,
                 ns="{}",
                 uri=None,
                 uri_prefix=None,
                 key=None,
                 comment=None,
                 order=None,
                 conditions=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.comment = comment
        self.order = order
        self.conditions = conditions

    def make_element(self):
        optionset = etree.Element("optionset")
        if self.uri:
            optionset.set(self.ns + "uri", self.uri)
        etree.SubElement(optionset, "uri_prefix").text = self.uri_prefix
        etree.SubElement(optionset, "key").text = self.key
        etree.SubElement(optionset, self.ns + "comment").text = self.comment
        etree.SubElement(optionset, "order").text = self.order
        etree.SubElement(optionset, "conditions").text = self.conditions

        return optionset


class Option(RDMOEntities):
    def __init__(self,
                 ns="{}",
                 uri=None,
                 uri_prefix=None,
                 key=None,
                 path=None,
                 comment=None,
                 optionset=None,
                 order=None,
                 text_dict=None,
                 additional_input=False):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.path = path
        self.comment = comment
        self.optionset = optionset
        self.order = order
        self.text_dict = text_dict
        self.additional_input = str(additional_input)

    def make_element(self):
        option = etree.Element("option")
        if self.uri:
            option.set(self.ns + "uri", self.uri)
        etree.SubElement(option, "uri_prefix").text = self.uri_prefix
        etree.SubElement(option, "key").text = self.key
        etree.SubElement(option, "path").text = self.path
        etree.SubElement(option, self.ns + "comment").text = self.comment
        if self.optionset:
            etree.SubElement(option, "optionset", {self.ns + "uri": self.optionset})
        else:
            etree.SubElement(option, "optionset")
        if self.order is not None:
            etree.SubElement(option, "order").text = str(self.order)
        else:
            etree.SubElement(option, "order")
        if self.text_dict:
            for lang in self.text_dict:
                etree.SubElement(option, "text", lang=lang).text = self.text_dict[lang]
        etree.SubElement(option, "additional_input").text = self.additional_input

        return option
