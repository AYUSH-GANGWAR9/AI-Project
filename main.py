!pip install stable-baselines3 kaggle kagglehub shimmy

import os
import pandas as pd
import numpy as np
import gym
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback
import kagglehub

path = kagglehub.dataset_download("abdurraziq01/cloud-computing-performance-metrics")
dataset_path = os.path.join(path, "vmCloud_data.csv")

if os.path.exists(dataset_path):
    data = pd.read_csv(dataset_path)
else:
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

irrelevant_columns = ['timestamp', 'vm_id']
data.drop(columns=irrelevant_columns, inplace=True, errors='ignore')

data.fillna(data.mean(numeric_only=True), inplace=True)

categorical_columns = data.select_dtypes(include=['object']).columns
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

scaler = MinMaxScaler()
numeric_columns = data.select_dtypes(include=[np.number]).columns
data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

data = data.sample(n=500, random_state=42).reset_index(drop=True)

class CloudResourceEnv(gym.Env):
    def __init__(self, data):
        super(CloudResourceEnv, self).__init__()
        self.data = data.values
        self.current_step = 0
        self.action_space = gym.spaces.Discrete(data.shape[1])
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(data.shape[1],), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        return self.data[self.current_step]

    def step(self, action):
        target_utilization = 0.7
        resource_utilization = self.data[self.current_step, action]
        if resource_utilization > target_utilization:
            penalty = -0.5 * (resource_utilization - target_utilization)
        elif resource_utilization < target_utilization:
            penalty = -0.2 * (target_utilization - resource_utilization)
        else:
            penalty = 0
        reward = 1 - abs(resource_utilization - target_utilization) + penalty
        self.current_step += 1
        done = self.current_step >= len(self.data)
        next_state = self.data[self.current_step] if not done else self.reset()
        return next_state, reward, done, {}

env = DummyVecEnv([lambda: CloudResourceEnv(data)])

model = PPO(
    "MlpPolicy",
    env,
    verbose=0,
    learning_rate=0.0003,
    ent_coef=0.005,
    n_steps=512,
    batch_size=64,
    policy_kwargs=dict(net_arch=[64, 64]),
)
eval_callback = EvalCallback(env, eval_freq=1000, n_eval_episodes=1000, verbose=0)
model.learn(total_timesteps=20000, callback=eval_callback)

model.save("ppo_cloud_resource_optimized_high_iters")

obs = env.reset()
total_rewards = []
cumulative_reward = 0
for episode in range(100):
    obs = env.reset()
    episode_reward = 0
    while True:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        episode_reward += reward
        if done:
            break
    total_rewards.append(episode_reward)

average_reward = np.mean(total_rewards)
std_reward = np.std(total_rewards)
max_reward = np.max(total_rewards)
min_reward = np.min(total_rewards)
print(f"Average Reward over 100 Episodes: {average_reward}")
print(f"Standard Deviation of Reward: {std_reward}")
print(f"Maximum Reward: {max_reward}")
print(f"Minimum Reward: {min_reward}")
