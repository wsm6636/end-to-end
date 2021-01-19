"""The transformer is used to import scheduling data of other frameworks.

:Filename: transformer.py
:Author: Marco Dürr (marco.duerr@tu-dortmund.de)
:Date: 03.02.19
"""
import matplotlib.pyplot as plt
import csv
import numpy as np

class Evaluation:

    ymin = -5
    ymax = 105
    hlines = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
    ylabel = ""

    # def draw_boxplot(self):
    #     jj_age = []
    #     jj_react = []
    #     sim_age = []
    #     sim_react = []
    #     for result in self.chains_2p:
    #         jj_age.append(result[0])
    #         jj_react.append(result[1])
    #         sim_age.append(result[2])
    #         sim_react.append(result[3])
    #     for result in self.chains_3p:
    #         jj_age.append(result[0])
    #         jj_react.append(result[1])
    #         sim_age.append(result[2])
    #         sim_react.append(result[3])
    #
    #     plt.rcParams.update({'font.size': 14})
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylabel("Calculated Value (%)")
    #     ax1.hlines([100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0], 0, 5, linestyles="dotted", colors="grey")
    #     my_plot = ax1.boxplot([jj_react, jj_age, sim_react, sim_age], labels=["Reaction \n Time", "Data Age", "Tight \n Reaction Time", "Tight \n Data Age"], showfliers=False)
    #     print("median1: " + str(my_plot['medians'][0]._y[0]))
    #     print("LQ1: " + str(my_plot['whiskers'][0]._y[0]))
    #     print("UQ1: " + str(my_plot['whiskers'][1]._y[0]))
    #     print("min1: " + str(my_plot['caps'][0]._y[0]))
    #     print("max1: " + str(my_plot['caps'][1]._y[0]))
    #     print("median2: " + str(my_plot['medians'][1]._y[0]))
    #     print("LQ2: " + str(my_plot['whiskers'][2]._y[0]))
    #     print("UQ2: " + str(my_plot['whiskers'][3]._y[0]))
    #     print("min2: " + str(my_plot['caps'][2]._y[0]))
    #     print("max2: " + str(my_plot['caps'][3]._y[0]))
    #     print("median3: " + str(my_plot['medians'][2]._y[0]))
    #     print("LQ3: " + str(my_plot['whiskers'][4]._y[0]))
    #     print("UQ3: " + str(my_plot['whiskers'][5]._y[0]))
    #     print("min3: " + str(my_plot['caps'][4]._y[0]))
    #     print("max3: " + str(my_plot['caps'][5]._y[0]))
    #     print("median4: " + str(my_plot['medians'][3]._y[0]))
    #     print("LQ4: " + str(my_plot['whiskers'][6]._y[0]))
    #     print("UQ4: " + str(my_plot['whiskers'][7]._y[0]))
    #     print("min4: " + str(my_plot['caps'][6]._y[0]))
    #     print("max4: " + str(my_plot['caps'][7]._y[0]))
    #     plt.show()
    #
    # def draw_boxplot_util_benchmark(self, file, filename, age):
    #     util50 = []
    #     util60 = []
    #     util70 = []
    #     util80 = []
    #     util90 = []
    #     with open(file) as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    #         if age:
    #             for row in csv_reader:
    #                 davare = row[3]
    #                 if row[0] == 50.0:
    #                     util50.append(max(0, (1 - (row[5] / davare)) * 100))
    #                 elif row[0] == 60.0:
    #                     util60.append(max(0, (1 - (row[5] / davare)) * 100))
    #                 elif row[0] == 70.0:
    #                     util70.append(max(0, (1 - (row[5] / davare)) * 100))
    #                 elif row[0] == 80.0:
    #                     util80.append(max(0, (1 - (row[5] / davare)) * 100))
    #                 elif row[0] == 90.0:
    #                     util90.append(max(0, (1 - (row[5] / davare)) * 100))
    #         else:
    #             for row in csv_reader:
    #                 davare = row[3]
    #                 if row[0] == 50.0:
    #                     util50.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 60.0:
    #                     util60.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 70.0:
    #                     util70.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 80.0:
    #                     util80.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 90.0:
    #                     util90.append(max(0, (1 - (row[4] / davare)) * 100))
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.left': 0.14})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.13})
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([util50, util60, util70, util80, util90], labels=["50%", "60%", "70%", "80%", "90%"],
    #                           showfliers=False)
    #     ax1.set_xlabel("Task Set Utilization")
    #     print("median1: " + str(my_plot['medians'][0]._y[0]))
    #     print("LQ1: " + str(my_plot['whiskers'][0]._y[0]))
    #     print("UQ1: " + str(my_plot['whiskers'][1]._y[0]))
    #     print("min1: " + str(my_plot['caps'][0]._y[0]))
    #     print("max1: " + str(my_plot['caps'][1]._y[0]))
    #     print("median2: " + str(my_plot['medians'][1]._y[0]))
    #     print("LQ2: " + str(my_plot['whiskers'][2]._y[0]))
    #     print("UQ2: " + str(my_plot['whiskers'][3]._y[0]))
    #     print("min2: " + str(my_plot['caps'][2]._y[0]))
    #     print("max2: " + str(my_plot['caps'][3]._y[0]))
    #     # print("median3: " + str(my_plot['medians'][2]._y[0]))
    #     # print("LQ3: " + str(my_plot['whiskers'][4]._y[0]))
    #     # print("UQ3: " + str(my_plot['whiskers'][5]._y[0]))
    #     # print("min3: " + str(my_plot['caps'][4]._y[0]))
    #     # print("max3: " + str(my_plot['caps'][5]._y[0]))
    #     # print("median4: " + str(my_plot['medians'][3]._y[0]))
    #     # print("LQ4: " + str(my_plot['whiskers'][6]._y[0]))
    #     # print("UQ4: " + str(my_plot['whiskers'][7]._y[0]))
    #     # print("min4: " + str(my_plot['caps'][6]._y[0]))
    #     # print("max4: " + str(my_plot['caps'][7]._y[0]))
    #     plt.savefig(filename)
    #
    # def draw_boxplot_length(self, file, filename, age):
    #     len5 = []
    #     len10 = []
    #     len15 = []
    #     len20 = []
    #     len25 = []
    #     with open(file) as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    #         if age:
    #             for row in csv_reader:
    #                 davare = row[2]
    #                 if row[1] == 5:
    #                     len5.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[1] == 10:
    #                     len10.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[1] == 15:
    #                     len15.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[1] == 20:
    #                     len20.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[1] == 25:
    #                     len25.append(max(0, (1 - (row[4] / davare)) * 100))
    #         else:
    #             for row in csv_reader:
    #                 davare = row[2]
    #                 if row[1] == 5:
    #                     len5.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[1] == 10:
    #                     len10.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[1] == 15:
    #                     len15.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[1] == 20:
    #                     len20.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[1] == 25:
    #                     len25.append(max(0, (1 - (row[3] / davare)) * 100))
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.left': 0.14})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.13})
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([len5, len10, len15, len20, len25], labels=["5", "10", "15", "20", "25"], showfliers=False)
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.set_xlabel("Number of Tasks in Cause-Effect Chain")
    #     print("median1: " + str(my_plot['medians'][0]._y[0]))
    #     print("LQ1: " + str(my_plot['whiskers'][0]._y[0]))
    #     print("UQ1: " + str(my_plot['whiskers'][1]._y[0]))
    #     print("min1: " + str(my_plot['caps'][0]._y[0]))
    #     print("max1: " + str(my_plot['caps'][1]._y[0]))
    #     print("median2: " + str(my_plot['medians'][1]._y[0]))
    #     print("LQ2: " + str(my_plot['whiskers'][2]._y[0]))
    #     print("UQ2: " + str(my_plot['whiskers'][3]._y[0]))
    #     print("min2: " + str(my_plot['caps'][2]._y[0]))
    #     print("max2: " + str(my_plot['caps'][3]._y[0]))
    #     # print("median3: " + str(my_plot['medians'][2]._y[0]))
    #     # print("LQ3: " + str(my_plot['whiskers'][4]._y[0]))
    #     # print("UQ3: " + str(my_plot['whiskers'][5]._y[0]))
    #     # print("min3: " + str(my_plot['caps'][4]._y[0]))
    #     # print("max3: " + str(my_plot['caps'][5]._y[0]))
    #     # print("median4: " + str(my_plot['medians'][3]._y[0]))
    #     # print("LQ4: " + str(my_plot['whiskers'][6]._y[0]))
    #     # print("UQ4: " + str(my_plot['whiskers'][7]._y[0]))
    #     # print("min4: " + str(my_plot['caps'][6]._y[0]))
    #     # print("max4: " + str(my_plot['caps'][7]._y[0]))
    #     plt.savefig(filename)
    #
    # def draw_boxplot_util(self, file, filename, age):
    #     util50 = []
    #     util60 = []
    #     util70 = []
    #     util80 = []
    #     util90 = []
    #     with open(file) as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    #         if age:
    #             for row in csv_reader:
    #                 davare = row[2]
    #                 if row[0] == 50:
    #                     util50.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 60:
    #                     util60.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 70:
    #                     util70.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 80:
    #                     util80.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 90:
    #                     util90.append(max(0, (1 - (row[4] / davare)) * 100))
    #         else:
    #             for row in csv_reader:
    #                 davare = row[2]
    #                 if row[0] == 50:
    #                     util50.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 60:
    #                     util60.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 70:
    #                     util70.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 80:
    #                     util80.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 90:
    #                     util90.append(max(0, (1 - (row[3] / davare)) * 100))
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.left': 0.14})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.13})
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([util50, util60, util70, util80, util90], labels=["50%", "60%", "70%", "80%", "90%"],
    #                           showfliers=False)
    #     ax1.set_xlabel("Task Set Utilization")
    #     print("median1: " + str(my_plot['medians'][0]._y[0]))
    #     print("LQ1: " + str(my_plot['whiskers'][0]._y[0]))
    #     print("UQ1: " + str(my_plot['whiskers'][1]._y[0]))
    #     print("min1: " + str(my_plot['caps'][0]._y[0]))
    #     print("max1: " + str(my_plot['caps'][1]._y[0]))
    #     print("median2: " + str(my_plot['medians'][1]._y[0]))
    #     print("LQ2: " + str(my_plot['whiskers'][2]._y[0]))
    #     print("UQ2: " + str(my_plot['whiskers'][3]._y[0]))
    #     print("min2: " + str(my_plot['caps'][2]._y[0]))
    #     print("max2: " + str(my_plot['caps'][3]._y[0]))
    #     # print("median3: " + str(my_plot['medians'][2]._y[0]))
    #     # print("LQ3: " + str(my_plot['whiskers'][4]._y[0]))
    #     # print("UQ3: " + str(my_plot['whiskers'][5]._y[0]))
    #     # print("min3: " + str(my_plot['caps'][4]._y[0]))
    #     # print("max3: " + str(my_plot['caps'][5]._y[0]))
    #     # print("median4: " + str(my_plot['medians'][3]._y[0]))
    #     # print("LQ4: " + str(my_plot['whiskers'][6]._y[0]))
    #     # print("UQ4: " + str(my_plot['whiskers'][7]._y[0]))
    #     # print("min4: " + str(my_plot['caps'][6]._y[0]))
    #     # print("max4: " + str(my_plot['caps'][7]._y[0]))
    #     plt.savefig(filename)
    #
    # def draw_boxplot_period(self, file, filename, age):
    #     period5 = []
    #     period50 = []
    #     period250 = []
    #     period500 = []
    #     period1000 = []
    #     with open(file) as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    #         if age:
    #             for row in csv_reader:
    #                 davare = row[2]
    #                 if row[0] == 5:
    #                     period5.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 50:
    #                     period50.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 250:
    #                     period250.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 500:
    #                     period500.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 1000:
    #                     period1000.append(max(0, (1 - (row[4] / davare)) * 100))
    #         else:
    #             for row in csv_reader:
    #                 davare = row[2]
    #                 if row[0] == 5:
    #                     period5.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 50:
    #                     period50.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 250:
    #                     period250.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 500:
    #                     period500.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 1000:
    #                     period1000.append(max(0, (1 - (row[3] / davare)) * 100))
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.left': 0.14})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.13})
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([period5, period50, period250, period500, period1000], labels=["5", "50", "250", "500", "1000"],
    #                           showfliers=False)
    #     ax1.set_xlabel("Range of Minimal Inter-Arrival Time")
    #     print("median1: " + str(my_plot['medians'][0]._y[0]))
    #     print("LQ1: " + str(my_plot['whiskers'][0]._y[0]))
    #     print("UQ1: " + str(my_plot['whiskers'][1]._y[0]))
    #     print("min1: " + str(my_plot['caps'][0]._y[0]))
    #     print("max1: " + str(my_plot['caps'][1]._y[0]))
    #     print("median2: " + str(my_plot['medians'][1]._y[0]))
    #     print("LQ2: " + str(my_plot['whiskers'][2]._y[0]))
    #     print("UQ2: " + str(my_plot['whiskers'][3]._y[0]))
    #     print("min2: " + str(my_plot['caps'][2]._y[0]))
    #     print("max2: " + str(my_plot['caps'][3]._y[0]))
    #     # print("median3: " + str(my_plot['medians'][2]._y[0]))
    #     # print("LQ3: " + str(my_plot['whiskers'][4]._y[0]))
    #     # print("UQ3: " + str(my_plot['whiskers'][5]._y[0]))
    #     # print("min3: " + str(my_plot['caps'][4]._y[0]))
    #     # print("max3: " + str(my_plot['caps'][5]._y[0]))
    #     # print("median4: " + str(my_plot['medians'][3]._y[0]))
    #     # print("LQ4: " + str(my_plot['whiskers'][6]._y[0]))
    #     # print("UQ4: " + str(my_plot['whiskers'][7]._y[0]))
    #     # print("min4: " + str(my_plot['caps'][6]._y[0]))
    #     # print("max4: " + str(my_plot['caps'][7]._y[0]))
    #     plt.savefig(filename)
    #
    # def draw_boxplot_com(self, file, filename, age):
    #     period5 = []
    #     period50 = []
    #     period250 = []
    #     period500 = []
    #     period1000 = []
    #     with open(file) as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    #         if age:
    #             for row in csv_reader:
    #                 davare = row[2]
    #                 if row[0] == 0:
    #                     period5.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 1:
    #                     period50.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 2:
    #                     period250.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 3:
    #                     period500.append(max(0, (1 - (row[4] / davare)) * 100))
    #                 elif row[0] == 4:
    #                     period1000.append(max(0, (1 - (row[4] / davare)) * 100))
    #         else:
    #             for row in csv_reader:
    #                 davare = row[2]
    #                 if row[0] == 0:
    #                     period5.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 1:
    #                     period50.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 2:
    #                     period250.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 3:
    #                     period500.append(max(0, (1 - (row[3] / davare)) * 100))
    #                 elif row[0] == 4:
    #                     period1000.append(max(0, (1 - (row[3] / davare)) * 100))
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.left': 0.14})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.13})
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted", colors="grey")
    #     my_plot = ax1.boxplot([period5, period50, period250, period500, period1000], labels=["0", "5", "10", "15", "20"],
    #                           showfliers=False)
    #     ax1.set_xlabel("Number of Communications")
    #     print("median1: " + str(my_plot['medians'][0]._y[0]))
    #     print("LQ1: " + str(my_plot['whiskers'][0]._y[0]))
    #     print("UQ1: " + str(my_plot['whiskers'][1]._y[0]))
    #     print("min1: " + str(my_plot['caps'][0]._y[0]))
    #     print("max1: " + str(my_plot['caps'][1]._y[0]))
    #     print("median2: " + str(my_plot['medians'][1]._y[0]))
    #     print("LQ2: " + str(my_plot['whiskers'][2]._y[0]))
    #     print("UQ2: " + str(my_plot['whiskers'][3]._y[0]))
    #     print("min2: " + str(my_plot['caps'][2]._y[0]))
    #     print("max2: " + str(my_plot['caps'][3]._y[0]))
    #     # print("median3: " + str(my_plot['medians'][2]._y[0]))
    #     # print("LQ3: " + str(my_plot['whiskers'][4]._y[0]))
    #     # print("UQ3: " + str(my_plot['whiskers'][5]._y[0]))
    #     # print("min3: " + str(my_plot['caps'][4]._y[0]))
    #     # print("max3: " + str(my_plot['caps'][5]._y[0]))
    #     # print("median4: " + str(my_plot['medians'][3]._y[0]))
    #     # print("LQ4: " + str(my_plot['whiskers'][6]._y[0]))
    #     # print("UQ4: " + str(my_plot['whiskers'][7]._y[0]))
    #     # print("min4: " + str(my_plot['caps'][6]._y[0]))
    #     # print("max4: " + str(my_plot['caps'][7]._y[0]))
    #     plt.savefig(filename)
    #
    # def date20_boxplot_age_davare(self, chain_order, chain_unorder, chain_all, filename):
    #
    #     exact_age_order = []
    #     exact_age_unorder = []
    #     exact_age_all = []
    #
    #     for chain in chain_order:
    #         exact_age_order.append((1 - (chain.sim_age / chain.e2e_latency)) * 100)
    #
    #     for chain in chain_unorder:
    #         exact_age_unorder.append((1 - (chain.sim_age / chain.e2e_latency)) * 100)
    #
    #     for chain in chain_all:
    #         exact_age_all.append((1 - (chain.sim_age / chain.e2e_latency)) * 100)
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.top': 0.99})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.25})
    #     plt.rcParams.update({'figure.subplot.left': 0.18})
    #     plt.rcParams.update({'figure.subplot.right': 0.99})
    #     plt.rcParams.update({'figure.figsize': [7, 4.8]})
    #
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([exact_age_all, exact_age_unorder, exact_age_order], labels=["arbitrary", "increasing", "decreasing"],
    #                           showfliers=False)
    #     ax1.set_xlabel("\nSorting of the task priorities\nwithin a cause-effect chain")
    #     plt.savefig(filename)
    #
    # def date20_boxplot_age_duerr(self, chain_order, chain_unorder, chain_all, filename):
    #
    #     exact_age_order = []
    #     exact_age_unorder = []
    #     exact_age_all = []
    #
    #     for chain in chain_order:
    #         exact_age_order.append((1 - (chain.sim_age / chain.jj_age)) * 100)
    #
    #     for chain in chain_unorder:
    #         exact_age_unorder.append((1 - (chain.sim_age / chain.jj_age)) * 100)
    #
    #     for chain in chain_all:
    #         exact_age_all.append((1 - (chain.sim_age / chain.jj_age)) * 100)
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.top': 0.99})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.25})
    #     plt.rcParams.update({'figure.subplot.left': 0.18})
    #     plt.rcParams.update({'figure.subplot.right': 0.99})
    #     plt.rcParams.update({'figure.figsize': [7, 4.8]})
    #
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([exact_age_all, exact_age_unorder, exact_age_order], labels=["arbitrary", "increasing", "decreasing"],
    #                           showfliers=False)
    #     ax1.set_xlabel("\nSorting of the task priorities\nwithin a cause-effect chain")
    #     plt.savefig(filename)
    #
    # def davare_boxplot_age_ordered(self, chains, filename):
    #
    #     kloda = []
    #     cases = []
    #     exact = []
    #
    #     for chain in chains:
    #         cases.append((1 - (chain.jj_age / chain.e2e_latency)) * 100)
    #         kloda.append((1 - (chain.kloda / chain.e2e_latency)) * 100)
    #         exact.append((1 - (chain.sim_age / chain.e2e_latency)) * 100)
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.top': 0.99})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.25})
    #     plt.rcParams.update({'figure.subplot.left': 0.18})
    #     plt.rcParams.update({'figure.subplot.right': 0.99})
    #     plt.rcParams.update({'figure.figsize': [7, 4.8]})
    #
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([cases, kloda, exact], labels=["Dürr", "Kloda", "Sim"],
    #                           showfliers=False)
    #     ax1.set_xlabel("\nMaximum-Data Age\nPriority-Ordered Sub-Chains")
    #     plt.savefig(filename)
    #
    # def davare_boxplot_age_unordered(self, chains, filename):
    #
    #     kloda = []
    #     cases = []
    #     exact = []
    #
    #     for chain in chains:
    #         cases.append((1 - (chain.jj_age / chain.e2e_latency)) * 100)
    #         kloda.append((1 - (chain.kloda / chain.e2e_latency)) * 100)
    #         exact.append((1 - (chain.sim_age / chain.e2e_latency)) * 100)
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.top': 0.99})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.25})
    #     plt.rcParams.update({'figure.subplot.left': 0.18})
    #     plt.rcParams.update({'figure.subplot.right': 0.99})
    #     plt.rcParams.update({'figure.figsize': [7, 4.8]})
    #
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([cases, kloda, exact], labels=["Dürr", "Kloda", "Sim"],
    #                           showfliers=False)
    #     ax1.set_xlabel("\nMaximum-Data Age\nPriority-Unordered Sub-Chains")
    #     plt.savefig(filename)
    #
    # def davare_boxplot_reaction_unordered(self, chains, filename):
    #
    #     kloda = []
    #     cases = []
    #     exact = []
    #
    #     for chain in chains:
    #         cases.append((1 - (chain.jj_react / chain.e2e_latency)) * 100)
    #         kloda.append((1 - (chain.kloda / chain.e2e_latency)) * 100)
    #         exact.append((1 - (chain.sim_react / chain.e2e_latency)) * 100)
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.top': 0.99})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.25})
    #     plt.rcParams.update({'figure.subplot.left': 0.18})
    #     plt.rcParams.update({'figure.subplot.right': 0.99})
    #     plt.rcParams.update({'figure.figsize': [7, 4.8]})
    #
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([cases, kloda, exact], labels=["Dürr", "Kloda", "Sim"],
    #                           showfliers=False)
    #     ax1.set_xlabel("\nReaction Time\nPriority-Unordered Sub-Chains")
    #     plt.savefig(filename)
    #
    # def davare_boxplot_reaction_ordered(self, chains, filename):
    #
    #     kloda = []
    #     cases = []
    #     exact = []
    #
    #     for chain in chains:
    #         cases.append((1 - (chain.jj_react / chain.e2e_latency)) * 100)
    #         kloda.append((1 - (chain.kloda / chain.e2e_latency)) * 100)
    #         exact.append((1 - (chain.sim_react / chain.e2e_latency)) * 100)
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.top': 0.99})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.25})
    #     plt.rcParams.update({'figure.subplot.left': 0.18})
    #     plt.rcParams.update({'figure.subplot.right': 0.99})
    #     plt.rcParams.update({'figure.figsize': [7, 4.8]})
    #
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([cases, kloda, exact], labels=["Dürr", "Kloda", "Sim"],
    #                           showfliers=False)
    #     ax1.set_xlabel("\nReaction Time\nPriority-Ordered Sub-Chains")
    #     plt.savefig(filename)
    #
    # def davare_boxplot_age_ordered_interconnected(self, chains, filename):
    #
    #     cases = []
    #     exact = []
    #
    #     for chain in chains:
    #         cases.append((1 - (chain.jj_age / chain.e2e_latency)) * 100)
    #         exact.append((1 - (chain.interconnected_age / chain.e2e_latency)) * 100)
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.top': 0.99})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.25})
    #     plt.rcParams.update({'figure.subplot.left': 0.18})
    #     plt.rcParams.update({'figure.subplot.right': 0.99})
    #     plt.rcParams.update({'figure.figsize': [7, 4.8]})
    #
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([cases, exact], labels=["Dürr", "New"],
    #                           showfliers=False)
    #     ax1.set_xlabel("\nMaximum-Data Age\nPriority-Ordered Interconnected Chains")
    #     plt.savefig(filename)
    #
    # def davare_boxplot_age_unordered_interconnected(self, chains, filename):
    #
    #     cases = []
    #     exact = []
    #
    #     for chain in chains:
    #         cases.append((1 - (chain.jj_age / chain.e2e_latency)) * 100)
    #         exact.append((1 - (chain.interconnected_age / chain.e2e_latency)) * 100)
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.top': 0.99})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.25})
    #     plt.rcParams.update({'figure.subplot.left': 0.18})
    #     plt.rcParams.update({'figure.subplot.right': 0.99})
    #     plt.rcParams.update({'figure.figsize': [7, 4.8]})
    #
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([cases, exact], labels=["Dürr", "New"],
    #                           showfliers=False)
    #     ax1.set_xlabel("\nMaximum-Data Age\nPriority-Unordered Interconnected Chains")
    #     plt.savefig(filename)
    #
    # def draw_boxplot_cases_react(self, chain_order, chain_unorder, filename):
    #
    #     bound_age_order = []
    #     exact_age_order = []
    #     bound_react_order = []
    #     exact_react_order = []
    #
    #     bound_age_unorder = []
    #     exact_age_unorder = []
    #     bound_react_unorder = []
    #     exact_react_unorder = []
    #
    #     for chain in chain_order:
    #         bound_age_order.append(max(0, (1 - (chain.jj_age / chain.e2e_latency)) * 100))
    #         exact_age_order.append(max(0, (1 - (chain.sim_age / chain.e2e_latency)) * 100))
    #         bound_react_order.append(max(0, (1 - (chain.jj_react / chain.e2e_latency)) * 100))
    #         exact_react_order.append(max(0, (1 - (chain.sim_react / chain.e2e_latency)) * 100))
    #
    #     for chain in chain_unorder:
    #         bound_age_unorder.append(max(0, (1 - (chain.jj_age / chain.e2e_latency)) * 100))
    #         exact_age_unorder.append(max(0, (1 - (chain.sim_age / chain.e2e_latency)) * 100))
    #         bound_react_unorder.append(max(0, (1 - (chain.jj_react / chain.e2e_latency)) * 100))
    #         exact_react_unorder.append(max(0, (1 - (chain.sim_react / chain.e2e_latency)) * 100))
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.left': 0.14})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.13})
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([bound_react_unorder, bound_react_order, exact_react_unorder, exact_react_order],
    #                           labels=["bound unorder", "bound order", "exact unoder", "exact oder"],
    #                           showfliers=False)
    #     ax1.set_xlabel("Maximum-Reaction Time")
    #     plt.savefig(filename)
    #
    # def draw_boxplot_cases_interconnect(self, chain_order, filename):
    #
    #     bound_age_order = []
    #     exact_age_order = []
    #     exact_jj_age_order = []
    #
    #     for chain in chain_order:
    #         bound_age_order.append((1 - (chain.jj_age / chain.e2e_latency)) * 100)
    #         exact_age_order.append((1 - (chain.interconnected_age / chain.e2e_latency)) * 100)
    #         exact_jj_age_order.append((1 - (chain.interconnected_age / chain.jj_age)) * 100)
    #
    #     plt.rcParams.update({'font.size': 18})
    #     plt.rcParams.update({'figure.subplot.left': 0.14})
    #     plt.rcParams.update({'figure.subplot.bottom': 0.13})
    #     fig1, ax1 = plt.subplots()
    #     ax1.set_ylim([self.ymin, self.ymax])
    #     ax1.set_ylabel(self.ylabel)
    #     ax1.hlines(self.hlines, 0, 6, linestyles="dotted",
    #                colors="grey")
    #     my_plot = ax1.boxplot([bound_age_order, exact_age_order, exact_jj_age_order],
    #                           labels=["bound", "exact", "exact to bound"],
    #                           showfliers=False)
    #     ax1.set_xlabel("Maximum-Data Age")
    #     plt.savefig(filename)
    #

    # ----------------------- the following should suffice:

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
