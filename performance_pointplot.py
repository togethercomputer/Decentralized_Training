import enum
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


case_0_df = pd.DataFrame(data=[[0, 23.64, 1.888, 12.52, 'Megatron'],
                               [0, 47.28, 1.914, 24.70, 'Megatron'],
                               [0, 94.56, 1.933, 48.91, 'Megatron'],
                               [0, 31.52, 2.049, 15.38, 'Megatron'],
                               [0, 63.04, 2.066, 30.51, 'Megatron'],
                               [0, 126.08, 2.090, 60.32, 'Megatron'],
                               [0, 39.41, 2.087, 18.88, 'Megatron'],
                               [0, 78.82, 2.138, 36.87, 'Megatron'],
                               [0, 157.64, 2.161, 72.96, 'Megatron'],

                               [0, 23.64, 1.604, 14.74, 'Deepspeed'],
                               [0, 47.28, 1.649, 28.68, 'Deepspeed'],
                               [0, 94.56, 1.613, 58.61, 'Deepspeed'],
                               [0, 31.52, 1.399, 25.31, 'Deepspeed'],
                               [0, 63.04, 1.407, 46.35, 'Deepspeed'],
                               [0, 126.08, 1.541, 90.62, 'Deepspeed'],
                               [0, 39.41, 1.651, 38.38, 'Deepspeed'],
                               [0, 78.82, 1.636, 73.98, 'Deepspeed'],
                               [0, 157.64, 1.786, 148.49, 'Deepspeed'],

                               [0, 23.64, 2.331, 10.14, 'Ours (w/ Scheduler)'],
                               [0, 47.28, 2.683, 17.62, 'Ours (w/ Scheduler)'],
                               [0, 94.56, 2.866, 32.99, 'Ours (w/ Scheduler)'],
                               [0, 31.52, 2.365, 13.33, 'Ours (w/ Scheduler)'],
                               [0, 63.04, 2.715, 23.22, 'Ours (w/ Scheduler)'],
                               [0, 126.08, 2.925, 43.10,
                                   'Ours (w/ Scheduler)'],
                               [0, 39.41, 2.360, 16.70, 'Ours (w/ Scheduler)'],
                               [0, 78.82, 2.665, 29.58, 'Ours (w/ Scheduler)'],
                               [0, 157.64, 2.930, 53.80,
                                   'Ours (w/ Scheduler)'],

                               [0, 23.64, 1.166, 20.27,
                                   'Ours (w/o Scheduler)'],
                               [0, 47.28, 1.422, 33.25,
                                   'Ours (w/o Scheduler)'],
                               [0, 94.56, 1.438, 65.78,
                                   'Ours (w/o Scheduler)'],
                               [0, 31.52, 1.365, 23.09,
                                   'Ours (w/o Scheduler)'],
                               [0, 63.04, 1.599, 39.43,
                                   'Ours (w/o Scheduler)'],
                               [0, 126.08, 1.607, 78.47,
                                   'Ours (w/o Scheduler)'],
                               [0, 39.41, 1.610, 24.48,
                                   'Ours (w/o Scheduler)'],
                               [0, 78.82, 1.763, 44.71,
                                   'Ours (w/o Scheduler)'],
                               [0, 157.64, 1.776, 88.74,
                                   'Ours (w/o Scheduler)'],
                               ],
                         columns=['case', 'pflop', 'pflops', 'runtime', 'system'])

case_1_df = pd.DataFrame(data=[[1, 23.64, 1.109, 21.31, 'Megatron'],
                               [1, 47.28, 1.116, 42.37, 'Megatron'],
                               [1, 94.56, 1.132, 83.57, 'Megatron'],
                               [1, 31.52, 1.360, 23.18, 'Megatron'],
                               [1, 63.04, 1.443, 43.68, 'Megatron'],
                               [1, 126.08, 1.474, 85.54, 'Megatron'],
                               [1, 39.41, 1.558, 25.29, 'Megatron'],
                               [1, 78.82, 1.595, 49.41, 'Megatron'],
                               [1, 157.64, 1.639, 96.16, 'Megatron'],

                               [1, 23.64, 1.246, 28.05, 'Deepspeed'],
                               [1, 47.28, 1.337, 62.44, 'Deepspeed'],
                               [1, 94.56, 1.384, 118.75, 'Deepspeed'],
                               [1, 31.52, 1.513, 45.92, 'Deepspeed'],
                               [1, 63.04, 1.626, 86.57, 'Deepspeed'],
                               [1, 126.08, 1.738, 170.38, 'Deepspeed'],
                               [1, 39.41, 1.694, 58.12, 'Deepspeed'],
                               [1, 78.82, 1.894, 120.21, 'Deepspeed'],
                               [1, 157.64, 1.983, 242.96, 'Deepspeed'],

                               [1, 23.64, 1.917, 12.33, 'Ours (w/ Scheduler)'],
                               [1, 47.28, 2.063, 22.92, 'Ours (w/ Scheduler)'],
                               [1, 94.56, 2.090, 45.24, 'Ours (w/ Scheduler)'],
                               [1, 31.52, 2.004, 15.73, 'Ours (w/ Scheduler)'],
                               [1, 63.04, 2.176, 28.97, 'Ours (w/ Scheduler)'],
                               [1, 126.08, 2.252, 55.99,
                                   'Ours (w/ Scheduler)'],
                               [1, 39.41, 2.138, 18.43, 'Ours (w/ Scheduler)'],
                               [1, 78.82, 2.292, 34.39, 'Ours (w/ Scheduler)'],
                               [1, 157.64, 2.345, 67.23,
                                   'Ours (w/ Scheduler)'],

                               [1, 23.64, 1.545, 15.30,
                                   'Ours (w/o Scheduler)'],
                               [1, 47.28, 1.681, 28.12,
                                   'Ours (w/o Scheduler)'],
                               [1, 94.56, 1.760, 53.72,
                                   'Ours (w/o Scheduler)'],
                               [1, 31.52, 1.683, 18.73,
                                   'Ours (w/o Scheduler)'],
                               [1, 63.04, 1.883, 33.48,
                                   'Ours (w/o Scheduler)'],
                               [1, 126.08, 1.957, 64.44,
                                   'Ours (w/o Scheduler)'],
                               [1, 39.41, 1.819, 21.67,
                                   'Ours (w/o Scheduler)'],
                               [1, 78.82, 1.969, 40.03,
                                   'Ours (w/o Scheduler)'],
                               [1, 157.64, 2.042, 77.20,
                                   'Ours (w/o Scheduler)'],
                               ],
                         columns=['case', 'pflop', 'pflops', 'runtime', 'system'])

case_2_df = pd.DataFrame(data=[[2, 23.64, 0.701, 33.72, 'Megatron'],
                               [2, 47.28, 0.792, 59.69, 'Megatron'],
                               [2, 94.56, 0.850, 111.31, 'Megatron'],
                               [2, 31.52, 0.928, 33.98, 'Megatron'],
                               [2, 63.04, 1.048, 60.17, 'Megatron'],
                               [2, 126.08, 1.122, 112.40, 'Megatron'],
                               [2, 39.41, 1.065, 37.01, 'Megatron'],
                               [2, 78.82, 1.211, 65.06, 'Megatron'],
                               [2, 157.64, 1.292, 121.98, 'Megatron'],

                               [2, 23.64, 0.523, 163.43, 'Deepspeed'],
                               [2, 47.28, 0.577, 326.26, 'Deepspeed'],
                               [2, 94.56, 0.610, 659.02, 'Deepspeed'],
                               [2, 31.52, 0.678, 244.57, 'Deepspeed'],
                               [2, 63.04, 0.732, 486.98, 'Deepspeed'],
                               [2, 126.08, 0.785, 973.39, 'Deepspeed'],
                               [2, 39.41, 0.761, 332.12, 'Deepspeed'],
                               [2, 78.82, 0.862, 660.87, 'Deepspeed'],
                               [2, 157.64, 0.911, 1325.28, 'Deepspeed'],

                               [2, 23.64, 1.240, 19.06, 'Ours (w/ Scheduler)'],
                               [2, 47.28, 1.447, 32.67, 'Ours (w/ Scheduler)'],
                               [2, 94.56, 1.735, 54.50, 'Ours (w/ Scheduler)'],
                               [2, 31.52, 1.410, 22.35, 'Ours (w/ Scheduler)'],
                               [2, 63.04, 1.686, 37.39, 'Ours (w/ Scheduler)'],
                               [2, 126.08, 1.956, 64.45,
                                   'Ours (w/ Scheduler)'],
                               [2, 39.41, 1.459, 27.02, 'Ours (w/ Scheduler)'],
                               [2, 78.82, 1.755, 44.91, 'Ours (w/ Scheduler)'],
                               [2, 157.64, 2.015, 78.23,
                                   'Ours (w/ Scheduler)'],

                               [2, 23.64, 0.850, 27.80,
                                   'Ours (w/o Scheduler)'],
                               [2, 47.28, 0.945, 50.01,
                                   'Ours (w/o Scheduler)'],
                               [2, 94.56, 1.013, 93.35,
                                   'Ours (w/o Scheduler)'],
                               [2, 31.52, 1.064, 29.62,
                                   'Ours (w/o Scheduler)'],
                               [2, 63.04, 1.231, 51.22,
                                   'Ours (w/o Scheduler)'],
                               [2, 126.08, 1.328, 94.91,
                                   'Ours (w/o Scheduler)'],
                               [2, 39.41, 1.208, 32.62,
                                   'Ours (w/o Scheduler)'],
                               [2, 78.82, 1.409, 55.95,
                                   'Ours (w/o Scheduler)'],
                               [2, 157.64, 1.540, 102.34,
                                   'Ours (w/o Scheduler)'],
                               ],
                         columns=['case', 'pflop', 'pflops', 'runtime', 'system'])

case_3_df = pd.DataFrame(data=[[3, 23.64, 0.421, 56.20, 'Megatron'],
                               [3, 47.28, 0.463, 102.08, 'Megatron'],
                               [3, 94.56, 0.488, 193.72, 'Megatron'],
                               [3, 31.52, 0.523, 60.31, 'Megatron'],
                               [3, 63.04, 0.580, 108.64, 'Megatron'],
                               [3, 126.08, 0.612, 206.11, 'Megatron'],
                               [3, 39.41, 0.617, 63.86, 'Megatron'],
                               [3, 78.82, 0.689, 114.33, 'Megatron'],
                               [3, 157.64, 0.729, 216.38, 'Megatron'],

                               [3, 23.64, 0.474, 240.28, 'Deepspeed'],
                               [3, 47.28, 0.543, 479.44, 'Deepspeed'],
                               [3, 94.56, 0.595, 958.07, 'Deepspeed'],
                               [3, 31.52, 0.579, 552.99, 'Deepspeed'],
                               [3, 63.04, 0.677, 1103.04, 'Deepspeed'],
                               [3, 126.08, 0.710, 2202.46, 'Deepspeed'],
                               [3, 39.41, 0.673, 845.31, 'Deepspeed'],
                               [3, 78.82, 0.799, 1673.22, 'Deepspeed'],
                               [3, 157.64, 0.837, 3364.53, 'Deepspeed'],

                               [3, 23.64, 1.063, 22.24, 'Ours (w/ Scheduler)'],
                               [3, 47.28, 1.222, 38.68, 'Ours (w/ Scheduler)'],
                               [3, 94.56, 1.313, 72.02, 'Ours (w/ Scheduler)'],
                               [3, 31.52, 1.201, 26.24, 'Ours (w/ Scheduler)'],
                               [3, 63.04, 1.381, 45.66, 'Ours (w/ Scheduler)'],
                               [3, 126.08, 1.465, 86.07,
                                   'Ours (w/ Scheduler)'],
                               [3, 39.41, 1.244, 31.69, 'Ours (w/ Scheduler)'],
                               [3, 78.82, 1.523, 51.75, 'Ours (w/ Scheduler)'],
                               [3, 157.64, 1.651, 95.46,
                                   'Ours (w/ Scheduler)'],

                               [3, 23.64, 0.739, 31.99,
                                   'Ours (w/o Scheduler)'],
                               [3, 47.28, 0.828, 57.07,
                                   'Ours (w/o Scheduler)'],
                               [3, 94.56, 0.891, 106.12,
                                   'Ours (w/o Scheduler)'],
                               [3, 31.52, 0.933, 33.78,
                                   'Ours (w/o Scheduler)'],
                               [3, 63.04, 1.079, 58.42,
                                   'Ours (w/o Scheduler)'],
                               [3, 126.08, 1.158, 108.91,
                                   'Ours (w/o Scheduler)'],
                               [3, 39.41, 1.048, 37.62,
                                   'Ours (w/o Scheduler)'],
                               [3, 78.82, 1.240, 63.58,
                                   'Ours (w/o Scheduler)'],
                               [3, 157.64, 1.360, 115.90,
                                   'Ours (w/o Scheduler)'],
                               ],
                         columns=['case', 'pflop', 'pflops', 'runtime', 'system'])

case_4_df = pd.DataFrame(data=[[4, 23.64, 0.141, 167.74, 'Megatron'],
                               [4, 47.28, 0.157, 301.30, 'Megatron'],
                               [4, 94.56, 0.165, 572.48, 'Megatron'],
                               [4, 31.52, 0.175, 180.11, 'Megatron'],
                               [4, 63.04, 0.201, 313.90, 'Megatron'],
                               [4, 126.08, 0.216, 584.52, 'Megatron'],
                               [4, 39.41, 0.209, 188.17, 'Megatron'],
                               [4, 78.82, 0.242, 326.02, 'Megatron'],
                               [4, 157.64, 0.265, 595.64, 'Megatron'],

                               [4, 23.64, 0.180, 583.71, 'Deepspeed'],
                               [4, 47.28, 0.209, 1170.45, 'Deepspeed'],
                               [4, 94.56, 0.231, 2378.79, 'Deepspeed'],
                               [4, 31.52, 0.224, 1103.88, 'Deepspeed'],
                               [4, 63.04, 0.266, 2197.83, 'Deepspeed'],
                               [4, 126.08, 0.294, 4394.91, 'Deepspeed'],
                               [4, 39.41, 0.264, 1656.86, 'Deepspeed'],
                               [4, 78.82, 0.305, 3222.48, 'Deepspeed'],
                               [4, 157.64, 0.354, 6679.11, 'Deepspeed'],

                               [4, 23.64, 0.540, 43.78, 'Ours (w/ Scheduler)'],
                               [4, 47.28, 0.759, 62.27, 'Ours (w/ Scheduler)'],
                               [4, 94.56, 0.909, 104.06,
                                   'Ours (w/ Scheduler)'],
                               [4, 31.52, 0.617, 51.06, 'Ours (w/ Scheduler)'],
                               [4, 63.04, 0.876, 71.96, 'Ours (w/ Scheduler)'],
                               [4, 126.08, 1.106, 114.01,
                                   'Ours (w/ Scheduler)'],
                               [4, 39.41, 0.677, 58.24, 'Ours (w/ Scheduler)'],
                               [4, 78.82, 0.977, 80.68, 'Ours (w/ Scheduler)'],
                               [4, 157.64, 1.271, 124.07,
                                   'Ours (w/ Scheduler)'],

                               [4, 23.64, 0.256, 92.29,
                                   'Ours (w/o Scheduler)'],
                               [4, 47.28, 0.285, 165.89,
                                   'Ours (w/o Scheduler)'],
                               [4, 94.56, 0.302, 313.63,
                                   'Ours (w/o Scheduler)'],
                               [4, 31.52, 0.318, 99.10,
                                   'Ours (w/o Scheduler)'],
                               [4, 63.04, 0.365, 172.54,
                                   'Ours (w/o Scheduler)'],
                               [4, 126.08, 0.393, 320.63,
                                   'Ours (w/o Scheduler)'],
                               [4, 39.41, 0.369, 106.71,
                                   'Ours (w/o Scheduler)'],
                               [4, 78.82, 0.435, 181.16,
                                   'Ours (w/o Scheduler)'],
                               [4, 157.64, 0.476, 331.25,
                                   'Ours (w/o Scheduler)'],
                               ],
                         columns=['case', 'pflop', 'pflops', 'runtime', 'system'])

cases_df = [case_0_df, case_1_df, case_2_df, case_3_df, case_4_df]


def plot_performance(subfig=None):
    axes = subfig.subplots(nrows=5, ncols=1, sharex=True)
    for i, df in enumerate(cases_df):
        ax = sns.pointplot(ax=axes[i], data=df, x='pflop', y="pflops", hue="system", hue_order=[
            "Ours (w/ Scheduler)", "Megatron", "Ours (w/o Scheduler)", "Deepspeed"], palette=["C2", "C0", "C1", "C3"])
        ax.set(ylim=(0, 3.1))
        ax.set_xlabel(None)
        ax.set_ylabel('PFLOPS')

        if i == 4:
            axes[i].set_xlabel('Model Architectures')
            ax.set(xticklabels=['L24\nB1k', 'L24\nB2k', 'L24\nB4k',
                                'L32\nB1k', 'L32\nB2k', 'L32\nB4k',
                                'L40\nB1k', 'L40\nB2k', 'L40\nB4k', ])
            ax.get_legend().set_title(None)
            ax.legend(loc='lower center', handletextpad=0.1, columnspacing=0.1, bbox_to_anchor=(
                0.48, -0.5), ncol=2, prop={'size': 9}, facecolor='white')
        else:
            ax.get_legend().remove()
