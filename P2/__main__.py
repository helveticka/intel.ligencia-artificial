import logging

from P2.agent import AgentQ, AgentSARSA
from P2.joc import Laberint


def main():
    logging.basicConfig(
        format="%(levelname)-8s: %(asctime)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )  # Only show messages *equal to or above* this level

    game = Laberint()
    agent = AgentSARSA(game)
    h, w, _ = agent.train(
        discount=0.90,
        exploration_rate=0.10,
        learning_rate=0.6,
        episodes=2000,
        stop_at_convergence=True,
    )

    game.reset()
    game.set_agent([agent])
    game.comencar()


if __name__ == "__main__":
    main()
