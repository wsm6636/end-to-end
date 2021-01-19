"""Representation of the drawer that generates tikz code of a previous generated schedule.

:Filename: drawer.py
:Author: Marco Dürr (marco.duerr@tu-dortmund.de)
:Date: 18.06.18
"""


class Drawer:
    """Class Drawer

        **Global Variables**
            :cvar id: Unique identifier.
            :type id: String
            :cvar schedule: Execution times of each job of the related task.
            :type schedule: Dict
            :cvar trace_length: Time how long the schedule is executed.
            :type trace_length: Integer
            :cvar max_age: End-to-End timing analysis result under max age semantic.
            :type max_age: Float
            :cvar reaction: End-to-End timing analysis result under reaction semantic.
            :type reaction: Float

        **Usage**
            >>> import stt.drawer
            >>> myDrawer = stt.drawer.Drawer("d1", [])
    """
    id = None
    schedule = None
    trace_length = None
    scale = None
    max_age = None
    reaction = None
    latency = None

    def __init__(self, d_id, d_schedule, d_max_age, d_reaction, d_latency):
        self.id = d_id
        self.schedule = d_schedule[0]
        self.trace_length = d_schedule[1]
        self.max_age = d_max_age
        self.reaction = d_reaction
        self.latency = d_latency

    def draw(self):
        # TODO untereinander oder in einem darstellen
        file = open("output/schedule.tex", "w+")
        # Create latex header
        file.write("\\documentclass[10pt,a4paper]{standalone}\n")
        file.write("\\usepackage[latin1]{inputenc}\n")
        file.write("\\usepackage{tikz}\n")
        file.write("\\usetikzlibrary{arrows,decorations.markings}\n")
        file.write("\\begin{document}\n")
        file.write("\\begin{tikzpicture}\n")
        # Draw the schedule
        index = 0
        for task in self.schedule:
            # Scope with y-axis translation
            file.write("\\begin{scope}[shift={(0," + str(index*(-2)) + ")}]\n")
            # x-axis, it is drawn a little longer to have a clean ending
            file.write("\\draw[decoration={markings,mark=at position 1 with {\\arrow[scale=2]{>}}},postaction="
                       "{decorate}] (0, 0) -- (" + str(self.trace_length + 0.5) + ", 0);\n")
            # labeling of the x-axis
            file.write("\\foreach \\x/\\xtext in {0,1,2,...," + str(self.trace_length) + "} \pgfmathsetmacro\label{\\x}"
                       "\draw(\\x,5pt)--(\\x,-5pt) node[below] {\\pgfmathprintnumber{\\label}};\n")
            file.write("\\foreach \\x in {0.2,0.4,...," + str(self.trace_length) + "}  \draw (\\x,0) -- (\\x,-3pt);\n")
            # labeling of the task, TODO use the correct task names
            file.write("\\draw(-0.3,0.3) node[above] {$\\tau_" + str(index) + "$};\n")
            # unit of the x-axis
            file.write("\\draw(" + str(self.trace_length + 0.4) + ",-4pt) node[right] {$t$};\n")

            for tick in range(self.trace_length * 10):
                for execution in self.schedule[task]:
                    if tick / 10 == execution:
                        file.write("\draw[black] (" + format(tick / 10, ".1f") + ",0)rectangle (" +
                                   format(tick / 10 + 0.1, ".1f") + ",1);\n")
                if (((tick - task.phase) / 10) % task.period) == 0 and (tick >= task.phase):
                    file.write("\\draw[->, line width=2pt, color=blue] (" +
                               format(tick / 10, ".1f") + ",0) -- (" + format(tick / 10, ".1f") + ", 1.3);\n")
            # Drawing End-to-End Analysis
            if index == 0:
                shift = len(list(self.schedule.keys())) * -2 + 1
                file.write("\\draw[<->](" + str(self.max_age[1][0][0]) + "," + str(shift) + ")--(" + str(
                    self.max_age[1][len(list(self.schedule.keys())) - 1][1]) + "," + str(
                    shift) + ") node[below] {Max Age (" + str(self.max_age[0]) + ")};")
                file.write("\\draw[<->](" + str(self.reaction[1][0][0]) + "," + str(shift-1) + ")--(" + str(
                    self.reaction[1][len(list(self.schedule.keys())) - 1][1]) + "," + str(
                    shift-1) + ") node[below] {Reaction (" + str(self.reaction[0]) + ")};")
                file.write("\\node[shift={(0, " + str(shift-2) + " )}] {End-to-End Latency (" + str(self.latency) + ")};")
            file.write("\\end{scope}\n")
            index = index + 1
        # Close latex file
        file.write("\end{tikzpicture}\n")
        file.write("\end{document}\n")
        file.close()
