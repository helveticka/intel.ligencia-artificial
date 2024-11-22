import logging
import random

import numpy as np

from base import entorn
from reinforcement.abstractmodel import AbstractModel
from reinforcement.joc import Status


class AgentSARSA(AbstractModel):
    """Model de predicció SARSA (State-Action-Reward-State-Action).

    Similar a Q-learning però utilitza aprenentatge dins-política, el que significa
    que actualitza la taula Q basant-se en l'acció següent real que es prendrà,
    en lloc del valor Q màxim de l'estat següent.

    """

    default_check_convergence_every = (
        5  # by default check for convergence every # episodes
    )

    def __init__(self, game, **kwargs):
        """Create a new prediction model for 'game'.

        Args:
            game (Maze): Maze game object
            kwargs: model dependent init parameters
        """
        super().__init__(game, name="SARSAModel")
        self.Q = {}  # table with value for (state, action) combination

    def q(self, state):
        """Get q values for all actions for a certain state."""
        if type(state) is np.ndarray:
            state = tuple(state.flatten())

        q_aprox = np.zeros(len(self.environment.actions))
        i = 0
        for action in self.environment.actions:
            if (state, action) in self.Q:
                q_aprox[i] = self.Q[(state, action)]
            i += 1

        return q_aprox

    def actua(self, percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        """Policy: choose

        Args:
            percepcio: game state
        Returns:
            selected action
        """
        q = self.q(percepcio["POS"])

        actions = np.nonzero(q == np.max(q))[
            0
        ]  # get index of the action(s) with the max value
        return random.choice(actions)

    def pinta(self, display) -> None:
        pass

    def predict(self, state):
        """Policy: epsilon-greedy policy.

        :param np.ndarray state: game state
        :return int: selected action
        """
        q = self.q(state)

        actions = np.nonzero(q == np.max(q))[
            0
        ]  # get index of the action(s) with the max value
        return self.environment.actions[random.choice(actions)]

    def train(
            self,
            discount,
            exploration_rate,
            learning_rate,
            episodes,
            stop_at_convergence=False,
    ):
        cumulative_reward = 0
        cumulative_reward_history = []
        win_history = []

        for episode in range(1, episodes + 1):
            # Inicialitzar l'estat S
            state = self.environment.reset()
            # Seleccionar l'acció derivada de la política epsilon-greedy
            if np.random.random() < exploration_rate:
                action = random.choice(self.environment.actions)
            else:
                action = self.predict(state)

            while True:
                # Executar l'acció A i observar la recompensa R i el nou estat S'
                next_state, reward, status = self.environment._aplica(action)
                cumulative_reward += reward

                # Seleccionar la siguiente acción antes de actualizar Q
                if np.random.random() < exploration_rate:
                    next_action = random.choice(self.environment.actions)
                else:
                    next_action = self.predict(next_state)

                if (
                        state,
                        action,
                ) not in self.Q.keys():  # ensure value exists for (state, action)
                    # to avoid a KeyError
                    self.Q[(state, action)] = 0.0

                if (
                        next_state,
                        next_action,
                ) not in self.Q.keys():  # ensure value exists for (next_state, next_action)
                    # to avoid a KeyError
                    self.Q[(next_state, next_action)] = 0.0

                # Actualització segons SARSA
                self.Q[(state, action)] = self.Q[(state, action)] + learning_rate * (
                        reward +
                        discount * self.Q[(next_state, next_action)] -
                        self.Q[(state, action)]
                )

                if status in (
                        Status.WIN,
                        Status.LOSE,
                ):  # terminal state reached, stop episode
                    break

                # Actualitzar l'estat i l'acció
                state = next_state
                action = next_action

            cumulative_reward_history.append(cumulative_reward)

            logging.info(
                "episode: {:d}/{:d} | status: {:4s} | e: {:.5f}".format(
                    episode, episodes, status.name, exploration_rate
                )
            )
        """
            if episode % check_convergence_every == 0:
                # check if the current model does win from all starting cells
                # only possible if there is a finite number of starting states
                w_all, win_rate = self.environment.check_win_all(self)
                win_history.append((episode, win_rate))
                if w_all is True and stop_at_convergence is True:
                    logging.info("won from all start cells, stop learning")
                    break
        """

        logging.info("episodes: {:d}".format(episode))

        return cumulative_reward_history, win_history, episode