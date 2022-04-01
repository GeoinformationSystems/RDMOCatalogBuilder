#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree

from RDMOEntities.RDMOEntities import RDMOEntities


class Catalog(RDMOEntities):
    """
    Catalog class with catalog specific variables.
    """

    def __init__(self,
                 ns="{}",
                 uri=None,
                 uri_prefix=None,
                 key=None,
                 comment=None,
                 order=None,
                 title_dict=None,
                 help_dict=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.comment = comment
        self.order = order
        self.title_dict = title_dict
        self.help_dict = help_dict

    def make_element(self):
        """
        Make an etree element of a catalog entry.

        :return: Catalog element
        """

        catalog = etree.Element("catalog")
        if self.uri:
            catalog.set(self.ns + "uri", self.uri)
        etree.SubElement(catalog, "uri_prefix").text = self.uri_prefix
        etree.SubElement(catalog, "key").text = self.key
        etree.SubElement(catalog, self.ns + "comment").text = self.comment
        if self.order is not None:
            etree.SubElement(catalog, "order").text = str(self.order)
        else:
            etree.SubElement(catalog, "order")
        if self.title_dict:
            for lang in self.title_dict:
                etree.SubElement(catalog, "title", lang=lang).text = self.title_dict[lang]
        if self.help_dict:
            for lang in self.help_dict:
                etree.SubElement(catalog, "help", lang=lang).text = self.help_dict[lang]

        return catalog


class Section(RDMOEntities):
    """
    Section class with section specific variables.
    """

    def __init__(self,
                 ns="{}",
                 uri=None,
                 uri_prefix=None,
                 key=None,
                 path=None,
                 comment=None,
                 catalog=None,
                 order=None,
                 title_dict=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.path = path
        self.comment = comment
        self.catalog = catalog
        self.order = order
        self.title_dict = title_dict

    def make_element(self):
        """
        Make an etree element of a section entry.

        :return: Section element
        """

        section = etree.Element("section")
        if self.uri:
            section.set(self.ns + "uri", self.uri)
        etree.SubElement(section, "uri_prefix").text = self.uri_prefix
        etree.SubElement(section, "key").text = self.key
        etree.SubElement(section, "path").text = self.path
        etree.SubElement(section, self.ns + "comment").text = self.comment
        if self.catalog:
            etree.SubElement(section, "catalog", {self.ns + "uri": self.catalog})
        else:
            etree.SubElement(section, "catalog")
        if self.order is not None:
            etree.SubElement(section, "order").text = str(self.order)
        else:
            etree.SubElement(section, "order")
        if self.title_dict:
            for lang in self.title_dict:
                etree.SubElement(section, "title", lang=lang).text = self.title_dict[lang]

        return section


class Questionset(RDMOEntities):
    """
    Questionset class with questionset specific variables.
    """

    def __init__(self,
                 ns="{}",
                 uri=None,
                 uri_prefix=None,
                 key=None,
                 path=None,
                 comment=None,
                 attribute=None,
                 section=None,
                 questionset=None,
                 is_collection=None,
                 order=None,
                 title_dict=None,
                 help_dict=None,
                 verbose_name_dict=None,
                 verbose_name_plural_dict=None,
                 conditions=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.path = path
        self.comment = comment
        self.attribute = attribute
        self.section = section
        self.questionset = questionset
        self.is_collection = make_first_upper(str(is_collection))
        self.order = order
        self.title_dict = title_dict
        self.help_dict = help_dict
        self.verbose_name_dict = verbose_name_dict
        self.verbose_name_plural_dict = verbose_name_plural_dict
        self.conditions = conditions

    def make_element(self):
        """
        Make an etree element of a questionset entry.

        :return: Questionset element
        """

        questionset = etree.Element("questionset")
        if self.uri:
            questionset.set(self.ns + "uri", self.uri)
        etree.SubElement(questionset, "uri_prefix").text = self.uri_prefix
        etree.SubElement(questionset, "key").text = self.key
        etree.SubElement(questionset, "path").text = self.path
        etree.SubElement(questionset, self.ns + "comment").text = self.comment
        if self.attribute:
            etree.SubElement(questionset, "attribute", {self.ns + "uri": self.attribute})
        else:
            etree.SubElement(questionset, "attribute")
        if self.section:
            etree.SubElement(questionset, "section", {self.ns + "uri": self.section})
        else:
            etree.SubElement(questionset, "section")
        if self.questionset:
            etree.SubElement(questionset, "questionset", {self.ns + "uri": self.questionset})
        else:
            etree.SubElement(questionset, "questionset")
        etree.SubElement(questionset, "is_collection").text = self.is_collection
        if self.order is not None:
            etree.SubElement(questionset, "order").text = str(self.order)
        else:
            etree.SubElement(questionset, "order")
        # get languages in title, help, verbose_name and verbose_name_plural
        lang = list()
        if self.title_dict:
            lang.extend(list(self.title_dict.keys()))
        if self.help_dict:
            lang.extend(list(self.help_dict.keys()))
        if self.verbose_name_dict:
            lang.extend(list(self.verbose_name_dict.keys()))
        if self.verbose_name_plural_dict:
            lang.extend(list(self.verbose_name_plural_dict.keys()))
        lang = list(set(lang))  # get unique list members
        if len(lang) > 0:
            # languages available
            for langAct in lang:
                if self.title_dict and langAct in self.title_dict:
                    etree.SubElement(questionset, "title", lang=langAct).text = self.title_dict[langAct]
                else:
                    etree.SubElement(questionset, "title", lang=langAct)
                if self.help_dict and langAct in self.help_dict:
                    etree.SubElement(questionset, "help", lang=langAct).text = self.help_dict[langAct]
                else:
                    etree.SubElement(questionset, "help", lang=langAct)
                if self.verbose_name_dict and langAct in self.verbose_name_dict:
                    etree.SubElement(questionset, "verbose_name", lang=langAct).text = self.verbose_name_dict[langAct]
                else:
                    etree.SubElement(questionset, "verbose_name", lang=langAct)
                if self.verbose_name_plural_dict and langAct in self.verbose_name_plural_dict:
                    etree.SubElement(questionset, "verbose_name_plural", lang=langAct) \
                        .text = self.verbose_name_plural_dict[langAct]
                else:
                    etree.SubElement(questionset, "verbose_name_plural", lang=langAct)
        if self.conditions:
            conditions = etree.Element("conditions")
            for condition in self.conditions:
                etree.SubElement(conditions, "condition", {self.ns + "uri": condition})
            questionset.append(conditions)
        else:
            etree.SubElement(questionset, "conditions")

        return questionset


class Question(RDMOEntities):
    """
    Question class with question specific variables.
    """

    def __init__(self,
                 ns="{}",
                 uri=None,
                 uri_prefix=None,
                 key=None,
                 path=None,
                 comment=None,
                 attribute=None,
                 questionset=None,
                 is_collection=False,
                 is_optional=False,
                 order=None,
                 help_dict=None,
                 text_dict=None,
                 default_text_dict=None,
                 verbose_name_dict=None,
                 verbose_name_plural_dict=None,
                 widget_type=None,
                 value_type=None,
                 maximum=None,
                 minimum=None,
                 step=None,
                 unit=None,
                 width=None,
                 optionsets=None,
                 default_option=None,
                 conditions=None,
                 default_external_id=None):
        self.ns = ns
        self.uri = uri
        self.uri_prefix = uri_prefix
        self.key = key
        self.path = path
        self.comment = comment
        self.attribute = attribute
        self.questionset = questionset
        self.is_collection = make_first_upper(str(is_collection))
        self.is_optional = make_first_upper(str(is_optional))
        if order:
            self.order = make_first_upper(str(order))
        else:
            self.order = order
        self.help_dict = help_dict
        self.text_dict = text_dict
        self.default_text_dict = default_text_dict
        self.verbose_name_dict = verbose_name_dict
        self.verbose_name_plural_dict = verbose_name_plural_dict
        self.widget_type = widget_type
        self.value_type = value_type
        self.maximum = maximum
        self.minimum = minimum
        self.step = step
        self.unit = unit
        self.width = width
        self.optionsets = optionsets
        self.default_option = default_option
        self.conditions = conditions
        self.default_external_id = default_external_id

    def make_element(self):
        """
        Make an etree element of a question entry.

        :return: Question element
        """

        question = etree.Element("question")
        if self.uri:
            question.set(self.ns + "uri", self.uri)
        etree.SubElement(question, "uri_prefix").text = self.uri_prefix
        etree.SubElement(question, "key").text = self.key
        etree.SubElement(question, "path").text = self.path
        etree.SubElement(question, self.ns + "comment").text = self.comment
        if self.attribute:
            etree.SubElement(question, "attribute", {self.ns + "uri": self.attribute})
        else:
            etree.SubElement(question, "attribute")
        if self.questionset:
            etree.SubElement(question, "questionset", {self.ns + "uri": self.questionset})
        else:
            etree.SubElement(question, "questionset")
        etree.SubElement(question, "is_collection").text = self.is_collection
        etree.SubElement(question, "is_optional").text = self.is_optional
        if self.order is not None:
            etree.SubElement(question, "order").text = str(self.order)
        else:
            etree.SubElement(question, "order")
        # get languages in help, text, default_text, verbose_name and verbose_name_plural
        lang = list()
        if self.help_dict:
            lang.extend(list(self.help_dict.keys()))
        if self.text_dict:
            lang.extend(list(self.text_dict.keys()))
        if self.default_text_dict:
            lang.extend(list(self.default_text_dict.keys()))
        if self.verbose_name_dict:
            lang.extend(list(self.verbose_name_dict.keys()))
        if self.verbose_name_plural_dict:
            lang.extend(list(self.verbose_name_plural_dict.keys()))
        lang = list(set(lang))  # get unique list members via a set
        if len(lang) > 0:
            # languages available
            for langAct in lang:
                if self.help_dict and langAct in self.help_dict:
                    etree.SubElement(question, "help", lang=langAct).text = self.help_dict[langAct]
                else:
                    etree.SubElement(question, "help", lang=langAct)
                if self.text_dict and langAct in self.text_dict:
                    etree.SubElement(question, "text", lang=langAct).text = self.text_dict[langAct]
                else:
                    etree.SubElement(question, "text", lang=langAct)
                if self.default_text_dict and langAct in self.default_text_dict:
                    etree.SubElement(question, "default_text", lang=langAct).text = self.default_text_dict[langAct]
                else:
                    etree.SubElement(question, "default_text", lang=langAct)
                if self.verbose_name_dict and langAct in self.verbose_name_dict:
                    etree.SubElement(question, "verbose_name", lang=langAct).text = self.verbose_name_dict[langAct]
                else:
                    etree.SubElement(question, "verbose_name", lang=langAct)
                if self.verbose_name_plural_dict and langAct in self.verbose_name_plural_dict:
                    etree.SubElement(question, "verbose_name_plural", lang=langAct) \
                        .text = self.verbose_name_plural_dict[langAct]
                else:
                    etree.SubElement(question, "verbose_name_plural", lang=langAct)
        etree.SubElement(question, "widget_type").text = self.widget_type
        etree.SubElement(question, "value_type").text = self.value_type
        etree.SubElement(question, "maximum").text = self.maximum
        etree.SubElement(question, "minimum").text = self.minimum
        etree.SubElement(question, "step").text = self.step
        etree.SubElement(question, "unit").text = self.unit
        if self.width is not None:
            etree.SubElement(question, "width").text = str(self.width)
        else:
            etree.SubElement(question, "width")
        if self.optionsets:
            optionsets = etree.Element("optionsets")
            etree.SubElement(optionsets, "optionset", {self.ns + "uri": self.optionsets})
            question.append(optionsets)
        else:
            etree.SubElement(question, "optionsets")
        if self.default_option:
            # in case of an optionset a default option can apply
            etree.SubElement(question, "default_option", {self.ns + "uri": self.default_option})
        else:
            etree.SubElement(question, "default_option")
        if self.conditions:
            conditions = etree.Element("conditions")
            for condition in self.conditions:
                etree.SubElement(conditions, "condition", {self.ns + "uri": condition})
            question.append(conditions)
        else:
            etree.SubElement(question, "conditions")
        etree.SubElement(question, "default_external_id").text = self.default_external_id

        return question


def make_first_upper(in_string):
    """
    Change first character in string into upper case

    :param in_string: original string
    :return: changed string
    """

    return in_string[0].upper() + in_string[1:]
