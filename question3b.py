import rdflib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def write_list_to_file(l, desc):
    result = open('question3c.txt', 'a+')
    result.write(desc)
    for item in l:
        result.write(str(item) + '\n')

# find all players who were born in Spain and play in the Premier League
q1 = "SELECT * WHERE { ?p <http://example.org/birthPlace> ?city . ?city <http://example.org/located_in> <http://example.org/Spain> . ?p <http://example.org/playsFor> ?team  }"
# Find all the players who were born after 1990
q2 = " SELECT * WHERE {?p <http://example.org/playsFor> ?team . ?p <http://example.org/birthDate> ?date . FILTER regex(str(?date), '199') } LIMIT 10"
# Find all players who play in the same city they were born in
q3 = " SELECT ?p WHERE { ?p <http://example.org/birthPlace> ?city . ?p <http://example.org/playsFor> ?team . ?team <http://example.org/homeCity> ?city}"
# Find all possible derby matches
q4 = " SELECT ?team1 ?team2 WHERE { ?team1 <http://example.org/homeCity> ?city . ?team2 <http://example.org/homeCity> ?city FILTER (?team1 != ?team2) }"

g1 = rdflib.Graph()
g1.parse("players.nt", format="nt")
x1 = g1.query(q1)
x2 = g1.query(q2)
x3 = g1.query(q3)
x4 = g1.query(q4)
desc = '************ QUERY 1: players who were born in Spain and play in the Premier League ************\n'
write_list_to_file(list(x1), desc)
desc = '************ QUERY 2: players who were born after 1990 (LIMIT 10) ************\n'
write_list_to_file(list(x2), desc)
desc = '************ QUERY 3: players who play in the same city they were born in ************\n'
write_list_to_file(list(x3), desc)
desc = '************ QUERY 4: all possible derby matches ************\n'
write_list_to_file(list(x4), desc)
