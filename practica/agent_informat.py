from queue import PriorityQueue

from practica import joc
from practica.joc import Accions
from practica.estat import Estat

class ViatgerInformat(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(ViatgerInformat, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        pass

    def cerca(self, estat_inicial: Estat) -> bool:
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put(estat_inicial)
        while not self.__oberts.empty():
            actual = self.__oberts.get()
            if actual in self.__tancats:
                continue
            if actual.es_meta():
                self.__accions = actual.accions
                return True
            estats_fills = actual.genera_fills()
            for f in estats_fills:
                self.__oberts.put(f)
            self.__tancats.add(actual)
        return False

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        if self.__accions is None:
            estat_inicial = Estat(
                nom = self.nom,
                parets = percepcio['PARETS'],
                taulell_x = len(percepcio['TAULELL']),
                taulell_y = len(percepcio['TAULELL'][0]),
                desti = percepcio['DESTI'],
                agents = percepcio['AGENTS'],
            )

            self.cerca(estat_inicial)

        if self.__accions:
            return self.__accions.pop(0)
        else:
            return Accions.ESPERAR