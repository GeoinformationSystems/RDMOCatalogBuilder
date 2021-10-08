#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree
from io import BytesIO
from RDMOEntities import Catalog, Domain, Options
import json


class RDMOElementSet:
    def __init__(self,
                 catalog_root,
                 domain_root,
                 options_root):
        self.catalog_root = catalog_root
        self.domain_root = domain_root
        self.options_root = options_root


def create_options(options_root, optionset, ns, uri_prefix):

    # optionset element
    optionset_key = optionset["key"]
    optionset_uri = uri_prefix + "/options/" + optionset_key
    if "comment" in optionset:
        optionset_comment = optionset["comment"]
    else:
        optionset_comment = None
    if "order" in optionset:
        optionset_order = optionset["order"]
    else:
        optionset_order = None
    options_root.append(Options.Optionset(ns=ns,
                                          uri=optionset_uri,
                                          uri_prefix=uri_prefix,
                                          key=optionset_key,
                                          comment=optionset_comment,
                                          order=optionset_order)
                        .make_element())

    # option elements
    ct_options = -1
    options = optionset["option"]
    for option in options:
        ct_options += 1
        option_key = option["key"]
        option_uri = optionset_uri + "/" + option_key
        option_path = optionset_key + "/" + option_key
        if "comment" in option:
            option_comment = option["comment"]
        else:
            option_comment = None
        if "additional_input" in option:
            option_additional_input = option["additional_input"]
        else:
            option_additional_input = None
        options_root.append(Options.Option(ns=ns,
                                           uri=option_uri,
                                           uri_prefix=uri_prefix,
                                           key=option_key,
                                           path=option_path,
                                           comment=option_comment,
                                           optionset=optionset_uri,
                                           order=ct_options,
                                           text_dict=option["text"],
                                           additional_input=option_additional_input)
                            .make_element())

    return options_root


def create_catalog(catalog_file):
    """
    Create a question catalog in a tree form. The input file can only contain one catalog. The number of sections,
    questionsets and questions is not restricted.

    :param catalog_file: A json format file with the necessary input
    :return: Catalog as etree.Element
    """

    # load json content
    fid = open(catalog_file)
    content = json.load(fid)
    fid.close()

    # build catalog
    # included are catalog, domain, options, conditions, tasks
    uri_prefix = content["uri_prefix"]
    ns_map = {content["namespace"]["prefix"]: content["namespace"]["url"]}
    ns = f"{{{ns_map[content['namespace']['prefix']]}}}"

    catalog_root = etree.Element("rdmo", nsmap=ns_map)
    domain_root = etree.Element("rdmo", nsmap=ns_map)
    options_root = etree.Element("rdmo", nsmap=ns_map)

    catalog = content["catalog"]
    catalog_key = catalog["key"]
    catalog_uri = uri_prefix + "/questions/" + catalog_key

    # catalog element
    catalog_root.append(Catalog.Catalog(ns=ns,
                                        uri=catalog_uri,
                                        uri_prefix=uri_prefix,
                                        key=catalog_key,
                                        order=0,
                                        title_dict=catalog["title"])
                        .make_element())

    catalog_attribute_key = catalog_key
    catalog_attribute_uri = uri_prefix + "/domain/" + catalog_attribute_key
    catalog_attribute_path = catalog_attribute_key
    domain_root.append(Domain.Attribute(ns=ns,
                                        uri=catalog_attribute_uri,
                                        uri_prefix=uri_prefix,
                                        key=catalog_attribute_key,
                                        path=catalog_attribute_path)
                       .make_element())

    # section elements
    ct_section = -1
    sections = catalog["section"]
    for section in sections:
        ct_section += 1
        section_key = section["key"]
        section_uri = catalog_uri + "/" + section_key
        section_path = catalog_key + "/" + section_key
        catalog_root.append(Catalog.Section(ns=ns,
                                            uri=section_uri,
                                            uri_prefix=uri_prefix,
                                            key=section_key,
                                            path=section_path,
                                            catalog=catalog_uri,
                                            order=ct_section,
                                            title_dict=section["title"])
                            .make_element())

        section_attribute_key = section_key
        section_attribute_uri = catalog_attribute_uri + "/" + section_attribute_key
        section_attribute_path = catalog_attribute_path + "/" + section_attribute_key
        domain_root.append(Domain.Attribute(ns=ns,
                                            uri=section_attribute_uri,
                                            uri_prefix=uri_prefix,
                                            key=section_attribute_key,
                                            path=section_attribute_path,
                                            parent=catalog_attribute_uri)
                           .make_element())

        # questionset elements
        ct_questionset = -1
        questionsets = section["questionset"]
        for questionset in questionsets:
            ct_questionset += 1
            questionset_key = questionset["key"]
            questionset_uri = section_uri + "/" + questionset_key
            questionset_path = section_path + "/" + questionset_key
            if "title" in questionset:
                questionset_title = questionset["title"]
            else:
                questionset_title = None
            if "help" in questionset:
                questionset_help = questionset["help"]
            else:
                questionset_help = None
            if "verbose_name" in questionset:
                questionset_verbose_name = questionset["verbose_name"]
            else:
                questionset_verbose_name = None
            if "verbose_name_plural" in questionset:
                questionset_verbose_name_plural = questionset["verbose_name_plural"]
            else:
                questionset_verbose_name_plural = None
            catalog_root.append(Catalog.Questionset(ns=ns,
                                                    uri=questionset_uri,
                                                    uri_prefix=uri_prefix,
                                                    key=questionset_key,
                                                    path=questionset_path,
                                                    section=section_uri,
                                                    order=ct_questionset,
                                                    title_dict=questionset_title,
                                                    help_dict=questionset_help,
                                                    verbose_name_dict=questionset_verbose_name,
                                                    verbose_name_plural_dict=questionset_verbose_name_plural)
                                .make_element())

            questionset_attribute_key = questionset_key
            questionset_attribute_uri = section_attribute_uri + "/" + questionset_attribute_key
            questionset_attribute_path = section_attribute_path + "/" + questionset_attribute_key
            domain_root.append(Domain.Attribute(ns=ns,
                                                uri=questionset_attribute_uri,
                                                uri_prefix=uri_prefix,
                                                key=questionset_attribute_key,
                                                path=questionset_attribute_path,
                                                parent=section_attribute_uri)
                               .make_element())

            # question elements
            ct_question = -1
            questions = questionset["question"]
            for question in questions:
                ct_question += 1
                question_key = question["key"]
                question_uri = questionset_uri + "/" + question_key
                question_path = questionset_path + "/" + question_key
                if "is_collection" in question:
                    question_is_collection = question["is_collection"]
                else:
                    question_is_collection = False
                if "help" in question:
                    question_help = question["help"]
                else:
                    question_help = None
                if "text" in question:
                    question_text = question["text"]
                else:
                    question_text = None
                if "verbose_name" in question:
                    question_verbose_name = question["verbose_name"]
                else:
                    question_verbose_name = None
                if "verbose_name_plural" in question:
                    question_verbose_name_plural = question["verbose_name_plural"]
                else:
                    question_verbose_name_plural = None
                if "optionset" in question:
                    # options_root.append
                    optionset = question["optionset"]
                    optionset_uri = uri_prefix + "/options/" + optionset["key"]
                    options_root = create_options(options_root=options_root,
                                                  optionset=optionset,
                                                  ns=ns,
                                                  uri_prefix=uri_prefix)
                else:
                    optionset_uri = None
                catalog_root.append(Catalog.Question(ns=ns,
                                                     uri=question_uri,
                                                     uri_prefix=uri_prefix,
                                                     key=question_key,
                                                     path=question_path,
                                                     questionset=questionset_uri,
                                                     is_collection=question_is_collection,
                                                     order=ct_question,
                                                     help_dict=question_help,
                                                     text_dict=question_text,
                                                     verbose_name_dict=question_verbose_name,
                                                     verbose_name_plural_dict=question_verbose_name_plural,
                                                     widget_type=question["widget_type"],
                                                     value_type=question["value_type"],
                                                     optionsets=optionset_uri)
                                    .make_element())

                question_attribute_key = question_key
                question_attribute_uri = questionset_attribute_uri + "/" + question_attribute_key
                question_attribute_path = questionset_attribute_path + "/" + question_attribute_key
                domain_root.append(Domain.Attribute(ns=ns,
                                                    uri=question_attribute_uri,
                                                    uri_prefix=uri_prefix,
                                                    key=question_attribute_key,
                                                    path=question_attribute_path,
                                                    parent=questionset_attribute_uri)
                                   .make_element())

    # objectify.deannotate(catalog_root)
    etree.cleanup_namespaces(catalog_root)
    etree.cleanup_namespaces(domain_root)
    etree.cleanup_namespaces(options_root)

    rdmo_element_set = RDMOElementSet(catalog_root, domain_root, options_root)

    return rdmo_element_set


def control_create_catalog(catalog_file, prefix_outfile):
    rdmo_element_set = create_catalog(catalog_file)

    # write catalog
    catalog = rdmo_element_set.catalog_root

    parser = etree.XMLParser(remove_blank_text=True)
    file_obj = BytesIO(etree.tostring(catalog))
    tree = etree.parse(file_obj, parser)

    file_catalog_out = prefix_outfile + "_questions.xml"

    try:
        with open(file_catalog_out, "wb") as xml_writer:
            tree.write(xml_writer, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    except IOError:
        pass

    # write domain
    domain = rdmo_element_set.domain_root

    parser = etree.XMLParser(remove_blank_text=True)
    file_obj = BytesIO(etree.tostring(domain))
    tree = etree.parse(file_obj, parser)

    file_domain_out = prefix_outfile + "_domain.xml"

    try:
        with open(file_domain_out, "wb") as xml_writer:
            tree.write(xml_writer, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    except IOError:
        pass

    # write options
    options = rdmo_element_set.options_root

    parser = etree.XMLParser(remove_blank_text=True)
    file_obj = BytesIO(etree.tostring(options))
    tree = etree.parse(file_obj, parser)

    file_options_out = prefix_outfile + "_options.xml"

    try:
        with open(file_options_out, "wb") as xml_writer:
            tree.write(xml_writer, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    except IOError:
        pass


    file_conditions_out = prefix_outfile + "_conditions.xml"
    file_tasks_out = prefix_outfile + "_tasks.xml"




if __name__ == '__main__':
    # catalog = create_catalog("questionaire.json")
    control_create_catalog("questionaire.json", "qa")

    # parser = etree.XMLParser(remove_blank_text=True)
    # file_obj = BytesIO(etree.tostring(catalog))
    # tree = etree.parse(file_obj, parser)

    # print()
    # print(etree.tostring(root, pretty_print=True, encoding="unicode", inclusive_ns_prefixes=True))

    # try:
    #     with open("example.xml", "wb") as xml_writer:
    #         tree.write(xml_writer, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    # except IOError:
    #     pass

    # https://www.blog.pythonlibrary.org/2014/03/26/python-creating-xml-with-lxml-objectify/
