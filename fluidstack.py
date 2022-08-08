import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


two_region = pd.DataFrame(data=[[0, 23.64, 0.265, 88.58, 2022, 'Megatron'],
                                [0, 23.64, 0.265, 91.93, 2023, 'Megatron'],
                                [0, 23.64, 0.265, 87.47, 2024, 'Megatron'],
                                [0, 47.28, 0.276, 170.61, 2022, 'Megatron'],
                                [0, 47.28, 0.276, 171.93, 2023, 'Megatron'],
                                [0, 47.28, 0.276, 172.14, 2024, 'Megatron'],
                                [0, 94.56, 0.278, 338.18, 2022, 'Megatron'],
                                [0, 94.56, 0.278, 342.43, 2023, 'Megatron'],
                                [0, 94.56, 0.278, 339.13, 2024, 'Megatron'],
                                [0, 31.52, 0.324, 91.32, 2022, 'Megatron'],
                                [0, 31.52, 0.324, 99.08, 2023, 'Megatron'],
                                [0, 31.52, 0.324, 101.31, 2024, 'Megatron'],
                                [0, 63.04, 0.350, 181.94, 2022, 'Megatron'],
                                [0, 63.04, 0.350, 176.85, 2023, 'Megatron'],
                                [0, 63.04, 0.350, 180.91, 2024, 'Megatron'],
                                [0, 126.08, 0.367, 340.69, 2022, 'Megatron'],
                                [0, 126.08, 0.367, 339.51, 2023, 'Megatron'],
                                [0, 126.08, 0.367, 349.33, 2024, 'Megatron'],
                                [0, 39.41, 0.398, 98.84, 2022, 'Megatron'],
                                [0, 39.41, 0.398, 100.04, 2023, 'Megatron'],
                                [0, 39.41, 0.398, 98.08, 2024, 'Megatron'],
                                [0, 78.82, 0.423, 188.04, 2022, 'Megatron'],
                                [0, 78.82, 0.423, 184.91, 2023, 'Megatron'],
                                [0, 78.82, 0.423, 186.09, 2024, 'Megatron'],
                                [0, 157.64, 0.448, 346.91, 2022, 'Megatron'],
                                [0, 157.64, 0.448, 343.96, 2023, 'Megatron'],
                                [0, 157.64, 0.448, 365.08, 2024, 'Megatron'],
                                [0, 117.12, 0.619, 189.38, 2022, 'Megatron'],
                                [0, 117.12, 0.619, 193.13, 2023, 'Megatron'],
                                [0, 117.12, 0.619, 185.08, 2024, 'Megatron'],
                                [0, 225.23, 0.781, 283.38, 2022, 'Megatron'],
                                [0, 225.23, 0.781, 292.82, 2023, 'Megatron'],
                                [0, 225.23, 0.781, 288.93, 2024, 'Megatron'],

                                [0, 23.64, 0.818, 30.36, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 23.64, 0.818, 29.07, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 23.64, 0.818, 27.29, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 47.28, 1.014, 49.63, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 47.28, 1.014, 46.35, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 47.28, 1.014, 43.95, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 94.56, 1.197, 78.78, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 94.56, 1.197, 80.36, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 94.56, 1.197, 77.82, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 31.52, 0.825, 34.99, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 31.52, 0.825, 41.16, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 31.52, 0.825, 38.41, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 63.04, 1.076, 61.04, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 63.04, 1.076, 57.26, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 63.04, 1.076, 57.54, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 126.08, 1.274, 99.16, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 126.08, 1.274, 97.87, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 126.08, 1.274, 99.89, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 39.41, 0.868, 43.6, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 39.41, 0.868, 45.75, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 39.41, 0.868, 46.9, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 78.82, 1.073, 72.3, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 78.82, 1.073, 75.17, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 78.82, 1.073, 72.98, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 157.64, 1.315, 120.61, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 157.64, 1.315, 120.95, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 157.64, 1.315, 118.19, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 117.12, 1.263, 92.29, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 117.12, 1.263, 95.23, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 117.12, 1.263, 90.74, 2024,
                                 'Ours (w/ Scheduler)'],
                                [0, 225.23, 1.422, 150.39, 2022,
                                 'Ours (w/ Scheduler)'],
                                [0, 225.23, 1.422, 160.7, 2023,
                                 'Ours (w/ Scheduler)'],
                                [0, 225.23, 1.422, 164.07, 2024,
                                 'Ours (w/ Scheduler)'],

                                [0, 23.64, 0.372, 60.47, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 23.64, 0.372, 65.07, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 23.64, 0.372, 64.94, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 47.28, 0.358, 128.44, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 47.28, 0.358, 136.02, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 47.28, 0.358, 131.4, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 94.56, 0.384, 239.03, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 94.56, 0.384, 260.18, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 94.56, 0.384, 238.95, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 31.52, 0.416, 76.09, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 31.52, 0.416, 74.37, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 31.52, 0.416, 76.6, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 63.04, 0.439, 139.67, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 63.04, 0.439, 152.66, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 63.04, 0.439, 138.2, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 126.08, 0.451, 272.3, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 126.08, 0.451, 288.62, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 126.08, 0.451, 277.66, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 39.41, 0.475, 85.38, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 39.41, 0.475, 81.34, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 39.41, 0.475, 81.93, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 78.82, 0.490, 163.87, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 78.82, 0.490, 166.36, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 78.82, 0.490, 152.61, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 157.64, 0.504, 315.21, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 157.64, 0.504, 305.77, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 157.64, 0.504, 317.29, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 117.12, 0.673, 175.15, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 117.12, 0.673, 177.5, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 117.12, 0.673, 169.35, 2024,
                                 'Ours (w/o Scheduler)'],
                                [0, 225.23, 0.816, 277.92, 2022,
                                 'Ours (w/o Scheduler)'],
                                [0, 225.23, 0.816, 268, 2023,
                                 'Ours (w/o Scheduler)'],
                                [0, 225.23, 0.816, 282.59, 2024,
                                 'Ours (w/o Scheduler)'],
                                ],
                          columns=['case', 'pflop', 'pflops', 'runtime', 'seed', 'system'])

cases_df = [two_region]


def plot_performance(subfig=None):
    axes = subfig.subplots(nrows=5, ncols=1, sharex=True)
    for i, df in enumerate(cases_df):
        ax = sns.barplot(ax=axes[i], data=df, x='pflop', y='runtime',
                         hue="system", hue_order=["Ours (w/ Scheduler)", "Ours (w/o Scheduler)", "Megatron"],
                         palette=["C2", "C1", "C0"],
                         alpha=0.8, ci="sd", errwidth=0.6, capsize=0.2)
        ax.set_ylabel('Runtime per iteration (s)')
        ax.set_xlabel(None)
        if i == 0:
            ax.set(ylim=(0, 200))
        if i == 1:
            ax.set(ylim=(0, 200))
        if i == 2:
            ax.set(ylim=(0, 200))
        elif i == 3:
            ax.set(ylim=(0, 600))
        elif i == 4:
            ax.set(ylim=(0, 600))

        if i == 4:
            axes[i].set_xlabel('Model Architectures')
            ax.set(xticklabels=['L24\nB1k', 'L24\nB2k', 'L24\nB4k',
                                'L32\nB1k', 'L32\nB2k', 'L32\nB4k',
                                'L40\nB1k', 'L40\nB2k', 'L40\nB4k',
                                '6.7B\nB1k', '13B\nB1k'])
            ax.get_legend().set_title(None)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles=[handles[0], handles[2], handles[1], handles[3]], labels=[labels[0], labels[2], labels[1], labels[3]],
                      loc='lower center', handletextpad=0.1, columnspacing=0.1, bbox_to_anchor=(
                0.48, -0.5), ncol=3, prop={'size': 9}, facecolor='white')
        else:
            ax.get_legend().remove()


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
plt.subplots_adjust(wspace=0.3)

ax = sns.pointplot(ax=axes[0], data=cases_df[0], x='pflop', y="pflops", hue="system", hue_order=[
    "Ours (w/ Scheduler)", "Ours (w/o Scheduler)", "Megatron"], palette=["C2", "C1", "C0"])
ax.set(ylim=(0, 1.5))
ax.set_xlabel('Model Architectures')
ax.set(xticklabels=['L24\nB1k', 'L24\nB2k', 'L24\nB4k',
                    'L32\nB1k', 'L32\nB2k', 'L32\nB4k',
                    'L40\nB1k', 'L40\nB2k', 'L40\nB4k',
                    '6.7B\nB1k', '13B\nB1k'])
ax.set_ylabel('PFLOPS')
ax.get_legend().remove()

ax = sns.barplot(ax=axes[1], data=cases_df[0], x='pflop', y='runtime',
                 hue="system", hue_order=["Ours (w/ Scheduler)", "Ours (w/o Scheduler)", "Megatron"],
                 palette=["C2", "C1", "C0"],
                 alpha=0.8, ci="sd", errwidth=0.6, capsize=0.2)
ax.set_ylabel('Runtime per iteration (s)')
ax.set_xlabel('Model Architectures')
ax.set(xticklabels=['L24\nB1k', 'L24\nB2k', 'L24\nB4k',
                    'L32\nB1k', 'L32\nB2k', 'L32\nB4k',
                    'L40\nB1k', 'L40\nB2k', 'L40\nB4k',
                    '6.7B\nB1k', '13B\nB1k'])

ax.set(ylim=(0, 400))
ax.get_legend().set_title(None)
ax.legend(loc='lower center', handletextpad=0.1, columnspacing=0.1, bbox_to_anchor=(
    -0.15, 1.05), ncol=3, prop={'size': 9}, facecolor='white')
plt.savefig("fluidstack.pdf", dpi=1000)
