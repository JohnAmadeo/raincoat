import easygui
from easygui import *

def getPriceForGenre(genre):
    return len(genre)*10

def getGenres():
    return ["Romance", "Tragedy", "Comedy"]

def getDirectors(remBudget):
    return ["Wes Anderson", "Spike Lee", "Tommy Wiseau"]

def getActors(remBudget):
    return ["Millie Bobbie Brown", "Elizabeth Taylor", "Cary Grant"]

def getPersonPrice(id):
    return 10

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

msg="Pick a genre:"
title="Movie Game"
genres=getGenres()
genreChoice=choicebox(msg, title, genres) #genre selection

budget=getPriceForGenre(genreChoice)
spent=0
msg=("Your budget is now $"+str(budget)+".\n"+
    remainingMoney(spent, budget))
msgbox(msg, ok_button="OK")

repeatDirector=True
while (repeatDirector==True):
    msg="Pick a director (these are all directors you can afford):"
    directors=getDirectors(budget)
    directorChoice=choicebox(msg, title, directors) #director selection
    price=getPersonPrice(directorChoice)
    msg=("This director costs $"+str(price)+".\n"+
    "You will have $"+str(budget-price-spent)+" remaining.\n"+
    remainingMoney(spent+price, budget)+"\n"+
    "Are you sure you want to hire this director?")
    repeatDirector= not ccbox(msg, "Confirm Director")
    if(not repeatDirector):
        spent=spent+price

count=1
actorSel=[""]*5
for x in range (0, 3):
    repeatActor=True
    while (repeatActor==True):
        msg="Pick your actor #"+str(count)+" (these are all the ones you can afford):"
        actors=getActors(budget-spent)
        actorChoice=choicebox(msg, title, actors) #director selection
        price=getPersonPrice(actorChoice)
        msg=("This actor costs $"+str(price)+".\n"+
        "You will have $"+str(budget-price-spent)+" remaining.\n"+
        remainingMoney(spent+price, budget)+"\n"+
        "Are you sure you want to hire this actor?")
        repeatActor= not ccbox(msg, "Confirm Actor")
        if(not repeatActor):
            spent=spent+price
            actorSel[count]=actorChoice
    count=count+1

#Results
textbox("Your movie:\n Genre: "+genreChoice+"\n"
+"Director: "+directorChoice+"\n"
+"Actor 1: "+actorSel[1]+"\n"
+"Actor 2: "+actorSel[2]+"\n"
+"Actor 3: "+actorSel[3]+"\n"
+"Total cost: "+str(spent))
