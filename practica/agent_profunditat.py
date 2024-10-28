from practica import joc
from practica.joc import Accions
from practica.estat import Estat

class ViatgerProfunditat(joc.Viatger):
    def _init_(self, *args, **kwargs):
        super(ViatgerProfunditat, self)._init_(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        pass

    def cerca(self, estat_inicial: Estat) -> bool:
        self.__oberts = [estat_inicial]
        self.__tancats = set()
        trobat = False

        actual = None
        while self.__oberts:
            actual = self.__oberts.pop(-1)
            if actual in self.__tancats:
                continue
            if actual.es_meta():
                self.__accions = actual.accions
                trobat = True
                break

            for f in actual.genera_fills():
                self.__oberts.append(f)

            self.__tancats.add(actual)

        return trobat

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