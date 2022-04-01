# RDMOCatalogBuilder

RDMOCatalogBuilder provides a small application to build a catalog for usage in RDMO
(https://github.com/rdmorganiser/rdmo). A single json structure has to be built that includes all necessary information
for the catalog. The json file serves as a basis for the production of xml files to be uploaded in RDMO (according
rights have to be admitted by the RDMO administrator).

## Usage

To use RDMOCatalogBuilder type the following:

```python
from BuildCatalog import *
control_create_catalog("infiles/qa_questionnaire.json")
```

This produces an example catalog resource for qa_questionnaire.json. Basically the json file is built according the
catalog settings: a catalog has sections, each section has questionsets with questions. Each part has a key that is used
for the uri (no spaces allowed). The other fields within each catalog part are based on their requirements according to
https://rdmo.readthedocs.io/en/latest/management/ . Please take qa_questionnaire.json as an example

## Structure

The package RDMOEntities includes classes of all parts of the RDMO data model. These classes inherit from RDMOEntities
class; a make_element method is therefore mandatory. BuildCatalog.py is the central file. The input json can be either
directly written into the main method or used like in usage before.

## Output Files

The following contents for RDMO are produced as xml files:

- questions
- domain
- options
- conditions
- tasks

## Documentation and json Structure Examples

In a stock RDMO, administrators can establish new catalogs using the management pages of RDMO. This is mainly manual
work with a little help via the GUI. Here, the Python package RDMOCatalogBuilder takes effect. The main development goal
of RDMOCatalogBuilder was a "write once use multiple" concept. A json file filled with all necessary information serves
as singular input for the script. The main script parses the json file and builds five xml files for questions, domain,
options, conditions, and tasks. Each xml file has the correct format for the import via the RDMO management pages.
RDMOCatalogBuilder implements all necessary links, e.g. it automatically adds appropriate attributes to the domain for
each question following a tree structure with a starting url prefix. If requested, conditions are properly linked to the
according attributes. The structure of the input json file is build along the questionnaire elements as given in the
RDMO management documentation (https://rdmo.readthedocs.io/en/latest/management/questions.html). First, three key are
defined: "prefix_outfile" stating the prefix for all RDAMOCatalogBuilder-written files, "uri_prefix" defining the uri
prefix as used in RDMO, and "namespace" as an object for prefix and url to used namespaces (so far, only "dc" is used
for dc:uri element). Second, the key "catalog" has an object with mandatory key named "key" (used for defining the url,
key, path, and attribute in RDMO) and keys as given in RDMO documentation (e.g. title or help). Further, the catalog
object contains a key named "section" with an array of objects. Here, for each object of the array we use again the
mandatory "key" as in "catalog" and the section-keys as stated in the RDMO documentation. The section than subdivides
into questionsets and the latter into questions, each with basically the same structure as "section". Each key with
potentially multiple localizations must be given as object with the according language abbreviations as key (e.g. "en",
"de", "fr", "es", "it") and the according string as value, e.g. the title or help text can be given in different
languages. The RDMO instance must be set up for using the languages. A minimal example is given in the code-block below.

```json
{
  "prefix_outfile": "prefixName",
  "uri_prefix": "https://path.to/uri/prefix",
  "namespace": {
    "prefix": "dc",
    "url": "http://purl.org/dc/elements/1.1/"
  },
  "catalog": {
    "key": "catalogName",
    "title": {
      "en": "titleEnglish",
      "de": "titleGerman"
    }
    "section": [
      {
        "key": "sectionName",
        "questionset": [
          {
            "key": "questionsetName",
            "question": [
              {
                "key": "questionName"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

A questionset can be defined as a collection using the key "is_collection" from the RDMO documentation and an additional
name of the collection "collection_name" (see code-block below). The latter serves as an identifier that can be used in
each questionset in the json structure. Using the same identifier in different questionsets results in the same dataset
collection for both questionsets in the RDMO questionnaire.

```json
{
  "questionset": [
    {
      "key": "questionsetName",
      "is_collection": "True",
      "collection_name": "collectionName",
      "question": [
        {
          ...
        }
      ]
    }
  ]
}
```

The questions can refer to a set of options. RDMOCatalogBuilder expects the optionset as part of the question (
code-block below). Although once defined, the "key" of the optionset can be used multiple times in the json structure
without the need of typing the whole options again. It is then sufficient to write the appropriate key into "optionset"
object.

```json
{
  "question": [
    {
      "key": "questionName",
      "widget_type": "select",
      "value_type": "option",
      "optionset": {
        "key": "optionsetName",
        "option": [
          {
            "key": "1",
            "text": {
              "en": "firstOptionName",
              "de": "nameErsteOption"
            }
          },
          {
            "key": "2",
            "text": {
              "en": "secondOptionName",
              "de": "nameZweiteOption"
            }
          }
        ]
      }
    }
  ]
}
```

A condition refers to an attribute that is filled with a question's answer. RDMOCatalogBuilder assumes the condition's
definition in one question and its usage in another question, questionset, or task. The condition defines, whether a
question, questionset, or task can be seen by the questionnaire user in RDMO. The key "condition_definition" is an array
of conditions defined upon the answer of the question (multiple conditions are allowed). It comprises a "key" as an
identifier and the "relation" as one of the following: "eq" - equal to, "neq" - not equal to, "contains", "gt" - greater
than, "gte" - greater than or equal to, "lt" - lower than, "lte" - lower than or equal to, "empty", "notempty". If "
relation" only refers to "empty" or "notempty", no further key must be given. Otherwise, if "relation" relies on a
comparison, a "target_text" must be given (first code-block below). An exception exists, if "relation" depends on a
particular option in an optionset. This case demands given values for "optionset" and "target_option" (second code-block
below).

A question with "condition" can also define (multiple) conditions to be used elsewhere.

```json
{
  "question": [
    {
      "key": "questionName1",
      "condition_definition": [
        {
          "key": "question1True",
          "relation": "eq",
          "target_text": "1"
        }
      ]
    },
    {
      "key": "questionName2",
      "condition": "question1True"
    }
  ]
}
```

```json
{
  "question": [
    {
      "key": "questionName1",
      "optionset": {
        "key": "optionsetName",
        "option": [
          {
            "key": "1",
            "text": {
              "en": "firstOptionName"
            }
          },
          {
            "key": "2",
            "text": {
              "en": "secondOptionName"
            }
          }
        ]
      }



      "condition_definition": [
        {
          "key": "question1Is2",
          "relation": "eq",
          "optionset": "optionsetName",
          "target_option": "2"
        }
      ]
    },
    {
      "key": "questionName2",
      "condition": "question1Is2"
    }
  ]
}
```

Tasks are displayed in RDMO if their condition is true. For RDMOCatalogBuilder, tasks are defined as array of objects
after the catalog. A task includes a "key", a "title", and the "condition" defined in the catalog before. The code-block
below shows an example task.

```json
{
  "catalog": {
    ...
  },
  "task": [
    {
      "key": "taskName",
      "title": {
        "en": "titleEnglish"
      },
      "condition": "question1Is2"
    }
  ]
}
```

The keys for catalog, section, questionset, question, optionset, option, condition, and task have the same wording as
the appropriate parameters in the RDMO documentation. In the case of extension or change of the parameters from the RDMO
side, RDMOCatalogBuilder can easily be tailored. All the parameters/keys (RDMO/json wording) are defined in the package
RDMOEntities. Additional entries in these classes must be complemented in the appropriate BuildCatalog.py method (e.g.
create_options for add-ons in RDMO option parameters). This schema eases the adaption to new content in RDMO.

The five xml files written by RDMOCatalogBuilder are advised to be imported in RDMO in the right order. First, the
domain xml file defining all attributes must be imported to allocate the necessary variables. The options and the
conditions xml files can be imported secondly. Third follows the import of the questions xml file. The tasks xml file
import finalizes the new RDMO catalog. We suggest establishing a uri_prefix that is unique on the target RDMO instance.
This ensures easier findability of the newly created RDMO elements and therefore their easier replacing or removing.

## Known Limitations/Bugs

Per json file only one catalog is allowed. Currently, RDMOCatalogBuilder implements the catalog features of RDMO 1.8
except the following:

- Catalog: Groups (only available via GUI)
- Catalog: Sites
- Option: Provider (dynamic options only usable via plugin)
- Task: Sites

## License

The RDMOCatalogBuilder is licensed under Apache-2.0. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

## Contact

Michael Wagner ([michael.wagner@tu-dresden.de](mailto:michael.wagner@tu-dresden.de))