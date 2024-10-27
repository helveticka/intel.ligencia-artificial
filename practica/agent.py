import random

from queue import PriorityQueue
from practica import joc
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)

    def distancia_manhattan(self, origen, desti):
        return abs(origen[0] - desti[0]) + abs(origen[1] - desti[1])

    def successors(self, posicio, parets, n):
        # genera els moviments possibles
        moviments = {
            "N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)
        }
        successors = []

        # moure
        for direccio, (dx, dy) in moviments.items():
            nx, ny = posicio[0] + dx, posicio[1] + dy
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in parets:
                successors.append(((nx, ny), Accions.MOURE, direccio, 1))  # Cost 1

        # botar
        for direccio, (dx, dy) in moviments.items():
            nx, ny = posicio[0] + 2 * dx, posicio[1] + 2 * dy
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in parets:
                successors.append(((nx, ny), Accions.BOTAR, direccio, 2))  # Cost 2

        return successors

    def pinta(self, display):
        pass

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        origen = percepcio['AGENTS']['NOM_AGENT']
        desti = percepcio['DESTI']
        parets = set(percepcio['PARETS'])
        n = len(percepcio['TAULELL'])

        # cua de prioritat A*
        frontier = PriorityQueue()
        frontier.put((0, origen))
        came_from = {origen: None}
        cost_so_far = {origen: 0}

        while not frontier.empty():
            _, actual = frontier.get()

            # si hem arribat, reconstruir el cami
            if actual == desti:
                return self.reconstrueix_cami(came_from, origen, desti)

            # expandir els successors
            for next, accio, direccio, cost in self.successors(actual, parets, n):
                nou_cost = cost_so_far[actual] + cost
                if next not in cost_so_far or nou_cost < cost_so_far[next]:
                    cost_so_far[next] = nou_cost
                    priority = nou_cost + self.distancia_manhattan(next, desti)
                    frontier.put((priority, next))
                    came_from[next] = (accio, direccio)

        # sino, esperar
        return Accions.ESPERAR

    def reconstrueix_cami(self, came_from, origen, desti):
        actual = desti
        cami = []
        while actual != origen:
            accio, direccio = came_from[actual]
            cami.append((accio, direccio))
            dx, dy = {"N": (1, 0), "S": (-1, 0), "E": (0, -1), "O": (0, 1)}[direccio]
            actual = (actual[0] - dx, actual[1] - dy)
        cami.reverse()
        return cami[0]  # Retorna la primera acció a executar