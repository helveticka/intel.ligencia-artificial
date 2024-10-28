from practica import agent, joc, agent_profunditat, agent_informat


def main():
    mida = (10, 10)

    agents = [
        agent_profunditat.ViatgerProfunditat("Agent profunditat", mida_taulell=mida)
        #agent_informat.ViatgerInformat("Agent informat", mida_taulell=mida)
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()


if __name__ == "__main__":
    main()
