#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree
from RDMOEntities.RDMOEntities import RDMOEntities


class Task(RDMOEntities):
    def __init__(self,
                 ns="{}",
                 uri=None,
                 uri_prefix=None,
                 key=None,
                 comment=None,
                 title_dict=None,
                 text_dict=None,
                 start_attribute=None,
                 end_attribute=None,
                 days_before=None,
                 days_after=None,
                 conditions=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.comment = comment
        self.title_dict = title_dict
        self.text_dict = text_dict
        self.start_attribute = start_attribute
        self.end_attribute = end_attribute
        self.days_before = days_before
        self.days_after = days_after
        self.conditions = conditions

    def make_element(self):
        task = etree.Element("task")
        if self.uri:
            task.set(self.ns + "uri", self.uri)
        etree.SubElement(task, "uri_prefix").text = self.uri_prefix
        etree.SubElement(task, "key").text = self.key
        etree.SubElement(task, self.ns + "comment").text = self.comment
        # get languages in title, help, verbose_name and verbose_name_plural
        lang = list()
        if self.title_dict:
            lang.extend(list(self.title_dict.keys()))
        if self.text_dict:
            lang.extend(list(self.text_dict.keys()))
        lang = list(set(lang))  # get unique list members
        if len(lang) > 0:
            # languages available
            for langAct in lang:
                if self.title_dict and langAct in self.title_dict:
                    etree.SubElement(task, "title", lang=langAct).text = self.title_dict[langAct]
                else:
                    etree.SubElement(task, "title", lang=langAct)
                if self.text_dict and langAct in self.text_dict:
                    etree.SubElement(task, "text", lang=langAct).text = self.text_dict[langAct]
                else:
                    etree.SubElement(task, "text", lang=langAct)
        if self.start_attribute:
            etree.SubElement(task, "start_attribute", {self.ns + "uri": self.start_attribute})
        else:
            etree.SubElement(task, "start_attribute")
        if self.end_attribute:
            etree.SubElement(task, "end_attribute", {self.ns + "uri": self.end_attribute})
        else:
            etree.SubElement(task, "end_attribute")
        etree.SubElement(task, "days_before").text = self.days_before
        etree.SubElement(task, "days_after").text = self.days_after
        etree.SubElement(task, "conditions").text = self.conditions

        return task
