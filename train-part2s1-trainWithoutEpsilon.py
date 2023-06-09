import gym
import numpy as np

env = gym.make("MountainCar-v0", render_mode="human")

LEARNING_RATE = 0.1

DISCOUNT = 0.95
EPISODES = 25000

DISCRETE_OS_SIZE = [20, 20]
discrete_os_win_size = (env.observation_space.high - env.observation_space.low)/DISCRETE_OS_SIZE

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))


def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low)/discrete_os_win_size
    return tuple(discrete_state.astype(np.int8))  # we use this tuple to look up the 3 Q values for the available actions in the q-table


discrete_state = get_discrete_state(env.reset()[0])
done = False
while not done:

    action = np.argmax(q_table[discrete_state])
    new_state, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated

    new_discrete_state = get_discrete_state(new_state)

    env.render()
    #new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

    # If simulation did not end yet after last step - update Q table
    if not done:

        # Maximum possible Q value in next step (for new state)
        max_future_q = np.max(q_table[new_discrete_state])

        # Current Q value (for current state and performed action)
        current_q = q_table[discrete_state + (action,)]

        # And here's our equation for a new Q value for current state and action
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        # Update Q table with new Q value
        q_table[discrete_state + (action,)] = new_q


    # Simulation ended (for any reson) - if goal position is achived - update Q value with reward directly
    elif new_state[0] >= env.goal_position:
        #q_table[discrete_state + (action,)] = reward
        q_table[discrete_state + (action,)] = 0

    discrete_state = new_discrete_state


env.close()