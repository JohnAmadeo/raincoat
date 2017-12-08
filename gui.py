import easygui
from easygui import *
import urlparse
import psycopg2

db_url = "postgres://flnagkaphunlzd:58d06cddda4a7bb84af165d0e61a1268fa8d6bdb13fc401f0d999487203a504e@ec2-174-129-227-116.compute-1.amazonaws.com:5432/dddk3nffa4e1qb"
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(db_url)

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()

def getPriceForGenre(genre):
    cur.execute("SELECT make_budget (%s);", (genre,))
    return cur.fetchone()[0]

#returns a list containing all possible genres
def getGenres():
    cur.execute("SELECT list_genres ();")
    return [i[0] for i in cur.fetchall()]

#returns a list of all possible directors given the budget remBudget
def getDirectors(remBudget):
    cur.execute("SELECT remaining_directors (%s);", (remBudget,))
    return [i[0] for i in cur.fetchall()]

#returns a list of all possible actors given the budget remBudget
def getActors(remBudget):
    if remBudget<=0:
        return []
    cur.execute("SELECT remaining_actors (%s);", (remBudget,))
    return [i[0] for i in cur.fetchall()]

#returns a list of all tuples (id, movie) for each person of the given name
#given the budget remBudget
def getPersonID(name, remBudget, isDirector):
    if isDirector == 1:
        cur.execute("SELECT match_name_director (%s, %s);", (remBudget, name))
    else:
        cur.execute("SELECT match_name_actor (%s, %s);", (remBudget, name))
    p = [i[0][1:-2].split(",\"") for i in cur.fetchall()]
    for i in p:
        i[0] = int(i[0])
    return p

#given an id, return that person's cost
def getPersonPrice(idNum, isDirector):
    cur.execute("SELECT cost_of_hire (%s, %s);", (idNum, isDirector))
    return cur.fetchone()[0]

#Generates a bar showing how much money remains
def remainingMoney(spent, budget):
    barlen=30
    returnString="$0 ["
    spentX=int(spent/float(budget)*barlen)
    leftX=barlen-spentX
    for x in range (0, spentX):
        returnString=returnString+unichr(0x2588)
    for x in range (0, leftX):
        returnString=returnString+"  "
    returnString=returnString+"] $"+str(budget)
    return returnString

#returns the metascore constribution of the person with the given id
#dir=0 means actor, and 1=director
#if the SQL function return is empty, return this function should return 0
def ratingM(id, isDirector):
    if id == 0:
        return 0
    cur.execute("SELECT rating_generated_m (%s, %s);", (id, isDirector))
    return cur.fetchone()[0]

#returns the IMDB constribution of the person with the given id
#dir=0 means actor, and 1=director
#if the SQL function return is empty, return this function should return 0
def ratingI(id, isDirector):
    if id == 0:
        return 0
    cur.execute("SELECT rating_generated_i (%s, %s);", (id, isDirector))
    return cur.fetchone()[0]

#returns the revenue contribution of the person with the given id
#dir=0 means actor, and 1=director
#if the SQL function return is empty, return this function should return 0
def revenue(id, isDirector):
    #print id
    if id == 0:
        return 0
    cur.execute("SELECT revenue (%s, %s);", (id, isDirector))
    return cur.fetchone()[0]


#Welcome Message, game explanation
msg=("Welcome, producer! The glorious world of film awaits you. "
+"In this game, you will create a movie. You will pick the genre, "
+"the director and three actors to star in your film. Make sure you"
" stay in your budget!\n"+
"At the end of the game, we will tell you how successful your film is.\n"+
"Let's begin." )
msgbox(msg)
repeat=True
while(repeat==True):
    spent=0
    pickedIDs=[0]*5
    actorSel=[" "]*4
    imdbRating=0
    metaRating=0
    made=0
    msg="Pick a genre:"
    title="Movie Game"
    genres=getGenres()
    genreChoice=None
    while(genreChoice==None):
        genreChoice=choicebox(msg, title, genres) #genre selection

    budget=getPriceForGenre(genreChoice)
    msg=("Your hiring budget is now $"+str(budget)+".\n"+
        remainingMoney(spent, budget))
    msgbox(msg)

    #Director
    repeatDirector=True
    while (repeatDirector==True):
        msg=("Pick a director (these are all directors you can afford):\n\n"+
        "Type a letter to skip to that portion of the list.")
        directors=getDirectors(budget-spent)
        directorChoice=None
        while(directorChoice is None):
            directorChoice=choicebox(msg, title, directors) #director selection
        idList=getPersonID(directorChoice, budget-spent, 1)
        if (len(idList)>1):
            movies=[tuple[1] for tuple in idList]
            msg=("There are multiple directors named "+directorChoice+
            ".\n Please select the movie that your chosen director has directed.")
            pickedMovie=choicebox(msg, "Clarify director",movies)
            idNum=next(x for x in idList if x[1] == pickedMovie)[0]
        else:
            idNum=idList[0][0]
        pickedIDs[0]=idNum #add directorID
        price=getPersonPrice(idNum, 1)
        msg=("This director costs $"+str(price)+".\n"+
        "You will have $"+str(budget-price-spent)+" remaining.\n"+
        remainingMoney(spent+price, budget)+"\n"+
        "Are you sure you want to hire this director?")
        repeatDirector= not ynbox(msg, "Confirm Director")
        if(not repeatDirector):
            spent=spent+price

    count=1
    for x in range (0, 3):
        repeatActor=True
        while (repeatActor==True):
            msg=("Pick your actor #"+str(count)+" (these are all the ones you can afford):\n\n"+
            "Type a letter to skip to that portion of the list.")
            actors=getActors(budget-spent)
            if(len(actors)==0):
                msg=("You have spent all of your money! You can't afford to hire an actor #"
                +str(count)+". Your rating will suffer because of your financial mismanagement.")
                msgbox(msg, ok_button="I accept my fate")
                break
            actorChoice=None
            while(actorChoice is None):
                actorChoice=choicebox(msg, title, actors) #director selection
            idList=getPersonID(actorChoice, budget-spent, 0)
            if (len(idList)>1):
                movies=[tuple[1] for tuple in idList]
                msg=("There are multiple actors named "+actorChoice+
                ".\n Please select the movie that your chosen actor was in.")
                pickedMovie=choicebox(msg, "Clarify Actor",movies)
                idNum=next(x for x in idList if x[1] == pickedMovie)[0]
            elif (len(idList)==1):
                idNum=idList[0][0]
            pickedIDs[count]=idNum #add actorID
            price=getPersonPrice(idNum, 0)
            msg=("This actor costs $"+str(price)+".\n"+
            "You will have $"+str(budget-price-spent)+" remaining.\n"+
            remainingMoney(spent+price, budget)+"\n"+
            "Are you sure you want to hire this actor?")
            repeatActor= not ynbox(msg, "Confirm Actor")
            if(not repeatActor):
                spent=spent+price
                actorSel[count]=actorChoice
        count=count+1
    #Results
    imdbRating=ratingI(pickedIDs[0], 1)+ratingI(pickedIDs[1], 0)+ratingI(pickedIDs[2], 0)+ratingI(pickedIDs[3], 0)
    metaRating=ratingM(pickedIDs[0], 1)+ratingM(pickedIDs[1], 0)+ratingM(pickedIDs[2], 0)+ratingM(pickedIDs[3], 0)
    made=revenue(pickedIDs[0], 1)+revenue(pickedIDs[1], 0)+revenue(pickedIDs[2], 0)+revenue(pickedIDs[3], 0)
    msgbox("Your movie:\nGenre: "+genreChoice+"\n"
    +"Director: "+directorChoice+"\n"
    +"Actor 1: "+actorSel[1]+"\n"
    +"Actor 2: "+actorSel[2]+"\n"
    +"Actor 3: "+actorSel[3]+"\n"
    +"Total cost: "+str(spent)+"\n\n"
    +"IMDB Rating: "+str(round(imdbRating,1))+"\n"
    +"MetaCritic Rating: "+str(metaRating)+"\n"
    +"Revenue: $"+str(made)+"\n"
    +"Profit: $"+str(made-spent)+"\n", ok_button="Done")

    repeat=ynbox("Thank you for playing! Would you like to play again?")

msgbox("Enjoy your retirement, producer!", ok_button="Thank you, I shall.")
