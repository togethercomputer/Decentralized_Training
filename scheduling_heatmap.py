import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import config


simulate_cases = [
    config.simulate_0_datacenter,
    config.simulate_1_datacenter_spot_gpu,
    config.simulate_2_multi_universities,
    config.simulate_3_regional_geo_distributed,
    config.simulate_4_worldwide_geo_distributed
]

fig, axes = plt.subplots(nrows=5, ncols=2, sharex=True,
                         sharey=True, figsize=(6, 12))
sns.set_theme()

for i, simulate_case in enumerate(simulate_cases):
    peer_delay, peer_bandwidth, regions = simulate_case()
    ax = sns.heatmap(ax=axes[i, 0], data=pd.DataFrame(peer_delay, index=list(range(config.nodes)), columns=list(range(
        config.nodes))), vmin=0, vmax=max(1, np.amax(peer_delay)), xticklabels=8, yticklabels=8, linewidths=0.001, square=True, cbar_kws={'label': 'Delay(ms)'})
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    ax = sns.heatmap(ax=axes[i, 1], data=pd.DataFrame(peer_bandwidth, index=list(range(config.nodes)), columns=list(range(
        config.nodes))), vmin=0, vmax=np.amax(peer_bandwidth), xticklabels=8, yticklabels=8, linewidths=0.001, square=True, cbar_kws={'label': 'Bandwidth(Gbps)'})

fig.supxlabel("Node IDs")
fig.supylabel("Node IDs")
plt.savefig("scheduling_heatmap.eps", dpi=300)
# plt.show()
