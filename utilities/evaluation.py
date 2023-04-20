"""Drawing Plots."""
import matplotlib.pyplot as plt
import numpy as np


class Evaluation:
    """Collection of functions to draw plots."""
    ymin = -5  # y-axis beginning
    ymax = 105  # y-axis ending
    hlines = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]  # horizontal lines
    ylabel = ""  # global label for y-axis
        
    def davare_boxplot_age_interconnected(self, chains,chainstsn, filename,
                                          xaxis_label="", ylabel=None):
        """Boxplot: Interconnected ECU, maximum data age.

        Shows the latency reduction [%] of several analyses compared to Davare.
        """
        if ylabel is None:
            ylabel = self.ylabel

        # Analysis results.
        Gunzel = []  # reduced interconnected data age (for comparison)
        tsn = [] 

        for chain in chains:
            Gunzel.append((1-(chain.inter_Gunzel_age/chain.davare))*100)
        for chaintsn in chainstsn:
            tsn.append((1-(chaintsn.inter_tsn_age/chain.davare))*100)
            # print(chaintsn.inter_tsn_age,chaintsn.davare,chain.davare)

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
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=25)
        ax1.hlines(self.hlines, 0, 3, linestyles=(0, (5, 5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot(
                [ Gunzel,tsn],
                labels=["Gunzel","tsn"],
                showfliers=False,
                boxprops=boxprops,
                medianprops=medianprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                widths=0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax1.tick_params(axis='x', rotation=0, labelsize=35)
        ax1.tick_params(axis='y', rotation=0, labelsize=35)
        ax1.set_xlabel(xaxis_label, fontsize=40)
        plt.tight_layout()

        # Save.
        plt.savefig(filename)

    def davare_boxplot_reaction_interconnected(self, chains, chainstsn,filename,
                                               xaxis_label="", ylabel=None):
        """Boxplot: Interconnected ECU, maximum reaction time.

        Shows the latency reduction [%] of several analyses compared to Davare.
        """
        if ylabel is None:
            ylabel = self.ylabel

        # Analysis results.
        Gunzel = []
        tsn = []

        for chain in chains:
            Gunzel.append((1-(chain.inter_Gunzel_react/chain.davare))*100)
        for chaintsn in chainstsn:
            tsn.append((1-(chaintsn.inter_tsn_react/chain.davare))*100)

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
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=25)
        ax1.hlines(self.hlines, 0, 3, linestyles=(0, (5, 5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot(
                [Gunzel,tsn],
                labels=["Gunzel","tsn"],
                showfliers=False,
                boxprops=boxprops,
                medianprops=medianprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                widths=0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax1.tick_params(axis='x', rotation=0, labelsize=35)
        ax1.tick_params(axis='y', rotation=0, labelsize=35)
        ax1.set_xlabel(xaxis_label, fontsize=40)
        plt.tight_layout()

        # Save.
        plt.savefig(filename)
