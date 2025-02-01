import math
from queue import PriorityQueue
from agent import Viatger
from practica import joc
from practica.joc import Accions, Laberint
from estat import Estat
class AgentMinimax(joc.Viatger):
    PODA = True
    def __init__(self, *args, **kwargs):
        super(AgentMinimax, self).__init__(*args, **kwargs)
        self.max_depth = 4

        self.__visitats = {}

    def processar_node(self, estat, alfa: float, beta: float, profunditat, tornMax, agents):
        if profunditat >= self.max_depth:
            return estat.heuristicaMinimax(agents[self.nom] if tornMax else agents[self.getOther(self.nom, agents)])

        valor = None
        self.__oberts.append(estat)
        fills = estat.genera_fills()

        for s in fills:
            #si ja s'ha processat o esta pendent de ser processat
            if s in self.__tancats or s in self.__oberts:
                continue #se salta la iteració
            #valor maxim o minim
            valor_nodo = self.processar_node(s, alfa, beta, profunditat + 1, not tornMax, agents)
            #si encara no tenim valor o es major que alfa o menor que beta
            if (valor is None) or (tornMax and valor_nodo > valor) or (not tornMax and valor_nodo < valor):
                valor = valor_nodo
                #si hem arribat al node superior
                if profunditat == 0:
                    self.accio_final = s.cami[0]
                if tornMax: #si es el torn de max, actualitzam alfa
                    alfa = valor
                else:
                    beta = valor #si no, beta

            if alfa >= beta:
                break

        self.__oberts.pop(-1) #ho treim de estats no visitats (perque ja hem acabat de processar-ho)
        self.__tancats.add(estat) #ho marcam com a visitats

        return valor

    def cerca(self, estat_inicial, agents):
        self.accio_final = Accions.ESPERAR
        self.__oberts = []
        self.__tancats = set()
        self.processar_node(estat_inicial, float("-inf"), float("+inf"), 0, True, agents)
        return self.accio_final
    def getOther(self, nom, agents : dict):
        """
        Retorna l'altre tipus de casella, si és lliure retorna lliure
        """
        noms = list(agents.keys())
        if nom == noms[0]:
            return noms[1]
        else:
            return noms[0]


    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        estat_inicial = Estat(parets=percepcio["PARETS"], desti=percepcio["DESTI"],
                              agent=percepcio["AGENTS"][self.nom], taulell= percepcio["TAULELL"])

        solucio = self.cerca(estat_inicial, percepcio["AGENTS"])
        if solucio:
            return solucio
        return Accions.ESPERAR