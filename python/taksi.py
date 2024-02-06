from taksioras import taksioras
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
import ast
import os, signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("TkAgg")

global G, pos, paths, start, end


def construct_graph(graph):
    G = nx.Graph()
    for vertex in range(0, len(graph.vertices)):
        neighbours = graph.vertices[vertex]
        for neighbour in neighbours:
            G.add_edge(vertex + 1, neighbour)
    return G


def draw():
    nx.draw(G,
            ax=ax,
            pos=pos,
            with_labels=True,
            font_color='#000000',
            node_size=400,
            font_weight='bold',
            node_color='#ffff00',
            width=5)
    nx.draw_networkx_nodes(G, ax=ax, pos=pos, nodelist=[start], node_size=2000, node_shape='^', node_color='black')
    nx.draw_networkx_nodes(G, ax=ax, pos=pos, nodelist=[end], node_size=2200, node_shape='v', node_color='black')
    nx.draw_networkx_nodes(G, ax=ax, pos=pos, nodelist=[end], node_size=2000, node_shape='v', node_color='yellow')
    nx.draw_networkx_labels(G, ax=ax, pos=pos, labels={start: start}, font_color='yellow', font_weight='bold')
    nx.draw_networkx_labels(G, ax=ax, pos=pos, labels={end: end}, font_color='black', font_weight='bold')


def animate(path, cur, all):
    print(path)

    edges = []
    edge_labels = {}
    nodes = []
    node_labels = {}

    for vertex in range(0, len(path) - 1):
        ax.clear()
        ax.text(0.95, 0.95, f'{cur}/{all}', ha='right', va='top', transform=fig.transFigure, fontsize=20,
                bbox=dict(facecolor='white', alpha=0.8))
        draw()
        edges.append((path[vertex], path[vertex + 1]))
        edge_labels[edges[vertex]] = vertex + 1
        nodes.append(path[vertex + 1])
        node_labels[path[vertex + 1]] = path[vertex + 1]

        nx.draw_networkx_edges(G, ax=ax, pos=pos, edgelist=edges, edge_color='red', width=7, arrows=True, arrowsize=30,
                               arrowstyle='->')
        nx.draw_networkx_nodes(G, ax=ax, pos=pos, nodelist=nodes, node_color='black', node_size=400, alpha=1)
        nx.draw_networkx_labels(G, ax=ax, pos=pos, labels=node_labels, font_weight='bold', font_color='yellow')
        nx.draw_networkx_edge_labels(G, ax=ax, pos=pos, edge_labels=edge_labels, font_color='black', font_weight='bold')

        canvas.draw()
        window.after(100)
        window.update()

        if window.state() != 'normal':
            os.kill(os.getpid(), signal.SIGKILL)


def animate_all():
    hide_ui()
    prepare_graph_data()
    canvas.get_tk_widget().pack(expand=True)
    for idx in range(0, len(paths)):
        path = paths[idx]
        animate(path, idx + 1, len(paths))
        window.after(800)
        window.update()


def hide_ui():
    start_button.pack_forget()
    path_frame.pack_forget()
    graph_frame.pack_forget()
    input_box_frame.pack_forget()
    start_end_frame.pack_forget()


def prepare_graph_data():
    global pos, paths, G, start, end
    width = int(grid_width_entry.get())
    height = int(grid_height_entry.get())
    graph = None

    if input_selection.get() == 'grid':
        graph = taksioras.Graph.new_grid(width, height)
        G = construct_graph(graph)
        pos = nx.spectral_layout(G)
    else:
        vertices = ast.literal_eval(text_input.get("1.0", "end-1c"))
        graph = taksioras.Graph(vertices)
        G = construct_graph(graph)
        pos = nx.spring_layout(G)

    loading_label = tk.Label(window, text="Skaičiuojami keliai... Kantrybės", font=('Helvetica', 20))
    loading_label.pack(anchor='center', expand=True, fill='both')
    window.update()
    window.after(100)

    start = int(start_entry.get())
    end = int(end_entry.get())
    paths = None
    if is_simple.get():
        paths = taksioras.Graph.longest_simple_paths(graph, start, end)
    else:
        paths = taksioras.Graph.longest_elementary_paths(graph, start, end)
    print_paths()

    loading_label.pack_forget()


def print_paths():
    for path in paths:
        print(path)
    print("Viso {}".format(len(paths)))


########################################################################################################################
# GUI

def activate_grid_creator():
    text_input.pack_forget()
    grid_frame.pack(anchor='w')
    start_end_frame.pack(anchor='sw')


def activate_custom_creator():
    text_input.pack(anchor='w')
    grid_frame.pack_forget()
    start_end_frame.pack(anchor='sw')


fig = plt.Figure(figsize=(100, 100), dpi=100)
ax = fig.add_subplot(111)

window = tk.Tk()
window.title('Taksioras')
window.geometry('800x800')
canvas = FigureCanvasTkAgg(fig, master=window)

start_button = tk.Button(window,
                         text='Važiuoti!',
                         width=25,
                         command=animate_all,
                         font=60)
start_button.pack(side='bottom')

#Path selection
path_frame = tk.Frame(window)
path_frame.pack(anchor='w', pady=10, padx=10)

is_simple = tk.BooleanVar(None, False)
radio_button_elementary = tk.Radiobutton(path_frame,
                                         text="Elementarieji keliai (negali kartotis viršūnė)",
                                         variable=is_simple,
                                         value=False,
                                         font=20)
radio_button_elementary.pack(anchor='w')
radio_button_simple = tk.Radiobutton(path_frame,
                                     text="Paprastieji keliai (negali kartotis briauna)",
                                     variable=is_simple,
                                     value=True,
                                     font=20)
radio_button_simple.pack(anchor='w')

#Graph selection
graph_frame = tk.Frame(window)
graph_frame.pack(anchor='w', pady=10, padx=10)
input_box_frame = tk.Frame(window)
input_box_frame.pack(anchor='sw', pady=10, padx=10)
input_selection = tk.StringVar(None, "grid")

#Grid
radio_button_grid = tk.Radiobutton(graph_frame,
                                   text="Tinklelis (grid)",
                                   font=20,
                                   variable=input_selection,
                                   value='grid',
                                   command=activate_grid_creator)
radio_button_grid.pack(anchor='w')

grid_frame = tk.Frame(input_box_frame)
grid_label = tk.Label(grid_frame, text="Tinklelio parametrai")
grid_label.grid(column=1)

width_label = tk.Label(grid_frame, text="Ilgis")
width_label.grid(row=1, column=0)
grid_width_entry = tk.Entry(grid_frame)
grid_width_entry.insert(0, '4')
grid_width_entry.grid(row=1, column=1)

height_label = tk.Label(grid_frame, text="Plotis")
height_label.grid(row=2, column=0)
grid_height_entry= tk.Entry(grid_frame)
grid_height_entry.insert(0, '4')
grid_height_entry.grid(row=2, column=1)

#Custom
radio_button_custom = tk.Radiobutton(graph_frame,
                                     text="Viršūnių matrica",
                                     font=20,
                                     variable=input_selection,
                                     value='custom',
                                     command=activate_custom_creator)
radio_button_custom.pack(anchor='sw')


text_input = tk.Text(input_box_frame, height=10, width=40)
example_graph = '''[
[2, 3, 5],
[1, 3, 4, 7],
[1, 2, 4, 5, 6],
[2, 3, 5, 6, 7],
[1, 3, 6],
[3, 4, 5],
[2, 4]
]'''
text_input.insert(tk.END, example_graph)

#Start-end
start_end_frame = tk.Frame(window)
start_end_frame.pack(anchor='sw', padx=10, pady=10)
start_label = tk.Label(start_end_frame, text="Pradžios viršūnė")
start_label.grid(row=0, column=0)
start_entry = tk.Entry(start_end_frame)
start_entry.insert(0, '1')
start_entry.grid(row=0, column=1)
end_label = tk.Label(start_end_frame, text="Pabaigos viršūnė")
end_label.grid(row=1, column=0)
end_entry = tk.Entry(start_end_frame)
end_entry.insert(0, '7')
end_entry.grid(row=1, column=1)

activate_grid_creator()
window.protocol("WM_DELETE_WINDOW", window.destroy)
window.mainloop()
