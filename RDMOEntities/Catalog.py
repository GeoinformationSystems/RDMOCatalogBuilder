#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree


class Catalog:
    def __init__(self, ns="{}", uri=None, uri_prefix=None, key=None, comment=None, order=None, title=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.comment = comment
        self.order = order
        self.title = title

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


class Section:
    def __init__(self, ns="{}", uri=None, uri_prefix=None, key=None, path=None, comment=None, catalog=None, order=None
                 , title=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.path = path
        self.comment = comment
        self.catalog = catalog
        self.order = order
        self.title = title

    def make_element(self):
        section = etree.Element("section")
        if self.uri:
            section.set(self.ns + "uri", self.uri)
        etree.SubElement(section, "uri_prefix").text = self.uri_prefix
        etree.SubElement(section, "key").text = self.key
        etree.SubElement(section, "path").text = self.path
        etree.SubElement(section, "comment").text = self.comment
        etree.SubElement(section, "catalog").text = self.catalog
        etree.SubElement(section, "order").text = self.order
        if self.title:
            for i in self.title:
                etree.SubElement(section, "title", lang=i).text = self.title[i]

        return section


class Questionset:
    def __init__(self, ns="{}", uri=None, uri_prefix=None, key=None, path=None, comment=None, attribute=None
                 , section=None, is_collection=None, order=None, title_explanation=None, conditions=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.path = path
        self.comment = comment
        self.attribute = attribute
        self.section = section
        self.is_collection = is_collection
        self.order = order
        self.title_explanation = title_explanation
        self.conditions = conditions

    def make_element(self):
        questionset = etree.Element("questionset")
        if self.uri:
            questionset.set(self.ns + "uri", self.uri)
        etree.SubElement(questionset, "uri_prefix").text = self.uri_prefix
        etree.SubElement(questionset, "key").text = self.key
        etree.SubElement(questionset, "path").text = self.path
        etree.SubElement(questionset, self.ns + "comment").text = self.comment
        etree.SubElement(questionset, "attribute").text = self.attribute
        etree.SubElement(questionset, self.ns + "uri", self.section)
        etree.SubElement(questionset, "is_collection").text = self.is_collection
        etree.SubElement(questionset, "order").text = self.order
        if self.title_explanation:
            title_explanation_keys = list(self.title_explanation.keys())
            for i in range(len(title_explanation_keys)):
                title_explanation_act = self.title_explanation[title_explanation_keys[i]]
                if "title" in title_explanation_act:
                    etree.SubElement(questionset, "title", lang=title_explanation_keys[i]).text = title_explanation_act["title"]
                if "help" in title_explanation_act:
                    etree.SubElement(questionset, "help", lang=title_explanation_keys[i]).text = title_explanation_act["help"]
                if "verbose_name" in title_explanation_act:
                    etree.SubElement(questionset, "verbose_name", lang=title_explanation_keys[i]).text = title_explanation_act["verbose_name"]
                if "verbose_name_plural" in title_explanation_act:
                    etree.SubElement(questionset, "verbose_name_plural", lang=title_explanation_keys[i]).text = title_explanation_act["verbose_name_plural"]

        return questionset


class Question:
    def __init__(self, ns="{}", uri=None, uri_prefix=None, key=None, path=None, comment=None, attribute=None
                 , questionset=None, is_collection=False, order=None, explanation=None, widget_type=None
                 , value_type=None, maximum=None, minimum=None, step=None, unit=None, optionsets=None, conditions=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.path = path
        self.comment = comment
        self.attribute = attribute
        self.questionset = questionset
        self.is_collection = str(is_collection)
        if order:
            self.order = str(order)
        else:
            self.order = order
        self.explanation = explanation
        self.widget_type = widget_type
        self.value_type = value_type
        self.maximum = maximum
        self.minimum = minimum
        self.step = step
        self.unit = unit
        self.optionsets = optionsets
        self.conditions = conditions

    def make_element(self):
        question = etree.Element("question")
        if self.uri:
            question.set(self.ns + "uri", self.uri)
        etree.SubElement(question, "uri_prefix").text = self.uri_prefix
        etree.SubElement(question, "key").text = self.key
        etree.SubElement(question, "path").text = self.path
        etree.SubElement(question, self.ns + "comment").text = self.comment
        etree.SubElement(question, "attribute").text = self.attribute
        etree.SubElement(question, "questionset").text = self.questionset
        etree.SubElement(question, "is_collection").text = self.is_collection
        etree.SubElement(question, "order").text = self.order
        if self.explanation:
            explanation_keys = list(self.explanation.keys())
            for i in range(len(explanation_keys)):
                explanation_act = self.explanation[explanation_keys[i]]
                if "help" in explanation_act:
                    etree.SubElement(question, "help", lang=explanation_keys[i]).text = explanation_act["help"]
                if "text" in explanation_act:
                    etree.SubElement(question, "text", lang=explanation_keys[i]).text = explanation_act["text"]
                if "verbose_name" in explanation_act:
                    etree.SubElement(question, "verbose_name", lang=explanation_keys[i]).text \
                        = explanation_act["verbose_name"]
                if "verbose_name_plural" in explanation_act:
                    etree.SubElement(question, "verbose_name_plural", lang=explanation_keys[i]).text \
                        = explanation_act["verbose_name_plural"]
        etree.SubElement(question, "widget_type").text = self.widget_type
        etree.SubElement(question, "value_type").text = self.value_type
        etree.SubElement(question, "maximum").text = self.maximum
        etree.SubElement(question, "minimum").text = self.minimum
        etree.SubElement(question, "step").text = self.step
        etree.SubElement(question, "unit").text = self.unit
        etree.SubElement(question, "optionsets").text = self.optionsets
        etree.SubElement(question, "conditions").text = self.conditions

        return question
