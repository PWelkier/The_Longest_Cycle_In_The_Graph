import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class GraphEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Edytor grafu")
        self.canvas = None
        self.graph = nx.DiGraph()
        self.node_positions = {}
        self.current_node = None
        self.start_edge_node = None
        self.edge_start = None
        self.finish_button = None
        self.finished = False
        self.is_in_progress = False
        self.counter = 0
        self.finish_nodes = False
        self.create_widgets()

    def create_widgets(self):
        self.graph_fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.graph_fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = self.graph_fig.add_subplot(111)
        self.ax.set_facecolor('white')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.canvas.draw()

        self.add_node_button = tk.Button(self.root, text="+ Dodaj wierzch.", command=self.add_node)
        self.add_node_button.pack(side=tk.LEFT)

        self.finish_button = tk.Button(self.root, text="Zakoncz dodawanie", command=self.finish)
        self.finish_button.pack(side=tk.LEFT)

        self.find_cycle_button = tk.Button(self.root, text="Znajdź najdłuższy cykl", command=self.display_longest_cycle)
        self.find_cycle_button.pack(side=tk.LEFT)

        self.instructions_button = tk.Button(self.root, text="Instrukcja", command=self.display_instructions)
        self.instructions_button.pack(side=tk.LEFT)

        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def display_instructions(self):
        messagebox.showinfo("Instrukcja", "Program szukający najdłuższego cyklu w grafie skierowanym\n\n"
                                          "Instrukcja:\n"
                                          "1. Aby dodać wierzchołek, kliknij przycisk '+ Dodaj wierzch.'\n"
                                          "2. Gdy skończysz dodawać wierzchołki, kliknij przycisk 'Zakoncz dodawanie'\n"
                                          "3. Aby połączyć dwa wierzchołki, kliknij lewym przyciskiem na wierzchołek początkowy i prawym na drugi wierzchołek\n"
                                          "4. Po dodaniu wszystkich krawędzi, użyj przycisku 'Znajdź najdłuższy cykl' aby obliczyć najdłuższy cykl.\n\n"
                                          "Ograniczenia:\n"
                                          "1. Nie można prowadzić krawędzi do tego samego wierzchołka\n"
                                          "2. Krawędzie pomiędzy tymi samymi wierzchołkami są jednokierunkowe")
    def add_node(self):
        node_label = str(self.counter)
        self.counter += 1
        self.current_node = node_label
        self.graph.add_node(node_label)
        self.node_positions = self.calculate_node_positions()
        self.draw()

    def calculate_node_positions(self):
        num_nodes = len(self.graph.nodes)
        angle_step = 2 * math.pi / num_nodes
        radius = 0.4
        return {node: (0.5 + radius * math.cos(i * angle_step), 0.5 + radius * math.sin(i * angle_step))
                for i, node in enumerate(self.graph.nodes)}

    def add_edge(self, node1, node2):
        self.graph.add_edge(node1, node2)
        self.draw()

    def draw(self):
        self.ax.clear()
        nx.draw(self.graph, pos=self.node_positions, ax=self.ax, with_labels=True, node_size=500,
                node_color='skyblue', font_size=12, arrows=True)
        self.canvas.draw()

    def on_click(self, event):
        if event.inaxes == self.ax and not self.finished and self.finish_nodes:
            if event.button == 1:  # Left click to select node
                for node, pos in self.node_positions.items():
                    if (pos[0] - event.xdata) ** 2 + (pos[1] - event.ydata) ** 2 <= 0.01:
                        self.start_edge_node = node
                        self.is_in_progress = True
                        return
                self.start_edge_node = None
            elif event.button == 3 and self.start_edge_node:  # Right click to add edge
                for node, pos in self.node_positions.items():
                    if (pos[0] - event.xdata) ** 2 + (pos[1] - event.ydata) ** 2 <= 0.01 and node != self.start_edge_node:
                        self.add_edge(self.start_edge_node, node)
                        self.is_in_progress = False
                        return
                self.is_in_progress = False
            elif event.button == 2:  # Middle click to deselect node
                self.start_edge_node = None

    def on_motion(self, event):
        if event.inaxes is not None and self.start_edge_node:
            self.edge_start = self.node_positions[self.start_edge_node]
            self.ax.clear()
            self.ax.plot([self.edge_start[0], event.xdata], [self.edge_start[1], event.ydata], 'r--')
            self.ax.autoscale(enable=False)
            if not self.is_in_progress:
                self.draw()
            else:
                nx.draw(self.graph, pos=self.node_positions, ax=self.ax, with_labels=True, node_size=500,
                        node_color='skyblue', font_size=12, arrows=True)
                self.canvas.draw()

    def finish(self):
        if not self.finish_nodes:
            self.add_node_button.config(state=tk.DISABLED)
            self.finish_nodes = True
        else:
            self.finished = True
            self.finish_button.config(state=tk.DISABLED)

    def find_longest_cycle(self):
        self.longest_cycle = []
        visited = set()
        path = []

        def dfs(v):
            nonlocal path, visited
            path.append(v)
            visited.add(v)
            max_cycle = []
            for u in self.graph.successors(v):
                if u in path:
                    cycle = path[path.index(u):]
                    if len(cycle) > len(max_cycle):
                        max_cycle = cycle
                elif u not in visited:
                    result = dfs(u)
                    if len(result) > len(max_cycle):
                        max_cycle = result
            path.pop()
            visited.remove(v)
            return max_cycle

        # Check each node as a possible cycle start point
        for node in self.graph.nodes():
            if node not in visited:
                current_cycle = dfs(node)
                if len(current_cycle) > len(self.longest_cycle):
                    self.longest_cycle = current_cycle

        return self.longest_cycle

    def display_longest_cycle(self):
        all_cycles = list(nx.simple_cycles(self.graph))
        if all_cycles:
            longest_cycle = max(all_cycles, key=len)
            print("All cycles found:")
            for cycle in all_cycles:
                print(cycle)
            messagebox.showinfo("Najdłuższy cykl", f"Najdłuższy cykl to: {longest_cycle}")
            self.highlight_cycle(longest_cycle)
        else:
            messagebox.showinfo("Najdłuższy cykl", "Nie znaleziono cyklu.")

    def highlight_cycle(self, cycle):
        self.draw()  # Redraw the graph to clear previous highlights
        node_colors = ['skyblue' if node not in cycle else 'lightgreen' for node in self.graph.nodes()]
        edge_colors = ['black' if (u, v) not in zip(cycle, cycle[1:] + [cycle[0]]) else 'red' for u, v in self.graph.edges()]
        nx.draw(self.graph, pos=self.node_positions, ax=self.ax, with_labels=True, node_size=500,
                node_color=node_colors, edge_color=edge_colors, font_size=12, arrows=True)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphEditor(root)
    root.mainloop()
