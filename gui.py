import easygui
from easygui import *

def getPriceForGenre(genre):
    return len(genre)*10

#returns a list containing all possible genres
def getGenres():
    return ["Romance", "Tragedy", "Comedy"]

#returns a list of all possible directors given the budget remBudget
def getDirectors(remBudget):
    return ["Wes Anderson", "Spike Lee", "Tommy Wiseau"]

#returns a list of all possible actors given the budget remBudget
def getActors(remBudget):
    if remBudget<=0:
        return []
    elif remBudget<30:
        return ["Millie Bobbie Brown"]
    return ["Millie Bobbie Brown", "Elizabeth Taylor", "Cary Grant"]

#returns a list of all tuples (id, movie) for each person of the given name
#given the budget remBudget
def getPersonID(name, remBudget):
    if(name=="Millie Bobbie Brown"):
        return [(1, "Stranger Things"), (2, "Death")]
    else:
        return [(3, "Goonies")]

#given an id, return that person's cost
def getPersonPrice(idNum):
    if (idNum==1):
        return 10
    if (idNum==2):
        return 20
    if (idNum==3):
        return 30

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
def ratingM(id, dir):
    return 20
    #if the return is empty, return 0

#returns the IMDB constribution of the person with the given id
#dir=0 means actor, and 1=director
#if the SQL function return is empty, return this function should return 0
def ratingI(id, dir):
    return 2
#if the return is empty, return 0

#returns the revenue contribution of the person with the given id
#dir=0 means actor, and 1=director
#if the SQL function return is empty, return this function should return 0
def revenue(id, dir):
    return 200


repeat=True
while(repeat==True):
    msg="Pick a genre:"
    title="Movie Game"
    genres=getGenres()
    genreChoice=None
    while(genreChoice==None):
        genreChoice=choicebox(msg, title, genres) #genre selection

    budget=getPriceForGenre(genreChoice)
    spent=0
    msg=("Your budget is now $"+str(budget)+".\n"+
        remainingMoney(spent, budget))
    msgbox(msg)
    pickedIDs=[0]*5
    #Director
    repeatDirector=True
    while (repeatDirector==True):
        msg="Pick a director (these are all directors you can afford):"
        directors=getDirectors(budget-spent)
        directorChoice=None
        while(directorChoice is None):
            directorChoice=choicebox(msg, title, directors) #director selection
        idList=getPersonID(directorChoice, budget-spent)
        if (len(idList)>1):
            movies=[tuple[1] for tuple in idList]
            msg=("There are multiple directors named "+directorChoice+
            ".\n Please select the movie that your chosen director has directed.")
            pickedMovie=choicebox(msg, "Clarify director",movies)
            idNum=next(x for x in idList if x[1] == pickedMovie)[0]
        else:
            idNum=idList[0][0]
        pickedIDs[0]=idNum #add directorID
        price=getPersonPrice(idNum)
        msg=("This director costs $"+str(price)+".\n"+
        "You will have $"+str(budget-price-spent)+" remaining.\n"+
        remainingMoney(spent+price, budget)+"\n"+
        "Are you sure you want to hire this director?")
        repeatDirector= not ynbox(msg, "Confirm Director")
        if(not repeatDirector):
            spent=spent+price

    count=1
    actorSel=[" "]*4
    for x in range (0, 3):
        repeatActor=True
        while (repeatActor==True):
            msg="Pick your actor #"+str(count)+" (these are all the ones you can afford):"
            actors=getActors(budget-spent)
            if(len(actors)==0):
                msg=("You have spent all of your money! You can't afford to hire an actor #"
                +str(count)+". Your rating will suffer because of your financial mismanagement.")
                msgbox(msg, ok_button="I accept my fate")
                break
            actorChoice=None
            while(actorChoice is None):
                actorChoice=choicebox(msg, title, actors) #director selection
            idList=getPersonID(actorChoice, budget-spent)
            if (len(idList)>1):
                movies=[tuple[1] for tuple in idList]
                msg=("There are multiple actors named "+actorChoice+
                ".\n Please select the movie that your chosen actor was in.")
                pickedMovie=choicebox(msg, "Clarify Actor",movies)
                idNum=next(x for x in idList if x[1] == pickedMovie)[0]
            elif (len(idList)==1):
                idNum=idList[0][0]
            pickedIDs[count]=idNum #add actorID
            price=getPersonPrice(idNum)
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
    revenue=revenue(pickedIDs[0], 1)+revenue(pickedIDs[1], 0)+revenue(pickedIDs[2], 0)+revenue(pickedIDs[3], 0)
    msgbox("Your movie:\n Genre: "+genreChoice+"\n"
    +"Director: "+directorChoice+"\n"
    +"Actor 1: "+actorSel[1]+"\n"
    +"Actor 2: "+actorSel[2]+"\n"
    +"Actor 3: "+actorSel[3]+"\n"
    +"Total cost: "+str(spent)+"\n\n"
    +"IMDB Rating:"+str(imdbRating)+"\n"
    +"MetaCritic Rating:"+str(metaRating)+"\n"
    +"Revenue: $"+str(revenue)+"\n", ok_button="Done")

    repeat=ynbox("Thank you for playing! Would you like to play again?")
