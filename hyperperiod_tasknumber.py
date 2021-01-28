#!/usr/bin/env python3
"""Show the dependency between randomly chosen task period and hyperperiod."""

import numpy as np
import matplotlib.pyplot as plt


def main():
    """Main Function."""

    task_numbers = [
        4,
        8,
        12,
        16,
        20
    ]

    min_period = 1
    max_period = 30

    number_tries = 10000

    results = []

    for tn in task_numbers:
        tn_results = []  # task number specific results
        for _ in range(number_tries):
            # Choose periods randomly.
            periods = list(np.random.randint(
                    low=min_period,
                    high=max_period,
                    size=(tn,)))
            # Compute hyperperiod
            # Attention: Integer overflows are possible with np.
            hyperperiod = np.lcm.reduce(periods)
            tn_results.append(hyperperiod)
        results.append(tn_results)

    # print(results)

    draw_boxplots(
        results,
        "output/timing/dependency_hyperperiod_numbertasks.pdf",
        task_numbers,
        xaxis_label="number of tasks",
        yaxis_label="hyperperiod",
    )


def draw_boxplots(
        results,
        filename,
        xlabels,
        xaxis_label="",
        yaxis_label="",
        ylimits=None  # [ylim_min, ylim_max]
        ):
    """Boxplot: Draw given results.
    """

    # Plotting.
    # Blue box configuration:
    boxprops = dict(linewidth=4, color='blue')
    # Median line configuration:
    medianprops = dict(linewidth=4, color='red')
    whiskerprops = dict(linewidth=4, color='black')
    capprops = dict(linewidth=4)
    # Size parameters:
    plt.rcParams.update({'font.size': 18})
    plt.rcParams.update({'figure.subplot.top': 0.99})
    plt.rcParams.update({'figure.subplot.bottom': 0.25})
    plt.rcParams.update({'figure.subplot.left': 0.18})
    plt.rcParams.update({'figure.subplot.right': 0.99})
    plt.rcParams.update({'figure.figsize': [7, 4.8]})

    # Draw plots:
    fig1, ax1 = plt.subplots()
    if ylimits is not None:
        ax1.set_ylim(ylimits)
    ax1.set_ylabel(yaxis_label, fontsize=25)

    my_plot = ax1.boxplot(
            results,
            labels=xlabels,
            showfliers=False,
            boxprops=boxprops,
            medianprops=medianprops,
            whiskerprops=whiskerprops,
            capprops=capprops,
            widths=0.6)
    # ax1.set_yticks([0, 20, 40, 60, 80, 100])
    # ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
    # ax1.tick_params(axis='x', rotation=0, labelsize=35)
    # ax1.tick_params(axis='y', rotation=0, labelsize=35)
    ax1.set_xlabel(xaxis_label, fontsize=25)
    plt.tight_layout()

    # Save.
    plt.savefig(filename)


if __name__ == '__main__':
    main()
