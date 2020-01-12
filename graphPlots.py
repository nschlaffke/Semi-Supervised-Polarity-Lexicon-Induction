import igraph as ig

def plotWithLabels(graph):
    graph.vs()["label"] = graph.vs()["name"]
    ig.plot(graph)

def plotWithLabelsCustom(graph, properties):
    ig.plot(graph, **properties)

def plotBigKKLayoutWithLabels(graph):
    layout = graph.layout("kk")

    visual_style = {}
    visual_style["vertex_size"] = 20
    visual_style["vertex_color"] = "blue"
    visual_style["vertex_label"] = graph.vs["name"]
    visual_style["edge_width"] = 1
    visual_style["layout"] = layout
    visual_style["bbox"] = (1200, 1200)
    visual_style["margin"] = 20

    plotWithLabelsCustom(graph, visual_style)


def simplePlot(graph):
    ig.plot(graph)

def plotCommunity(communities):
    ig.plot(communities, mark_groups = True)
