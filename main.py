import algorithmx
import networkx as nx

from services.worksheet import read_excel_file

DATA = {
    'Institucional': {'mainColor': 'blue', 'secondaryColor': 'lightblue', 'columnIndex': -2, 'labelIndex': 315,
                      'yearIndex': 0},
    'Científico': {'mainColor': 'green', 'secondaryColor': 'lightgreen', 'columnIndex': -4, 'labelIndex': 315,
                   'yearIndex': 0},
    'Histórico': {'mainColor': 'pink', 'secondaryColor': 'lightpink', 'columnIndex': 3, 'labelIndex': 225,
                  'yearIndex': 180},
}

COLOR = {
    'Alemanha': '#f9cb9c',
    'Dinamarca': '#b4a7d6',
    'Escócia': '#d9ead3',
    'Estados Unidos': '#c9daf8',
    'Europa': '#ffd966',
    'Europa e Estados Unidos': '#ffd966',
    'Europa Ocidental': '#ffd966',
    'França': '#bf9000',
    'França e Alemanha': '#f9cb9c',
    'Incerto': 'black',
    'Inglaterra': '#d9ead3',
    'Itália': '#fff2cc',
    'Mundo': '#cccccc',
    'Reino Unido': '#d9ead3',
    'Suiça': '#f6b26b',
    'União Soviética e Ocidente': '#e06666',
    'URSS': '#e06666',
}

server = algorithmx.http_server(port=5050)
canvas = server.canvas()

lines = read_excel_file(filename='linha-do-tempo-2.xlsx', sheet_name='FINAL')

T = nx.Graph()

nodes = [(line['Evento'], line) for line in lines]
nline = [float(line['Escala']) if line['Escala'] != 'None' else 0 for line in lines]
T.add_nodes_from(nodes)


def inodes_positioning() -> dict:
    ncoords = dict()
    for index in range(len(T.nodes) + 1):
        if index == 0:
            line = 0
        else:
            line = ncoords[index - 1][1] - (4 * 10) - nline[index - 1]
        ncoords[index] = (0, line)
    return ncoords


def start():
    inposition = inodes_positioning()
    inode = 1

    index = 0
    for key, value in COLOR.items():
        labels = {0: {'remove': True}}
        canvas.node(key).add(pos=(-700, index * (-1)), color=value, size=6, labels=labels).label('color').add(text=key,
                                                                                                              angle=0)
        index += (8 * 4)

    for node in T.nodes:

        ndata: dict = T.nodes[node]
        ntype: str = ndata['Tipo']

        ncolor, scolor = DATA[ntype]['mainColor'], DATA[ntype]['secondaryColor']
        ipos = inposition[inode]

        year, yangle = ndata.get('Ano') or 'Não Especificado', DATA[ntype]['yearIndex']
        event, eangle = node, DATA[ntype]['labelIndex']

        svgattrs = {'stroke-width': 2, 'stroke': scolor}
        labels = {0: {'remove': True}}

        npos = (DATA[ntype]['columnIndex'] * -15, ipos[1])

        color = COLOR[ndata['Espaço']]

        # First Node
        if inode == 1: canvas.node(0).add(pos=inposition[0], shape='circle', labels=labels, size=3, fixed=True,
                                          draggable=False).visible(False)

        # Identification Node
        canvas.node(inode).add(pos=ipos, shape='rect', size=4, color=ncolor, labels=labels, fixed=True, draggable=False,
                               svgattrs=svgattrs, )

        # Event Node
        canvas.node(node).add(pos=npos, size=4, color=color, labels=labels, fixed=True, draggable=False)
        canvas.node(node).label('evento').add(text=event, color='black', angle=eangle)
        canvas.node(node).label('ano').add(text=year, angle=yangle, color='black', )

        # Connection
        canvas.edges([(inode - 1, inode), (inode, node)]).add().thickness(1).color('black')
        inode += 1

    for number in range(70):
        canvas.duration(1).zoom(1).pan([0, -100 * number]).pause(1)


canvas.onmessage('start', start)
server.start()
