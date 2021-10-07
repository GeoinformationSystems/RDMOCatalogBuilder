#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree
# from lxml import objectify
from io import BytesIO
from RDMOEntities import Catalog
import json


def create_catalog_test():
    ns = {
        "dc": "http://purl.org/dc/elements/1.1/"
    }
    # dc = "{%s}" % ns["dc"]
    # dc = "{" + ns["dc"] + "}"
    dc = f"{{{ns['dc']}}}"

    root_questions = etree.Element("rdmo", nsmap=ns)
    root_questions.append(Catalog.Question(ns=dc,
                                           uri="https://geokur.geo.tu-dresden.de/terms/questions/qa/prerequisites"
                                               "/data_provider_definitions/dq4usage",
                                           uri_prefix="https://geokur.geo.tu-dresden.de/terms",
                                           key="dq4usage",
                                           path="qa/prerequisites/data_provider_definitions/dq4usage")
                          .make_element())

    root_questions.append(Catalog.Question(ns=dc,
                                           uri="https://geokur.geo.tu-dresden.de/terms/questions/qa/prerequisites"
                                               "/data_provider_definitions/open4usage",
                                           uri_prefix="https://geokur.geo.tu-dresden.de/terms",
                                           key="open4usage",
                                           path="qa/prerequisites/data_provider_definitions/open4usage")
                          .make_element())
    root_questions.append(Catalog.Question(ns=dc,
                                           comment="123",
                                           is_collection=True,
                                           help_dict={"en": "A testhelp in english", "de": "A testhelp in deutsch", "fr": "help en francais"},
                                           text_dict={"en": "A testtext in english", "de": "A testtext in deutsch"},
                                           verbose_name_dict={"en": "A test verbose name in english", "de": "A test verbose name in deutsch"},
                                           verbose_name_plural_dict={"en": "A test plural verbose name in english", "de": "A test plural verbose name in deutsch"},
                                           path="qa/prerequisites/data_provider_definitions/test4usage",
                                           order=2)
                          .make_element())
    root_questions.append(Catalog.Questionset(ns=dc,
                                              comment="TestComment",
                                              title_dict={"en": "title en", "fr": "title fr"},
                                              verbose_name_dict={"en": "verbose name en"})
                          .make_element())

    # objectify.deannotate(rdmo_root)
    etree.cleanup_namespaces(root_questions)

    return root_questions


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
    uri_prefix = content["uri_prefix"]
    ns_map = {content["namespace"]["prefix"]: content["namespace"]["url"]}
    ns = f"{{{ns_map[content['namespace']['prefix']]}}}"

    catalog_root = etree.Element("rdmo", nsmap=ns_map)

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
                                                     value_type=question["value_type"])
                                    .make_element())

    # objectify.deannotate(catalog_root)
    etree.cleanup_namespaces(catalog_root)

    return catalog_root


if __name__ == '__main__':
    catalog = create_catalog("questionaire.json")
    # catalog = create_catalog_test()

    parser = etree.XMLParser(remove_blank_text=True)
    file_obj = BytesIO(etree.tostring(catalog))
    tree = etree.parse(file_obj, parser)

    # print()
    # print(etree.tostring(root, pretty_print=True, encoding="unicode", inclusive_ns_prefixes=True))

    try:
        with open("example.xml", "wb") as xml_writer:
            tree.write(xml_writer, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    except IOError:
        pass

    # https://www.blog.pythonlibrary.org/2014/03/26/python-creating-xml-with-lxml-objectify/
