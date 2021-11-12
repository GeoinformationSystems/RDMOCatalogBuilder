# RDMOCatalogBuilder
RDMOCatalogBuilder provides a small application to build a catalog for usage in RDMO
(https://github.com/rdmorganiser/rdmo). A single json has to be built that includes all necessary information for the
catalog. The json file serves as a basis for the production of xml files to be uploaded in RDMO (according rights have
to be admitted by the RDMO administrator).

## Usage
To use RDMOCatalogBuilder type the following:

```
from BuildCatalog import *
control_create_catalog("qa_questionnaire.json")
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

## Known Limits/Bugs
Per json file only one catalog is allowed. Currently RDMOCatalogBuilder implements the catalog features of RDMO
1.5.5. An upgrade to RDMO 1.6.x is planned for the near future.

## License
The RDMOCatalogBuilder is licensed under Apache-2.0. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

## Contact
Michael Wagner ([michael.wagner@tu-dresden.de](mailto:michael.wagner@tu-dresden.de))