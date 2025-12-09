# represents an item that has been picked up
class item:
    
    def __init__(self, name = "NONAME", tier = "NOTIER", qty = -1):
        self.name = name
        self.tier = tier
        self.qty = qty

    # prints out item's attributes
    def list(self):
        print(f"ITEM: {self.name} \n     Tier: {self.tier}\n     QTY: {self.qty}")

    def getName(self):
        return self.name
    
    # This is stupid but the project is due in 4 hours so fuck it
    def addQty(self, newQTY):
        qty_int = int(self.qty)
        newQty_int = int(newQTY)
        int_result = qty_int + newQty_int

        self.qty = str(int_result)


    def getQty(self):
        return self.qty
    
    def getTier(self):
        return self.tier

# represents a player character
class player_inv:

    # holds all items a player has picked up according to the log
    items = []

    def __init__(self, name = "NONAME", alliance = "NOALLIANCE", guild = "NOGUILD"):
        self.name = name
        self.alliance = alliance
        self.guild = guild

    def getName(self):
        return self.name
    
    def getAlliance(self):
        if self.alliance != "":
            return self.alliance
        
        else: 
            return "NOALLIANCE"
    
    def getGuild(self):
        if self.guild != "":
            return self.guild
        
        else:
            return "NOGUILD"
    
    def getItems(self):
        return self.items
    
    def add(self, item):
        found = False

        for i in range(len(self.items)):
            if item.getName() == self.items[i].getName():
                self.items[i].addQty(item.getQty())
                found = True

                print(f"incremented QTY of {item.getName()} to {item.getQty()}") # debug

                break
        
        if not found:
            self.items.append(item)

            print (f"added new item {item.getName()}") # debug



#===========================================================*START OF MAIN*===========================================================================
#name of input file; REPLACE WITH SOMETHING GENERIC
inFile = "loot-events-2025-12-04-11-07-27.txt"
players = []
playerNames = []

                        # ***Main loop of reading and processing file***
try:
    with open(inFile, 'r') as file:

        for line in file:

            #print(line) # temporary, this is where line processing goes

            # each element is separated into a list using semicolons as sepatators
            elements = line.split(";")

            # creates item object from elements, (name, tier, quantity)
            currItem = item(elements[5], elements[4], elements[6])
            #currItem.list() # Debug

            # if player (element #3) is in players, add to their inventory. Else, create a new player
            found = False
            for i in range(len(players)):
                currPlayer = players[i]

                # if player already exists
                if elements[3] == players[i].getName():
                    currPlayer.add(currItem)
                    found = True

                    #print(f"adding item {elements[5]} to existing player {elements[3]}") # debug

                    break
            
            if not found:
                # skip first entry, it just gives an example
                if elements[3] == "looted_by__name":
                    pass

                # create a new player_inv (name, alliance, guild)
                else:
                    newPlayer = player_inv(elements[3], elements[1], elements[2])
                    players.append(newPlayer)
                    newPlayer.add(currItem)

                    #print(f"created new player {elements[3]}, added item {elements[5]}") # debug

except FileNotFoundError:
    print(f"Error: The file '{inFile}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")




                                # ***File output***

outFile = "Python_Lootlog.txt"


try:
    with open(outFile, 'w') as file:
        for i in range(len(players)):

            currPlayer = players[i]
            currItems = currPlayer.getItems()

            # Put together header that shows info about player
            line1 = "PLAYER: " + currPlayer.getName() + "    ALLIANCE: " + currPlayer.getAlliance() + "    GUILD: " + currPlayer.getGuild()
            file.write(line1 + '\n')

            for j in range(len(currItems)):

                line2 = "   Item: " + currItems[j].getName() + '\n'
                line3 = "       Tier: " + currItems[j].getTier() + '\n'
                line4 = "       Qty : " + currItems[j].getQty() + '\n'
                file.write(line2 + line3 + line4)

            file.write('\n')

except Exception as e:
    print(f"An error occurred: {e}")