import copy
from typing import Tuple, Dict, Set

from practica.joc import Accions


class Estat:
    #Tots el possibles moviments. Primer els moviments que més canvis poden provocar,
    #llavors els moviments més simples i, per acabar, els moviments més complexos
    moviments_possibles = [
        (Accions.POSAR_PARET, "N"),
        (Accions.POSAR_PARET, "S"),
        (Accions.POSAR_PARET, "E"),
        (Accions.POSAR_PARET, "O"),
        (Accions.MOURE, "N"),
        (Accions.MOURE, "S"),
        (Accions.MOURE, "E"),
        (Accions.MOURE, "O"),
        (Accions.BOTAR, "N"),
        (Accions.BOTAR, "S"),
        (Accions.BOTAR, "E"),
        (Accions.BOTAR, "O"),
    ]

    def __init__(self, nom: str, parets: Set[Tuple[int, int]], taulell_x: int, taulell_y: int, meta: Tuple[int, int], agents: Dict[str, Tuple[int, int]], accions = []):
        self._nom = nom
        self._parets = parets
        self._taulell_x = taulell_x
        self._taulell_y = taulell_y
        self._meta = meta
        self._agents = agents
        self._posicio = self._agents[self._nom]
        self.accions = accions

    #Realitza la funció Hash identificant les parets i els agents per aquest estat
    def __hash__(self):
        parets_hash = hash(tuple(self._parets))
        agents_hash = hash(tuple(sorted((c, v) for c, v in self._agents.items())))
        return hash((parets_hash, agents_hash))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def es_meta(self) -> bool:
        #Comprobam si la posició és la mateixa que la de la meta tant a x com a y.
        return self._posicio[0] == self._meta[0] and self._posicio[1] == self._meta[1]

    def es_valid(self) -> bool:
        #Miram si la posició està fora del limits del taulell. Si ho està, retornam False
        if self._posicio[0] < 0 or self._posicio[0] >= self._taulell_x or self._posicio[1] < 0 or self._posicio[1] >= self._taulell_y:
            return False

        #Per totes les coordenades de les parets comprobam si:
        #   - L'agent es troba sobre una paret
        #   - Si hi ha una paret sobre la meta.
        #Tornant False si es compleix alguna d'aquestes comprobacions.
        for coordx, coordy in self._parets:
            if coordx == self._posicio[0] and coordy == self._posicio[1]:
                return False
            if coordx == self._meta[0] and coordy == self._meta[1]:
                return False

        return True

    def genera_fills(self) -> list:
        moure = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "O": (-1, 0)
        }
        botar = {
            "N": (0, -2),
            "S": (0, 2),
            "E": (2, 0),
            "O": (-2, 0)
        }

        estats_fills = []
        for moviment in self.moviments_possibles:
            fill = copy.deepcopy(self)
            fill.pare = self
            fill.accions.append(moviment)

            x, y = self.calcular_posicio(moviment, botar, moure)
            self.aplicar_canvi(fill, x, y, moviment)

            if fill.es_valid():
                estats_fills.append(fill)

        return estats_fills

    def calcular_posicio(self, moviment, botar, moure):
        desp = (0, 0)

        if moviment[0] == Accions.BOTAR:
            desp = botar.get(moviment[1], (0, 0))
        elif moviment[0] in (Accions.MOURE, Accions.POSAR_PARET):
            desp = moure.get(moviment[1], (0, 0))

        x = self._posicio[0] + desp[0]
        y = self._posicio[1] + desp[1]

        return x, y

    def aplicar_canvi(self, nou_estat, x, y, moviment):
        if moviment[0] == Accions.POSAR_PARET:
            if (x, y) in nou_estat._parets:
                nou_estat._invalid = True
            else:
                nou_estat._parets.add((x, y))
        elif moviment[0] in (Accions.MOURE, Accions.BOTAR):
            nou_estat._agents[nou_estat._nom] = (x, y)
            nou_estat._posicio = (x, y)

    def __lt__(self, other):
        #Ens ajuda a comparar entre el valor d'aquest estat amb el que es troba dins la PriorityQueue
        #tenguent en compte el valor (heurística + cost)
        if self.calcular_valor() == other.calcular_valor():
            return self.heuristica() < other.heuristica()

        return self.calcular_valor() < other.calcular_valor()

    def calcular_valor(self):
        return self.heuristica() + self.cost()

    def heuristica(self) -> int:
        #L'heurística que feim servir es la distància de Manhattan
        return abs(self._posicio[0] - self._meta[0]) + abs(self._posicio[1] - self._meta[1])

    def cost(self) -> int:
        costs = {
            Accions.ESPERAR: 0,
            Accions.MOURE: 1,
            Accions.BOTAR: 2,
            Accions.POSAR_PARET: 4,
        }
        cost = 0
        for accio,coordenada in self.accions:
            cost += costs[accio]

        return cost