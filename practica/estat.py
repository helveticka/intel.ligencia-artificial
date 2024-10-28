from typing import Dict, Tuple, Set


class Estat:
    def __init__(self, nom: str, parets: Set[Tuple[int, int]], taulell_x: int, taulell_y: int, meta: Tuple[int, int], agents: Dict[str, Tuple[int, int]],  accions = []):
        self.nom = nom,
        self.parets = parets,
        self.taulell_x = taulell_x,
        self.taulell_y = taulell_y,
        self.meta = meta,
        self.agents = agents
        self.accions = accions

