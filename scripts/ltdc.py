import requests
import re
from graphviz import Graph

cookie = {
    'Cookie': 'wiki_wikiUserID=7; wiki_wikiUserName=Fabien;'
              + ' wiki_wikiToken=8e8703c517db1ef0343181e2da1a2224; '
              + 'ltdc_pppe_wikiUserID=7;'
              + ' ltdc_pppe_wikiUserName=Fabien;'
              + ' ltdc_pppe_wikiToken=8e8703c517db1ef0343181e2da1a2224;'
              + ' wiki_wiki_session=c52v051pcbu9e26clhrnjivr8941sd20;'
              + ' ltdc_pppe_wiki_session=tgk3v637iovmj0vve6cp8rv4h1snp03d'}
page_perso = requests.get("http://louiki.elyseum.fr/ltdc_pppe/index.php?title=Personnages&action=edit",
                          headers=cookie).text

page_groupe = requests.get("http://louiki.elyseum.fr/ltdc_pppe/index.php?title=Groupes_et_organisations&action=edit",
                           headers=cookie).text

page_trame = requests.get("http://louiki.elyseum.fr/ltdc_pppe/index.php?title=Trames&action=edit", headers=cookie).text

page_event = requests.get("http://louiki.elyseum.fr/ltdc_pppe/index.php?title=Trames_locales&action=edit",
                          headers=cookie).text

page_lieu = requests.get("http://louiki.elyseum.fr/ltdc_pppe/index.php?title=G%C3%A9ographie&action=edit",
                         headers=cookie).text

page_role = requests.get("http://louiki.elyseum.fr/ltdc_pppe/index.php?title=Connaissances_diverses&action=edit",
                         headers=cookie).text

page_materiel = requests.get("http://louiki.elyseum.fr/ltdc_pppe/index.php?title=Mat%C3%A9riel&action=edit",
                             headers=cookie).text

page_edge = requests.get("http://louiki.elyseum.fr/ltdc_pppe/index.php?title=Liens&action=edit", headers=cookie).text


dot = Graph(name='Dragons', filename='derniersDragons.gv', comment='Les Derniers Dragons', strict=True)


def get_nomgraph(content):
    """
    :param content: le texte dans lequel on recherche
    :return: le nomgraph associé
    """
    return re.findall("nomgraphe=(.*)\n", content)[0]


def get_link(content):
    return re.findall("lien=(.*)\n", content)[0]


def map_link_nomgraph(content):
    dico = {}
    for c in content:
        n = get_nomgraph(c)
        l = get_link(c)
        dico[l] = n
    return dico


def get_line(content, search):
    """
    :param content: le text dans lequel on recherche la ligne.
    :param search: le type de la ligne rechercher (groupe, trame, localisation,...)
    :return: le reste de la ligne "" si non trouvée.
    """
    line = re.findall("{}=(.*)\n".format(search), content)
    line = line[0] if len(line) > 0 else ""
    return line


def line_to_list(line, search):
    """
    :param line: le texte de la ligne
    :param search: le type de lien rechercher dans la ligne (g, gr, t, tl, ...)
    :return: la liste des liens trouvers dans la ligne
    """
    return re.findall("[^\{]*(\{\{" + search + "\|[^\}]+\}\})", line)


def get_link_list(content, attribut, link):
    """
    :param content: le texte dans lequel rechecher
    :param attribut: l'attibut du "personnage/groupe/..." dans lequel rechercher "(groupe, trame, localisation)...
    :param link: les liens recherchers g, gr, t, tl, ...
    :return: la liste des liens trouvers.
    """
    return line_to_list(get_line(content, attribut), link)


def add_nodes_types_shape(types, shape, linkname, peripheries='1', linkpers='', link=''):
    """
    :param types: modèle concerné
    :param shape: shape du node pour ce modèle
    :param linkname: lien vers le wiki dans le cas où c'est lien + nom
    :param peripheries: nombre de délimitations autour d'un noeud
    :param linkpers: lien dans le cas ou c'est lien + link
    :param link: lien dans le cas ou c'est juste lien
    :return:
    """
    for t in types:
        nomgraph = re.findall("nomgraphe=(.*)\n", t)[0]
        nom = re.findall("nom=(.*)\n", t)[0]
        color = 'white'
        if get_line(t, 'ferme'):
            # grey
            color = '#999999'
        elif get_line(t, 'asuivre'):
            # red
            color = '#e41a1c'
        elif get_line(t, 'joueur'):
            # vert
            color = '#4daf4a'
        if linkname != '':
            dot.node(nomgraph, nom, shape=shape, link=linkname + nom, peripheries=peripheries, fillcolor=color)
        elif linkpers != '':
            lien = re.findall("lien=\{\{.*\|(.*)\}\}\n", t)[0]
            dot.node(nomgraph, nom, shape=shape, link=linkpers + lien, peripheries=peripheries, fillcolor=color)
        else:
            dot.node(nomgraph, nom, shape=shape, link=link, peripheries=peripheries, fillcolor=color)
    return


personnages = page_perso.split("{{Personnage")
personnages.pop(0)
p_link_to_nomgraphe = map_link_nomgraph(personnages)


groupes = page_groupe.split("{{Groupe")
groupes.pop(0)
gr_link_to_nomgraphe = map_link_nomgraph(groupes)

trames = page_trame.split("{{Trame")
trames.pop(0)
tr_link_to_nomgraphe = map_link_nomgraph(trames)

events = page_event.split("{{Trame")
events.pop(0)
ev_link_to_nomgraphe = map_link_nomgraph(events)

lieux = page_lieu.split("{{Géographie")
lieux.pop(0)
l_link_to_nomgraphe = map_link_nomgraph(lieux)

roles = page_role.split("{{Role")
roles.pop(0)
r_link_to_nomgraphe = map_link_nomgraph(roles)

materiels = page_materiel.split("{{Objet")
materiels.pop(0)
m_link_to_nomgraphe = map_link_nomgraph(materiels)

edges = page_edge.split("{{Edge")
edges.pop(0)

categories = [
    (personnages, p_link_to_nomgraphe, "personnages", "p"),
    (groupes, gr_link_to_nomgraphe, "groupe", "gr"),
    (trames, tr_link_to_nomgraphe, "trame", "t"),
    (events, ev_link_to_nomgraphe, "trame", "tl"),
    (roles, r_link_to_nomgraphe, "role", "r"),
    (materiels, m_link_to_nomgraphe, "materiel", "o"),
    (lieux, l_link_to_nomgraphe, "localisation", "g")
]

# Ajouts des nodes persos
add_nodes_types_shape(personnages, 'ellipse', '', '1', 'http://louiki.elyseum.fr/ltdc_pppe/index.php/Personnages#')

# Ajouts des nodes groupes
add_nodes_types_shape(groupes, 'ellipse', 'http://louiki.elyseum.fr/ltdc_pppe/index.php/Groupes_et_organisations#', '2')

# Ajouts des nodes trames, events, lieux, objets, roles
add_nodes_types_shape(trames, 'octagon', 'http://louiki.elyseum.fr/ltdc_pppe/index.php/Trames#', '2')
add_nodes_types_shape(events, 'octagon', 'http://louiki.elyseum.fr/ltdc_pppe/index.php/Trames_locales#')
add_nodes_types_shape(lieux, 'box', 'http://louiki.elyseum.fr/ltdc_pppe/index.php/G%C3%A9ographie#')
add_nodes_types_shape(materiels, 'invhouse', 'http://louiki.elyseum.fr/ltdc_pppe/index.php/Mat%C3%A9riel#')
add_nodes_types_shape(roles, 'pentagon', '', '1', '',
                      'http://louiki.elyseum.fr/ltdc_pppe/index.php/Connaissances_diverses#Tarot_de_Targ.C3.A8ne')

error = ""

for ci in range(len(categories)-1):
    for element in categories[ci][0]:
        nomgraph = get_nomgraph(element)
        for sci in range(ci, len(categories)):
            links = get_link_list(element, categories[sci][2], categories[sci][3])
            for link in links:
                if link in categories[sci][1]:
                    dot.edge(nomgraph, categories[sci][1][link])
                else:
                    error += "Lien non trouvé : {} dans {}\n".format(link, nomgraph)


# Contruction des liens lieu vers lieu
for l in lieux:
    nomgraph = get_nomgraph(l)
    colonies_lieu = get_link_list(l, "coloniede", "g")
    for c in colonies_lieu:
        dot.edge(nomgraph, l_link_to_nomgraphe[c], 'Colonie')
    villes_lieu = get_link_list(l, "villede", "g")
    for v in villes_lieu:
        dot.edge(nomgraph, l_link_to_nomgraphe[v], 'Ville')

# Ajouts des liens manuels
for e in edges:
    head = re.findall("head=(.*)\n", e)[0]
    tails = re.findall("tails=(.*)\n", e)[0]
    label = re.findall("label=(.*)\n", e)[0]
    if label:
        dot.edge(head, tails, label)
    else:
        dot.edge(head, tails)

dot.save()
print(error)