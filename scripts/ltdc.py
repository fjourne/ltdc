#!/usr/bin/python3
# coding: utf-8
import unidecode
import requests
import re

from graphviz import Graph

cookie = {
    'Cookie': 'wiki_wikiUserID=4; wiki_wikiUserName=Piell;'
              + ' wiki_wikiToken=c36a79b16a31568dbedd74442315fd0d; '
              + 'ltdc_pppe_wikiUserID=4;'
              + ' ltdc_pppe_wikiUserName=Piell;'
              + ' ltdc_pppe_wikiToken=c36a79b16a31568dbedd74442315fd0d;'
              + ' wiki_wiki_session=ilmc6k7e2vefmor20lmlg9k7lpjbpg6;'
              + ' ltdc_pppe_wiki_session=h0jvm1nh9cq1dp8gjhdl8uh2c23mvknp;'}

entente_color = '#006400'
opposition_color = '#800080'
famille_color = '#FFD700'


class Entry:
    lien = ''
    nom = ''
    nom_graph = ''
    a_suivre = ''
    localisation = []


class Trame(Entry):
    trame = []


class Groupe(Trame):
    groupe = []
    entente = []
    neutre = []
    opposition = []
    materiel = []


class Personnage(Groupe):
    joueur = False


class Materiel(Trame):
    pass


class Geographie(Entry):
    categorie = ''


node_periferies = {
    Personnage: '1',
    Groupe: '2',
    Trame: '1',
    Geographie: '1',
    Materiel: '1'
}
node_shapes = {
    Personnage: 'ellipse',
    Groupe: 'ellipse',
    Trame: 'octagon',
    Geographie: 'pentagon',
    Materiel: 'box'
}


def to_nom_graph(nom):
    """
    Converti un nom au format nom graph.
    :param nom: le nom a convertir
    :return:  le nom graph
    """
    nom_graph_tmp = unidecode.unidecode(nom)
    nom_graph = ''
    for a in nom_graph_tmp:
        if a.isalpha():
            nom_graph += a
    return nom_graph


def get_link_list(string):
    """
    :param string: la string a parser
    :return: la liste des liens "<a>" contenue dans la string
    """
    links_tmp = re.findall(r'<a href="([^"]*)"[^<]*</a>', string)
    links = []
    for link in links_tmp:
        links.append("https://louiki.elyseum.fr" + link)
    return links


def retreive_main_table(url):
    """
    Récupère le tableau principale d'une page
    :param url: l'url de la page
    :return: la liste double des lignes et cellule du tableau
    """
    page = requests.get(url, headers=cookie).text
    table = page.split("<table class=\"wikitable sortable\">")
    table.pop(0)
    table = table[0].split("</table>")
    # On nétoie les fins de cellule et fin de ligne.
    table = table[0].split("<tr>")
    table.pop(0)
    # La 1ère ligne est le ligne de titre du tableau
    table.pop(0)

    tmp_table = []
    for row in table:
        row = row.replace("\n</td>\n", "").replace("\n</td></tr>\n", "")
        row = row.split("<td>")
        row.pop(0)
        tmp_table.append(row)
    return tmp_table


def retreive_personnnages():
    """
    :return: le tableau des personnages
    """
    tableau_personnages = retreive_main_table("https://louiki.elyseum.fr/ltdc_pppe/index.php/Graphe_Personnages")
    personnages = []
    for p in tableau_personnages:
        perso = Personnage()
        perso.lien = get_link_list(p[0])[0]
        perso.nom = p[1]
        perso.nom_graph = to_nom_graph(p[1])
        perso.localisation = get_link_list(p[2])
        perso.groupe = get_link_list(p[3])
        perso.famille = get_link_list(p[4])
        perso.entente = get_link_list(p[5])
        perso.neutre = get_link_list(p[6])
        perso.opposition = get_link_list(p[7])
        perso.materiel = get_link_list(p[8])
        perso.trame = get_link_list(p[9])
        perso.joueur = p[10] != ''
        personnages.append(perso)
    return personnages


def retreive_groupes():
    """
    :return: le tableau des groupes
    """
    tableau_groupes = retreive_main_table("https://louiki.elyseum.fr/ltdc_pppe/index.php/Graphe_Groupes")
    groupes = []
    for g in tableau_groupes:
        groupe = Groupe()
        groupe.lien = get_link_list(g[0])[0]
        groupe.nom = g[1]
        groupe.nom_graph = to_nom_graph(g[1])
        groupe.localisation = get_link_list(g[2])
        groupe.groupe = get_link_list(g[3])
        groupe.entente = get_link_list(g[4])
        groupe.neutre = get_link_list(g[5])
        groupe.opposition = get_link_list(g[6])
        groupe.materiel = get_link_list(g[7])
        groupe.trame = get_link_list(g[8])
        groupes.append(groupe)
    return groupes


def retreive_trames():
    """
    :return: le tableau des trames
    """
    tableau_trames = retreive_main_table("https://louiki.elyseum.fr/ltdc_pppe/index.php/Graphe_Trames")
    trames = []
    for t in tableau_trames:
        trame = Trame()
        trame.lien = get_link_list(t[0])[0]
        trame.nom = t[1]
        trame.nom_graph = to_nom_graph(t[1])
        trame.localisation = get_link_list(t[2])
        trame.trame = get_link_list(t[3])
        trame.a_suivre = t[4]
        trames.append(trame)
    return trames


def retreive_geographie():
    """
    :return: le tableau de la géographie
    """
    tableau_geographie = retreive_main_table("https://louiki.elyseum.fr/ltdc_pppe/index.php/Graphe_G%C3%A9ographie")
    geographie = []
    for g in tableau_geographie:
        lieu = Geographie()
        lieu.lien = get_link_list(g[0])[0]
        lieu.nom = g[1]
        lieu.nom_graph = to_nom_graph(g[1])
        lieu.localisation = get_link_list(g[2])
        lieu.categorie = g[3]
        geographie.append(lieu)
    return geographie


def retreive_materiels():
    """
    :return: le tableau des mateliers.
    """
    tableau_materiels = retreive_main_table("https://louiki.elyseum.fr/ltdc_pppe/index.php/Graphe_Mat%C3%A9riels")
    materiels = []
    for m in tableau_materiels:
        materiel = Materiel()
        materiel.lien = get_link_list(m[0])[0]
        materiel.nom = m[1]
        materiel.nom_graph = to_nom_graph(m[1])
        materiel.localisation = get_link_list(m[2])
        materiel.trame = get_link_list(m[3])
        materiel.a_suivre = m[4]
        materiels.append(materiel)
    return materiels


def add_nodes_types_shape(dot, entries):
    """
    Ajoute les entrées au graph
    :param dot: le graph
    :param entries: une liste d'entrée a ajouter dans le graph
    """
    for e in entries:
        color = 'white'
        if e.a_suivre != '':
            if e.a_suivre != 'Non':
                # red
                color = '#e41a1c'
            else:
                color = '#999999'

        elif isinstance(e, Personnage) and e.joueur:
            # vert
            color = '#4daf4a'
        dot.node(e.nom_graph, e.nom, link=e.lien,
                 shape=node_shapes.get(e.__class__),peripheries=node_periferies.get(e.__class__), fillcolor=color)


def create_link(dot, link_to_nomgraph, entry, link, fillcolor="#000000"):
    """
    Créé un lien dans le graph
    :param dot: le graph
    :param link_to_nomgraph: le dictionnaire de lien nom graph
    :param entry: l'objet du quel le lien est crée
    :param link: le lien de l'objet destination
    :param fillcolor: (optionel) la couleur.
    """
    if link in link_to_nomgraph:
        if isinstance(entry, Geographie):
            dot.edge(entry.nom_graph, link_to_nomgraph.get(link), entry.categorie, fillcolor=fillcolor)
        else:
            dot.edge(entry.nom_graph, link_to_nomgraph.get(link), fillcolor=fillcolor)
    else:
        print("Erreur : aucune page pour le lien '" + link + "' pour l'entitée '" + entry.nom + "'")


def build_link_to_nom_graph_dict(*entries_list):
    """
    Contruit le dictionnaire des liens -> nom_graph
    :param entries_list: un tableau de liste d'entrée
    :return: le dictionnaire contruit
    """
    link_to_nom_graph = {}
    for el in entries_list:
        for e in el:
            link_to_nom_graph[e.lien] = e.nom_graph
    return link_to_nom_graph


def add_link_trames(dot, link_to_nomgraph, trames):
    """
    Ajoute le lien des trames.
    :param dot: le graph
    :param link_to_nomgraph: le dictionnaire des liens nom graph
    :param trames: un liste de trames
    """
    for e in trames:
        for link in e.localisation:
            create_link(dot, link_to_nomgraph, e, link)
        for link in e.trame:
            create_link(dot, link_to_nomgraph, e, link)


def add_link_geographie(dot, link_to_nomgraph, geographie):
    """
    Ajoute le lien des geographie.
    :param dot: le graph
    :param link_to_nomgraph: le dictionnaire des liens nom graph
    :param trames: un liste de geographie
    """
    for e in geographie:
        for link in e.localisation:
            create_link(dot, link_to_nomgraph, e, link)


def add_link_materiels(dot, link_to_nomgraph, materiels):
    """
    Ajoute le lien des trames.
    :param dot: le graph
    :param link_to_nomgraph: le dictionnaire des liens nom graph
    :param trames: un liste de trames
    """
    add_link_trames(dot, link_to_nomgraph, materiels)


def add_link_groupes(dot, link_to_nomgraph, groupes):
    """
    Ajoute le lien des groupes.
    :param dot: le graph
    :param link_to_nomgraph: le dictionnaire des liens nom graph
    :param trames: un liste de groupes
    """
    add_link_trames(dot, link_to_nomgraph, groupes)
    for e in groupes:
        for link in e.groupe:
            create_link(dot, link_to_nomgraph, e, link)
        for link in e.entente:
            create_link(dot, link_to_nomgraph, e, link, entente_color)
        for link in e.neutre:
            create_link(dot, link_to_nomgraph, e, link)
        for link in e.opposition:
            create_link(dot, link_to_nomgraph, e, link, opposition_color)
        for link in e.materiel:
            create_link(dot, link_to_nomgraph, e, link)


def add_link_personnages(dot, link_to_nomgraph, personnages):
    """
    Ajoute le lien des personnages.
    :param dot: le graph
    :param link_to_nomgraph: le dictionnaire des liens nom graph
    :param trames: un liste de personnages
    """
    add_link_groupes(dot, link_to_nomgraph, personnages)
    for e in personnages:
        for link in e.famille:
            create_link(dot, link_to_nomgraph, e, link, famille_color)


def main():
    """
    Main
    """
    print("Content-type: text/html\r\n\r\n")

    personnages = retreive_personnnages()
    groupes = retreive_groupes()
    trames = retreive_trames()
    geographies = retreive_geographie()
    materiels = retreive_materiels()

    link_to_nomgraph = build_link_to_nom_graph_dict(personnages, groupes, trames, geographies, materiels)

    dot = Graph(name='Dragons', filename='./tmp/derniersDragons.gv', comment='Les Derniers Dragons', strict=True)
    add_nodes_types_shape(dot, personnages)
    add_nodes_types_shape(dot, groupes)
    add_nodes_types_shape(dot, trames)
    add_nodes_types_shape(dot, geographies)
    add_nodes_types_shape(dot, materiels)
    add_link_personnages(dot, link_to_nomgraph, personnages)
    add_link_groupes(dot, link_to_nomgraph, groupes)
    add_link_trames(dot, link_to_nomgraph, trames)
    add_link_geographie(dot, link_to_nomgraph, geographies)
    add_link_materiels(dot, link_to_nomgraph, materiels)

    dot.save()
    print("done")


main()
