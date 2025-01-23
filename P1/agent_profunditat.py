from P1 import joc
from P1.joc import Accions
from P1.estat import Estat

class ViatgerProfunditat(joc.Viatger):

    def __init__(self, *args, **kwargs):
        super(ViatgerProfunditat, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        pass

    def cerca(self, estat_inicial: Estat) -> bool:
        #Inicialitzam les estructures necesàries per gestionar els estats oberts (amb la inserció de l'estat inicial)
        #i tancats
        self.__oberts = [estat_inicial]
        self.__tancats = set()
        trobat = False

        actual = None
        #Mentre hi hagui estats a __oberts, comprovam:
        #   - Si l'estat actual està visitat (passam)
        #   - Si l'estat actual és la meta (break y possam trobat a True)
        while self.__oberts:
            actual = self.__oberts.pop(-1)
            if actual in self.__tancats:
                continue
            if actual.es_meta():
                self.__accions = actual.accions
                trobat = True
                break

            #Per cada fill de la llista que genera el mètode, l'insertam a __oberts.
            for f in actual.genera_fills():
                self.__oberts.append(f)

            #Consideram l'estat actual visitat i el tancam.
            self.__tancats.add(actual)

        return trobat

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        #Si no hi ha accions a aquesta instancia, passam l'estat inicial al mètode de cerca
        if self.__accions is None:
            estat_inicial = Estat(
                nom=self.nom,
                parets=percepcio['PARETS'],
                taulell_x=len(percepcio['TAULELL']),
                taulell_y=len(percepcio['TAULELL'][0]),
                meta=percepcio['DESTI'],
                agents=percepcio['AGENTS'],
            )

            self.cerca(estat_inicial)

        if self.__accions:
            return self.__accions.pop(0)
        else:
            return Accions.ESPERAR
