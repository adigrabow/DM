import requests
import lxml.html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

wiki_prefix = "http://en.wikipedia.org"
bad_cities = []

def get_all_teams_in_league(leagues_url):
    print '*********** ALL TEAMS IN THE PREMIER LEAGUE ***********'
    res = requests.get(leagues_url)
    doc = lxml.html.fromstring(res.content)
    teams_table = doc.xpath("//table[contains(@class, 'wikitable sortable')][1]/tr")
    write_to_file('2016%E2%80%9317_Premier_League', '<http://example.org/country>', 'England')

    for index in range(1,21):
        team = teams_table[index].xpath("td[1]/a/@href")[0]
        location = teams_table[index].xpath("td[2]/a/@href")

        # if location is not a link we need to extract the text
        if len(location) == 0:
            location = teams_table[index].xpath("td[2]/text()")[0]
        else:
            location = location[0]

        write_to_file(team, '<http://example.org/league>', leagues_url)
        write_to_file(team, '<http://example.org/homeCity>', location)

        print team + " " + location
        get_all_players_in_team(wiki_prefix + team)


def get_all_players_in_team(teams_url):
    print '*********** ALL PLAYERS IN ' + teams_url + '***********'
    number_of_players = 0
    res = requests.get(teams_url)
    doc = lxml.html.fromstring(res.content)
    players_tables = doc.xpath("//table[contains(. , 'Player')][1]/tr[contains(@class, 'vcard agent')]/td/span[contains(@class, 'fn')]/a/@href")
    print 'number of players ' + str(len(players_tables))
    for player in players_tables:
        if number_of_players > 30:
            break
        number_of_players += 1
        print player
        get_player_info(wiki_prefix + player)


def get_player_info(url):
    print '*********** PLAYER INFO: + ' + url + ' ***********'
    try:
        res = requests.get(url)
    except:
        return
    doc = lxml.html.fromstring(res.content)
    try:
        # get to the infobox
        a = doc.xpath("//table[contains(@class, 'infobox')]")
        if len(a) > 0:
            # extract name from the info box.
            name = a[0].xpath("//caption//text()")[0].replace(" ", "_")
            # extract DoB
            b = a[0].xpath("//table//th[contains(text(), 'Date of birth')]")
            if len(b) > 0:
                dob = b[0].xpath("./../td//span[@class='bday']//text()")[0].replace(" ", "_")
            # extract pob
            # c = a[0].xpath("//table//th[contains(text(), 'Place of birth')]")
            # pob_1 = c[0].xpath("./../td//a/text()")
            # if len(pob_1) < 1:
            #     pob = c[0].xpath("./../td/text()")[0].replace(" ", "_")
            # else:
            #     pob = c[0].xpath("./../td//a/text()")[0].replace(" ", "_")
            pob = a[0].xpath("//table/tr[th[contains(text(), 'Place of birth')]]/td/a/@href")[0]
            print ('pob = ' + pob)
            getCountry(wiki_prefix + pob)
            # extract position
            position = None
            d = a[0].xpath("//table//th[contains(text(), 'Playing position')]")
            if len(d) > 0:
                pos = d[0].xpath("./../td//a/text()")
                if len(pos) > 0:
                    position = pos[0].replace(" ", "_")
            # extract current team
            current_team = None
            e = a[0].xpath("//tr[th/div/text()='Current team']")
            if len(e) > 0:
                # current_team = e[0].xpath("td/a/text()")
                current_team = e[0].xpath("td/a/@href")
                if len(current_team) == 0:
                    current_team = e[0].xpath("td/text()")[0]
                else:
                    current_team = current_team[0]
            # instead of creating a graph and using the "add" function, we can just use write function
            name = name.replace(" ", "_")
            if (current_team is not None) and (position is not None):
                write_to_file(name, '<http://example.org/birthPlace>', pob)
                write_to_file(name, '<http://example.org/position>', position)
                write_to_file(name, '<http://example.org/birthDate>', dob)
                write_to_file(name, '<http://example.org/playsFor>', current_team)
                print (name + " " + dob + " " + pob + " " + position)
    except Exception:
        print 'Exception :('


def getCountry(city):
    res = requests.get(city)
    doc = lxml.html.fromstring(res.content)
    country = doc.xpath("//table[contains(@class, 'infobox')]/tr/th/a[contains(text(), 'Country')]/../../td/a/text()")
    if len(country) == 0:
        country = doc.xpath("//*[contains(text(),'Country')]/../td/a/text()")
        if len(country) == 0:
            country = doc.xpath("//table[contains(@class,'infobox')]/tr[th/span/a[contains(text(), 'country')]]/td/a/text()")
            if len(country) == 0:
                country = doc.xpath("//table[contains(@class,'infobox')]/tr[th/a[contains(text(), 'Country')]]/td/span/a/text()")
                if len(country) == 0:
                    country = doc.xpath("//table[contains(@class,'infobox')]/tr[th/a[contains(text(), 'country')]]/td/text()")
                    if len(country) == 0:
                        country = doc.xpath("//table[contains(@class,'infobox')]/tr[th/a[contains(text(), 'Country')]]/td/text()")
                        if len(country) == 0:
                            country = doc.xpath("//table[contains(@class,'infobox')]/tr[th[contains(text(), 'Country')]]/td/span/a/text()")
                            if len(country) == 0:
                                country = doc.xpath("//table[contains(@class,'infobox')]/tr[th/span/a[contains(text(), 'country')]]/td/text()")
                                if len(country) == 0:
                                    country = doc.xpath("//table[contains(@class,'infobox')]/tr[th/a[contains(text(),'country')]]/td/a/text()")
                                    if len(country) == 0:
                                        country = doc.xpath("//table[contains(@class,'infobox')]/tr[th/a[contains(text(), 'State')]]/td/a/text()")
                                        if len(country) == 0:
                                            country = doc.xpath("//table[contains(@class, 'infobox')]/tr[th[contains(text(), 'Country')]]/td/text()")
                                            if len(country) == 0:
                                                country = doc.xpath("//table[contains(@class, 'infobox')]/tr[th[contains(text(), 'Country')]]/td/span/text()")
                                                if len(country) == 0:
                                                    country = doc.xpath("//table[contains(@class, 'infobox')]/tr[th[contains(text(), 'country')]]/td/a/text()")


    # Add country to ontology
    if len(country) > 0:
        write_to_file(city, '<http://example.org/located_in>', country[0])
    else:
        print '! ! ! ! ! ! ! ERROR IN EXTRACTIN COUNTRY FOR ' + city
        bad_cities.append(city)
        return
    print country


def write_to_file(e1, relation, e2):
    if (e1 is None) or (e2 is None) or (e2 == '\n'):
        return
    f = open('players.nt', 'a+')
    e1 = e1.split('/')[-1]
    e1 = e1.replace(' ', '_')
    e2 = e2.split('/')[-1]
    e2 = e2.replace(' ', '_')
    f.write("<http://example.org/" + e1 + "> " + relation + " <http://example.org/" + e2 + "> . \n")
    f.close()

get_all_teams_in_league(wiki_prefix + '/wiki/2016%E2%80%9317_Premier_League')
print 'bad cities = ' + str(len(bad_cities))
