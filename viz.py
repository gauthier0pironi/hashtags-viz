from pattern.graph import Graph
import MySQLdb
#########
#########
#########
keyword = 'ebola'
limit_tweets_to_analyse = 10000
db = MySQLdb.connect(host="127.0.0.1", user="python",
                  passwd="python", db="streaming")


#########

cursor = db.cursor()
query = 'SELECT text FROM streaming.tweets_' + keyword + ' LIMIT 0,' + str(limit_tweets_to_analyse);
try:
    cursor.execute(query)
    results = cursor.fetchall()
except Exception as e:
    print 'error', e
##########
def combinliste(seq, k):
    p = []
    i, imax = 0, 2**len(seq)-1
    while i<=imax:
        s = []
        j, jmax = 0, len(seq)-1
        while j<=jmax:
            if (i>>j)&1==1:
                s.append(seq[j])
            j += 1
        if len(s)==k:
            p.append(s)
        i += 1 
    return p
#########
tweets_treated = 0

g = Graph()


for row in results:
    list_hashtag = []
    row = str(row[0])
    for word in row.split():
        token = word.lower()
        if token.startswith('#'):
            # : if graph contains. Augmenter le poids. fontweight
            if g.add_node(token, radius= 3, fill=(0,0,0,0.4)) is not None:
                g.add_node(token).radius += 0.003
                g.add_node(token).text.fontsize += 0.03
            if token not in list_hashtag:
                list_hashtag.append(token)
    combinaison = combinliste(list_hashtag,2)
    for paire in combinaison:
        #si le poids existe alors on augmente le poids (voir la valeur de retour de add_edge.)
        if g.add_edge(paire[0], paire[1], strokewidth=0.1, stroke=(0,0,0,0.4), weight=0.0, type='is-related-to') is not None:
            g.add_edge(paire[0], paire[1]).strokewidth +=0.06
            listStroke = list(g.add_edge(paire[0], paire[1]).stroke)
            listStroke[3]+=0.1
            g.add_edge(paire[0], paire[1]).stroke = tuple(listStroke)
    tweets_treated +=1
    print tweets_treated


#elagage
#

#g = g.split()[0]

#print 'NUMBER OF NODES ' + str(len(g.nodes))


#node_removed=0

#for node in g.nodes:
 #   if node.weight <= 0.07:
 #       print node_removed
 #       node_removed+=1
 #       g.remove(node)
  #      g = g.split()[0]
  #      g.eigenvector_centrality()

#print '\nNUMBER OF NODES ' + str(len(g.nodes))

#for graph i g.split():
#    graph.export('hashtags' + str(i),title='Hashtags Network',width=800, height=600, directed=False,repulsion=60)
#    i+=1
# 
#
#on a que le sous graphe

#g.split()[0].export('hashtags' ,title='Hashtags Network',width=900, height=550, directed=False,k=7,repulsion=60)

#g.export('hashtags' ,title='Hashtags Network',width=900, height=550, directed=False,k=7,repulsion=60)

g.export('sound', directed=True)
#g.serialize()

print '\n\ngraph exported'