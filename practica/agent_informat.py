from practica import joc
from practica.joc import Accions
from queue import PriorityQueue


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
        sortir = False

        self.__oberts.put((estat_inicial.calc_heuristica(), estat_inicial))

        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            print(actual)
            if actual in self.__tancats:
                continue
            if actual.es_meta():
                break
            estats_fills = actual.genera_fills()
            for estat_f in estats_fills:
                self.__oberts.put((estat_f.calc_heuristica(), estat_f))
            self.__tancats.add(actual)
            if actual.es_meta():
                self.__accions = actual.accions_previes
                sortir = True
            return sortir

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        if self.__accions is None:
            estat_inicial = Estat(
                nom = self.nom,
                parets = percepcio['PARETS'],
                taulell_x = len(percepcio['TAULELL']),
                taulell_y = len(percepcio['TAULELL'][0]),
                meta = percepcio['META'],
                agents = percepcio['AGENTS'],
            )

            self.cerca(estat_inicial)

        if self.__accions:
            return self.__accions.pop(0)
        else:
            return Accions.ESPERAR