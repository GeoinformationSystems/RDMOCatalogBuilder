#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from lxml import etree
# from lxml import objectify
from io import BytesIO
from RDMOEntities import Catalog


def create_catalog():
    ns = {
        "dc": "http://purl.org/dc/elements/1.1/"
    }
    # dc = "{%s}" % ns["dc"]
    # dc = "{" + ns["dc"] + "}"
    dc = f"{{{ns['dc']}}}"

    root_questions = etree.Element("rdmo", nsmap=ns)
    # root_questions.append(Catalog.Question(ns=dc,
    #                                        uri="https://geokur.geo.tu-dresden.de/terms/questions/qa/prerequisites"
    #                                            "/data_provider_definitions/dq4usage",
    #                                        uri_prefix="https://geokur.geo.tu-dresden.de/terms",
    #                                        key="dq4usage",
    #                                        path="qa/prerequisites/data_provider_definitions/dq4usage")
    #                       .make_element())
    #
    # root_questions.append(Catalog.Question(ns=dc,
    #                                        uri="https://geokur.geo.tu-dresden.de/terms/questions/qa/prerequisites"
    #                                            "/data_provider_definitions/open4usage",
    #                                        uri_prefix="https://geokur.geo.tu-dresden.de/terms",
    #                                        key="open4usage",
    #                                        path="qa/prerequisites/data_provider_definitions/open4usage")
    #                       .make_element())
    # root_questions.append(Catalog.Question(ns=dc,
    #                                        comment="123",
    #                                        is_collection=True,
    #                                        help_dict={"en": "A testhelp in english", "de": "A testhelp in deutsch", "fr": "help en francais"},
    #                                        text_dict={"en": "A testtext in english", "de": "A testtext in deutsch"},
    #                                        verbose_name_dict={"en": "A test verbose name in english", "de": "A test verbose name in deutsch"},
    #                                        verbose_name_plural_dict={"en": "A test plural verbose name in english", "de": "A test plural verbose name in deutsch"},
    #                                        path="qa/prerequisites/data_provider_definitions/test4usage",
    #                                        order=2)
    #                       .make_element())
    root_questions.append(Catalog.Questionset(ns=dc,
                                              comment="TestComment",
                                              title_dict={"en": "title en", "fr": "title fr"},
                                              verbose_name_dict={"en": "verbose name en"})
                          .make_element())

    # objectify.deannotate(rdmo_root)
    etree.cleanup_namespaces(root_questions)

    return root_questions


if __name__ == '__main__':
    root1 = create_catalog()

    parser = etree.XMLParser(remove_blank_text=True)
    file_obj = BytesIO(etree.tostring(root1))
    tree = etree.parse(file_obj, parser)

    print()
    print(etree.tostring(root1, pretty_print=True, encoding="unicode", inclusive_ns_prefixes=True))

    try:
        with open("example.xml", "wb") as xml_writer:
            tree.write(xml_writer, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    except IOError:
        pass

    # https://www.blog.pythonlibrary.org/2014/03/26/python-creating-xml-with-lxml-objectify/
