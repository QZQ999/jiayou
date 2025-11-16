"""
纯Python版本的cython_func - Windows兼容
替代 cython_func.pyx，无需编译

功能：历史观察滚动（用于LSTM等时序模型）
"""
import numpy as np

def roll_hisory(obs_feed_new, prev_obs_feed, valid_mask, N_valid, next_his_pool):
    """
    滚动历史观察数组

    参数:
        obs_feed_new: 新观察 [n_threads, n_agents, max_entities, obs_dim]
        prev_obs_feed: 历史观察 [n_threads, n_agents, max_entities, obs_dim]
        valid_mask: 有效掩码 [n_threads, n_agents, max_entities]
        N_valid: 有效实体数量 [n_threads, n_agents]
        next_his_pool: 输出缓冲区 [n_threads, n_agents, max_entities, obs_dim]

    返回:
        滚动后的历史观察数组
    """
    vmax = N_valid.shape[0]  # n_threads
    wmax = N_valid.shape[1]  # n_agents
    max_obs_entity = obs_feed_new.shape[2]

    for th in range(vmax):
        for a in range(wmax):
            pointer = 0
            # 收集有效的新观察
            for k in range(max_obs_entity):
                if valid_mask[th, a, k]:
                    next_his_pool[th, a, pointer] = obs_feed_new[th, a, k]
                    pointer += 1

            # 补充历史观察
            n_v = N_valid[th, a]
            for k in range(n_v, max_obs_entity):
                next_his_pool[th, a, k] = prev_obs_feed[th, a, k - n_v]

    return np.asarray(next_his_pool)
