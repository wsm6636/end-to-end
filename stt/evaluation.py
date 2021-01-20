"""Drawing Plots.
"""
import matplotlib.pyplot as plt
import csv
import numpy as np

class Evaluation:

    ymin = -5
    ymax = 105
    hlines = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
    ylabel = ""

    def davare_boxplot_age(self, chains, filename, xaxis_label="\nMaximum-Data Age\nPriority-(Un)ordered Sub-Chains", ylabel = None):

        if ylabel is None:
            ylabel = self.ylabel

        kloda = []
        cases = []
        exact = []

        #the blue box
        boxprops = dict(linewidth=4, color='blue')
        #the median line
        medianprops = dict(linewidth=4, color='red')
        whiskerprops = dict(linewidth=4, color='black')
        capprops = dict(linewidth=4)

        for chain in chains:
            cases.append((1 - (chain.jj_age / chain.e2e_latency)) * 100)
            kloda.append((1 - (chain.kloda / chain.e2e_latency)) * 100)
            exact.append((1 - (chain.sim_sh_age / chain.e2e_latency)) * 100) # we compare with our shortened data age

        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'figure.subplot.top': 0.99})
        plt.rcParams.update({'figure.subplot.bottom': 0.25})
        plt.rcParams.update({'figure.subplot.left': 0.18})
        plt.rcParams.update({'figure.subplot.right': 0.99})
        plt.rcParams.update({'figure.figsize': [7, 4.8]})

        fig1, ax1 = plt.subplots()
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=25)
        ax1.hlines(self.hlines, 0, 4, linestyles=(0,(5,5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot([cases, kloda, exact], labels=["Dür", "Klo", "Our"],
                              showfliers=False,  boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops, widths = 0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax1.tick_params(axis='x', rotation=0, labelsize=35)
        ax1.tick_params(axis='y', rotation=0, labelsize=35)
        ax1.set_xlabel(xaxis_label, fontsize=40)
        plt.tight_layout()
        plt.savefig(filename)


    def davare_boxplot_reaction(self, chains, filename, xaxis_label="\nReaction Time\nPriority-(Un)ordered Sub-Chains", ylabel=None):

        if ylabel is None:
            ylabel = self.ylabel

        kloda = []
        cases = []
        exact = []

        #the blue box
        boxprops = dict(linewidth=4, color='blue')
        #the median line
        medianprops = dict(linewidth=4, color='red')
        whiskerprops = dict(linewidth=4, color='black')
        capprops = dict(linewidth=4)

        # #the blue box
        # boxprops = dict(linewidth=2, color='blue')
        # #the median line
        # medianprops = dict(linewidth=2.5, color='red')
        # whiskerprops = dict(linewidth=2.5, color='black')
        # capprops = dict(linewidth=2.5)

        for chain in chains:
            cases.append((1 - (chain.jj_react / chain.e2e_latency)) * 100)
            kloda.append((1 - (chain.kloda / chain.e2e_latency)) * 100)
            exact.append((1 - (chain.sim_react / chain.e2e_latency)) * 100)

        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'figure.subplot.top': 0.99})
        plt.rcParams.update({'figure.subplot.bottom': 0.25})
        plt.rcParams.update({'figure.subplot.left': 0.18})
        plt.rcParams.update({'figure.subplot.right': 0.99})
        plt.rcParams.update({'figure.figsize': [7, 4.8]})

        fig1, ax1 = plt.subplots()
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=25)
        ax1.hlines(self.hlines, 0, 4, linestyles=(0,(5,5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot([cases, kloda, exact], labels=["Dür", "Klo", "Our"],
                              showfliers=False, boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops, widths = 0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax1.tick_params(axis='x', rotation=0, labelsize=35)
        ax1.tick_params(axis='y', rotation=0, labelsize=35)
        ax1.set_xlabel(xaxis_label, fontsize=40)
        plt.tight_layout()
        plt.savefig(filename)


    def davare_boxplot_age_interconnected(self, chains, filename, xaxis_label="\nMaximum-Data Age\nPriority-(Un)ordered Interconnected Chains", ylabel=None):

        if ylabel is None:
            ylabel = self.ylabel

        cases = []
        exact = []

        #the blue box
        boxprops = dict(linewidth=4, color='blue')
        #the median line
        medianprops = dict(linewidth=4, color='red')
        whiskerprops = dict(linewidth=4, color='black')
        capprops = dict(linewidth=4)

        for chain in chains:
            cases.append((1 - (chain.jj_age / chain.e2e_latency)) * 100)
            exact.append((1 - (chain.interconnected_age / chain.e2e_latency)) * 100)

        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'figure.subplot.top': 0.99})
        plt.rcParams.update({'figure.subplot.bottom': 0.25})
        plt.rcParams.update({'figure.subplot.left': 0.18})
        plt.rcParams.update({'figure.subplot.right': 0.99})
        plt.rcParams.update({'figure.figsize': [7, 4.8]})

        fig1, ax1 = plt.subplots()
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=25)
        ax1.hlines(self.hlines, 0, 3, linestyles=(0,(5,5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot([cases, exact], labels=["Dür", "Our"],
                              showfliers=False,  boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops, widths = 0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax1.tick_params(axis='x', rotation=0, labelsize=35)
        ax1.tick_params(axis='y', rotation=0, labelsize=35)
        ax1.set_xlabel(xaxis_label, fontsize=40)
        plt.tight_layout()
        plt.savefig(filename)


    def davare_boxplot_reaction_interconnected(self, chains, filename, xaxis_label="\nMaximum-Data Age\nPriority-(Un)ordered Interconnected Chains", ylabel=None):

        if ylabel is None:
            ylabel = self.ylabel

        cases = []
        exact = []

        #the blue box
        boxprops = dict(linewidth=4, color='blue')
        #the median line
        medianprops = dict(linewidth=4, color='red')
        whiskerprops = dict(linewidth=4, color='black')
        capprops = dict(linewidth=4)


        for chain in chains:
            cases.append((1 - (chain.jj_react / chain.e2e_latency)) * 100)
            exact.append((1 - (chain.interconnected_react / chain.e2e_latency)) * 100)

        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'figure.subplot.top': 0.99})
        plt.rcParams.update({'figure.subplot.bottom': 0.25})
        plt.rcParams.update({'figure.subplot.left': 0.18})
        plt.rcParams.update({'figure.subplot.right': 0.99})
        plt.rcParams.update({'figure.figsize': [7, 4.8]})

        fig1, ax1 = plt.subplots()
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=25)
        ax1.hlines(self.hlines, 0, 3, linestyles=(0,(5,5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot([cases, exact], labels=["Dür", "Our"],
                              showfliers=False, boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops, widths = 0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax1.tick_params(axis='x', rotation=0, labelsize=35)
        ax1.tick_params(axis='y', rotation=0, labelsize=35)
        ax1.set_xlabel(xaxis_label, fontsize=40)
        plt.tight_layout()
        plt.savefig(filename)

    def heatmap_improvement_disorder_age(self, chains, filename,  yaxis_label="Improvement over Davare", xaxis_label="Norm. chain-disorder"):
        import seaborn as sns

        disorder_ratio =[]
        improvement=[]
        for chain in chains:
            improvement.append((1 - (chain.sim_age / chain.e2e_latency)) * 100)
            if len(chain.chain) == 1:
                disorder_ratio.append(0)
            else:
                disorder_ratio.append(float(chain.chain_disorder)/float(len(chain.chain)-1))

        xedges = []
        yedges = []
        for x in range(20+1):
            xedges.append(x*0.05)
        for y in range(20+1):
            yedges.append(y*5)
        heatmap, xedges, yedges = np.histogram2d(disorder_ratio, improvement, bins=(xedges,yedges))
        heatmap = np.log(heatmap+1) # logarithmic color-scaling

        plt.clf()
        fig1, ax1 = plt.subplots()
        ax  = sns.heatmap(heatmap, linewidth=0.5) #cbar_kws={'label': 'e^()-1'}
        cbar = ax.collections[0].colorbar
        cbar.set_ticks([0, 4, 8])
        cbar.set_ticklabels(['$10^0$-1', '$10^4$-1', '$10^8$-1'])
        cbar.ax.tick_params(labelsize=33)

        xticks = [0, 4, 8, 12, 16, 20]#[0, 5,10,15, 20]#[0,10,20]#[0, 4, 8, 12, 16, 20]
        yticks = [0, 4, 8, 12, 16, 20]
        ax1.invert_yaxis()
        ax.set_xticks(xticks)
        ax.set_xticklabels(("0", "0.2", "0.4", "0.6", "0.8", "1"))#(("0", "0.25", "0.5", "0.75", "1.0"))#(("0", "0.5", "1.0"))#(("0", "0.2", "0.4", "0.6", "0.8", "1.0"))
        ax.set_yticks(yticks)
        ax.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax.tick_params(axis='x', rotation=0, labelsize=28)
        ax.tick_params(axis='y', rotation=0, labelsize=38)
        ax1.set_xlabel(xaxis_label, fontsize=38)
        ax1.set_ylabel(yaxis_label, fontsize=38)
        plt.tight_layout()
        plt.savefig(filename)


    def heatmap_improvement_disorder_react(self, chains, filename, yaxis_label="Improvement over Davare", xaxis_label="Norm. chain-disorder"):
        import seaborn as sns

        disorder_ratio =[]
        improvement=[]
        for chain in chains:
            improvement.append((1 - (chain.sim_react / chain.e2e_latency)) * 100)
            if len(chain.chain) == 1:
                disorder_ratio.append(0)
            else:
                disorder_ratio.append(float(chain.chain_disorder)/float(len(chain.chain)-1))

        xedges = []
        yedges = []
        for x in range(20+1):
            xedges.append(x*0.05)
        for y in range(20+1):
            yedges.append(y*5)
        heatmap, xedges, yedges = np.histogram2d(disorder_ratio, improvement, bins=(xedges,yedges))
        heatmap = np.log(heatmap+1) # logarithmic color-scaling

        plt.clf()
        fig1, ax1 = plt.subplots()
        ax  = sns.heatmap(heatmap, linewidth=0.5) #cbar_kws={'label': 'e^()-1'}
        cbar = ax.collections[0].colorbar
        cbar.set_ticks([0, 4, 8])
        cbar.set_ticklabels(['$10^0$-1', '$10^4$-1', '$10^8$-1'])
        cbar.ax.tick_params(labelsize=33, rotation=0)

        xticks = [0, 4, 8, 12, 16, 20]#[0, 5,10,15, 20]#[0,10,20]#[0, 4, 8, 12, 16, 20]
        yticks = [0, 4, 8, 12, 16, 20]
        ax1.invert_yaxis()
        ax.set_xticks(xticks)
        ax.set_xticklabels(("0", "0.2", "0.4", "0.6", "0.8", "1"))#(("0", "0.25", "0.5", "0.75", "1.0"))#(("0", "0.5", "1.0"))#(("0", "0.2", "0.4", "0.6", "0.8", "1.0"))
        ax.set_yticks(yticks)
        ax.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax.tick_params(axis='x', rotation=0, labelsize=28)
        ax.tick_params(axis='y', rotation=0, labelsize=38)
        ax1.set_xlabel(xaxis_label, fontsize=38)
        ax1.set_ylabel(yaxis_label, fontsize=38)
        plt.tight_layout()
        plt.savefig(filename)
