import copy
from typing import Dict, Tuple, Set
from practica.joc import Accions

class Estat:
    moviments_possibles = [  # aquest ordre optimitza la cerca per profunditat
        (Accions.POSAR_PARET, "S"),
        (Accions.POSAR_PARET, "N"),
        (Accions.POSAR_PARET, "E"),
        (Accions.POSAR_PARET, "O"),
        (Accions.MOURE, "E"),
        (Accions.MOURE, "S"),
        (Accions.MOURE, "N"),
        (Accions.MOURE, "O"),
        (Accions.BOTAR, "S"),
        (Accions.BOTAR, "N"),
        (Accions.BOTAR, "E"),
        (Accions.BOTAR, "O"),
    ]
    def __init__(self, nom: str, parets: Set[Tuple[int, int]], taulell_x: int, taulell_y: int, meta: Tuple[int, int], agents: Dict[str, Tuple[int, int]],  accions = []):
        self.nom = nom,
        self.parets = parets,
        self.taulell_x = taulell_x,
        self.taulell_y = taulell_y,
        self.meta = meta,
        self.agents = agents
        self.accions = accions
        self.posicio = self.agents[self.nom]
        self.invalid = False

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        parets_hash = hash(tuple(self.parets))
        agents_hash = hash(tuple(sorted((clau, valor) for clau, valor in self.agents.items())))
        return hash((parets_hash, agents_hash))

    def es_meta(self) -> bool:
        return self.posicio[0] == self.meta[0] and self.posicio[1] == self.meta[1]

    def es_valid(self) -> bool:
        if self.posicio[0] < 0 or self.posicio[0] >= self.taulell_x or self.posicio[1] < 0 or self.posicio[1] >= self.taulell_y: #está fora del taulell
            return False

        if self.invalid: # hi ha parets duplicades, s'actualitza en crear l'estat
            return False

        for x, y in self.parets:
            if x < 0 or x >= self.taulell_x or y < 0 or y >= self.taulell_y: # hi ha parets fora de rang
                return False
            if x == self.posicio[0] and y == self.posicio[1]: # l'agent es troba sobre una paret
                return False
            if x == self.meta[0] and y == self.meta[1]: # hi ha una paret sobre la meta
                return False

        for nom, posicio in self.agents.items():
            if self.nom != nom and self.posicio == posicio: # l'agent está damunt un altre
                return False

        return True

    def genera_fill(self) -> list:
        """ Mètode per generar els estats fills.

        Genera tots els estats fills a partir de l'estat actual.

        Returns:
            Llista d'estats fills generats.
        """

        desp_moure = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "O": (-1, 0)
        }
        desp_botar = {
            "N": (0, -2),
            "S": (0, 2),
            "E": (2, 0),
            "O": (-2, 0)
        }

        estats_generats = []

        for moviment in self.moviments_possibles:
            nou_estat = copy.deepcopy(self)
            nou_estat.pare = self
            nou_estat.accions.append(moviment)

            # Calcular x, y
            desp = (0, 0)
            if moviment[0] == Accions.BOTAR:
                desp = desp_botar.get(moviment[1], (0, 0))
            elif moviment[0] in (Accions.MOURE, Accions.POSAR_PARET):
                desp = desp_moure.get(moviment[1], (0, 0))
            x, y = self.posicio[0] + desp[0], self.posicio[1] + desp[1]

            # Fer canvis
            if moviment[0] == Accions.POSAR_PARET:
                if (x, y) in nou_estat.parets:
                    nou_estat._invalid = True
                else:
                    nou_estat.parets.add((x, y))

            elif moviment[0] in (Accions.MOURE, Accions.BOTAR):
                nou_estat.posicio = (x, y)
                nou_estat.agents[nou_estat.nom] = (x, y)

            if nou_estat.es_valid():
                estats_generats.append(nou_estat)

        return estats_generats

    def calc_heuristica(self) -> int:
        return abs(self.posicio[0] - self.desti[0]) + abs(self.posicio[1] - self.desti[1])
