import logging
import random

import numpy as np

from base import entorn
from reinforcement.abstractmodel import AbstractModel
from reinforcement.joc import Status


class AgentSARSA(AbstractModel):
    """Tabular SARSA (State-Action-Reward-State-Action) prediction model.

    Similar to Q-learning but uses on-policy learning, meaning it updates the Q-table
    based on the actual next action that will be taken, rather than the maximum Q-value
    of the next state.
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
        super().__init__(game, name="QTableModel")
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
        """Policy: choose the action with the highest value from the Q-table. Random choice if
        multiple actions have the same (max) value.

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
        """Policy: choose the action with the highest value from the Q-table.
        Random choice if multiple actions have the same (max) value.

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
            state = self.environment.reset()
            # Cambio principal 1: Seleccionar la primera acción al inicio del episodio
            action = self.select_action(state, exploration_rate)

            while True:
                # Ejecutar la acción seleccionada
                next_state, reward, status = self.environment._aplica(action)
                cumulative_reward += reward

                # Cambio principal 2: Seleccionar la siguiente acción antes de actualizar Q
                next_action = self.select_action(next_state, exploration_rate)

                # Asegurar que existe el valor para (estado, acción)
                if (state, action) not in self.Q:
                    self.Q[(state, action)] = 0.0

                # Asegurar que existe el valor para (siguiente_estado, siguiente_acción)
                if (next_state, next_action) not in self.Q:
                    self.Q[(next_state, next_action)] = 0.0

                # Cambio principal 3: Actualización SARSA
                # En lugar de usar el máximo Q-valor del siguiente estado,
                # usamos el Q-valor de la siguiente acción que realmente tomaremos
                self.Q[(state, action)] = self.Q[(state, action)] + learning_rate * (
                        reward +
                        discount * self.Q[(next_state, next_action)] -
                        self.Q[(state, action)]
                )

                if status in (Status.WIN, Status.LOSE):
                    break

                # Cambio principal 4: Actualizar estado y acción para el siguiente paso
                state = next_state
                action = next_action

            cumulative_reward_history.append(cumulative_reward)

            logging.info(
                "episode: {:d}/{:d} | status: {:4s} | e: {:.5f}".format(
                    episode, episodes, status.name, exploration_rate
                )
            )

        logging.info("episodes: {:d}".format(episode))
        return cumulative_reward_history, win_history, episode

    def select_action(self, state, exploration_rate):
        """Selecciona una acción usando política ε-greedy."""
        if np.random.random() < exploration_rate:
            return random.choice(self.environment.actions)
        else:
            return self.predict(state)