from practica import agent, joc, agent_informat, agent_profunditat


def main():
    mida = (10, 10)

    agents = [
        agent_profunditat.ViatgerProfunditat("Agent 1", mida_taulell=mida)
        #agent_informat.ViatgerInformat("Agent 1", mida_taulell=mida)
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()


if __name__ == "__main__":
    main()
