#  @author: Michael Wagner
#  @organization: TU Dresden
#  @contact: michael.wagner@tu-dresden.de

from abc import ABC, abstractmethod


class RDMOEntities(ABC):
    @abstractmethod
    def make_element(self):
        pass
