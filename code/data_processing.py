import json
import matplotlib.pyplot as plt


file_nodes = '/Applications/XAMPP/xamppfiles/htdocs/visualization/data/occupations_nodes.csv'
file_edges = '/Applications/XAMPP/xamppfiles/htdocs/visualization/data/occupations_edges.csv'
file_financial_skills = '/Applications/XAMPP/xamppfiles/htdocs/visualization/data/skills_financial.csv' 
centrality_measures = '/Applications/XAMPP/xamppfiles/htdocs/visualization/data/Centrality_measure_all occupation.csv'

def data_forcedirected():
    f = open(file_nodes, 'r')

    graph = {}
    graph['nodes'] = []
    nodes = []
    for entry in f.readlines():
        nodes.append(entry.strip())
        graph['nodes'].append({"name": entry.strip(), "group":entry.strip().split('-')[0]})

    f = open(file_edges, 'r')
    graph['links'] = []
    for entry in f.readlines()[1:]:
        graph['links'].append({"source": nodes.index(entry.strip().split(',')[0]), "target": nodes.index(entry.strip().split(',')[1]), "weight": 1})

    json.dump(graph, open('/Applications/XAMPP/xamppfiles/htdocs/visualization/data/data.json', 'w'), indent=2)


def data_hierarchical_edgebundling():

    graph = {}

    f = open(file_edges, 'r')
    for entry in f.readlines()[1:]:
        source = entry.strip().split(',')[0]
        target = entry.strip().split(',')[1]

        if source not in graph:
            graph[source] = {}
            graph[source]['size'] = 0
            graph[source]['imports'] = []
        if target not in graph:
            graph[target] = {}
            graph[target]['size'] = 0
            graph[target]['imports'] = []

        if source not in graph[target]['imports']:
            graph[target]['size'] += 1
            graph[target]['imports'].append(source)
        if target not in graph[source]['imports']:
            graph[source]['size'] += 1
            graph[source]['imports'].append(target)
    
    output = []
    for key in graph:
        output.append({"name": key, "size": graph[key]['size'], "imports": graph[key]['imports']})
         
    json.dump(output, open('/Applications/XAMPP/xamppfiles/htdocs/visualization/data/data_hierarchical_edgebundling.json', 'w'), indent=2)


def data_financial_hierarchical_edgebundling():
   
    financial_occupations = get_financial_occupations()
    
    output = {}
    output['nodes'] = list(financial_occupations)
    nodes = [node['name'] for node in financial_occupations]
 
    output['links'] = []
    f = open(file_edges, 'r')
    for entry in f.readlines()[1:]:
        source = entry.strip().split(',')[0]
        target = entry.strip().split(',')[1]
        if source not in nodes or target not in nodes:
            continue
        link = {'source': source, 'target': target}
        output['links'].append(link)
    
    json.dump(output, open('/Applications/XAMPP/xamppfiles/htdocs/visualization/data/data_financial_hierarchical_edgebundling.json', 'w'), indent=2)

 
def get_financial_occupations():
    f = open(file_financial_skills, 'r')
    financial_occupations = {*[line.split(',')[1] for line in f.readlines()[1:]]}
    financial_occupations = [{"name": node} for node in financial_occupations]
    return financial_occupations
    

def get_financial_skills():
    f = open(file_financial_skills, 'r')
    output = {}
    output['name'] = 'skills'
    output['nodes'] = []
    output['children'] = {}

    occupation_skill_map = {}
    for line in f.readlines()[1:]:
        skill, occupation, weight = line.strip().split(',')
        output['nodes'].append(skill)
        if occupation not in occupation_skill_map:
            occupation_skill_map[occupation] = []
        occupation_skill_map[occupation].append({'name': skill, 'size': weight})

    for occupation in occupation_skill_map:
        output['children'][occupation] = {'name': occupation, 'children': occupation_skill_map[occupation]}

    json.dump(output, open('/Applications/XAMPP/xamppfiles/htdocs/visualization/data/financial_skills.json', 'w'), indent=4)



def process_data():
    occupations = [str(i) + '-0000' for i in range(11, 57, 2)]
    edges = [line.strip().split(',') for line in open(file_edges, 'r').readlines()[1:]]
    output = {}
    output['nodes'] = [{'name': occupation} for occupation in occupations]
    output['links'] = []
    for [source, target] in edges:
        source = source.split('-')[0] + '-0000'
        target = target.split('-')[0] + '-0000'
        output['links'].append({'source': source, 'target': target})
    json.dump(output, open('/Applications/XAMPP/xamppfiles/htdocs/visualization/data/occupations_graph.json', 'w'), indent=4)


def process_subgraph_data():
    occupations = [str(i) + '-0000' for i in range(11, 57, 2)]
    edges = [line.strip().split(',') for line in open(file_edges, 'r').readlines()[1:]]
    nodes = [line.strip() for line in open(file_nodes, 'r').readlines()]
    output = {}
    for occupation in occupations:
        output[occupation] = {}
        output[occupation]['nodes'] = []
        output[occupation]['links'] = []

    for node in nodes:
        occupation = node.split('-')[0] + '-0000'
        output[occupation]['nodes'].append({'name': node})

    for [source, target] in edges:
        source_occupation = source.split('-')[0] + '-0000'
        target_occupation = target.split('-')[0] + '-0000'
        if source_occupation == target_occupation:
            output[source_occupation]['links'].append({'source': source, 'target': target})
    json.dump(output, open('/Applications/XAMPP/xamppfiles/htdocs/visualization/data/occupations_subgraph.json', 'w'), indent=4)


def visualize_centrality():
    f = open(centrality_measures, 'r')
    data = {}
    header = f.readline()
    centralities = header.strip().split(',')[1:]
    for line in f.readlines():
        occupation, c0, c1, c2 = line.strip().split(',')
        group = occupation.split('-')[0]
        if group not in data:
            data[group] = {}
            for centrality in centralities:
                data[group][centrality] = []
        data[group][centralities[0]].append(float(c0))
        data[group][centralities[1]].append(float(c1))
        data[group][centralities[2]].append(float(c2))
    count = 0
    for j in range(len(list(data.keys())[0:5])):
        for i in range(3):
	        plt.subplot(len(list(data.keys())[0:5]), 3, count+1)
	        count += 1
	        y = data[list(data.keys())[0:5][j]][centralities[i]]
	        x = range(len(y))
	        plt.scatter(x, y)
	        plt.plot(x, y, 'r')
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
    plt.show()
    
visualize_centrality()

#get_financial_skills()

#process_subgraph_data()


