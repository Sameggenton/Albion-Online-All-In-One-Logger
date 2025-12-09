import time
import psutil

# represents an item that has been picked up
class item:
    
    def __init__(self, name = "NONAME", qty = -1):
        self.name = name
        self.qty = qty

    # prints out item's attributes
    def list(self):
        print(f"ITEM: {self.name} \n     QTY: {self.qty}")

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

# represents a player character
class player_inv:

    # holds all items a player has picked up according to the log

    def __init__(self, name = "NONAME", alliance = "NOALLIANCE", guild = "NOGUILD"):
        self.name = name
        self.alliance = alliance
        self.guild = guild
        self.items = []


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

        # see if player already has an item
        for i in range(len(self.items)):
            if item.getName() == self.items[i].getName():

                # if player already has it, add to QTY running total
                self.items[i].addQty(item.getQty())
                found = True

                #print(f"incremented QTY of {item.getName()} to {item.getQty()}") # debug

                break
        
        # Player does not have item yet, create new entry
        if not found:
            self.items.append(item)

            #print (f"added new item {item.getName()}") # debug



#==========================================================*START OF MAIN*===========================================================================
#name of input file; REPLACE WITH SOMETHING GENERIC IF UR ACTUALLY USING THIS TOOL
inFile = "loot-events-2025-12-04-11-07-27.txt"
players = []
playerNames = []

                        # ***Main loop of reading and processing file***
start_main = time.perf_counter_ns() # all perf_counter uses are for measuring program performance in different aspects
start_read = time.perf_counter_ns()
process = psutil.Process() # Will be used to measure memory usage

try:
    with open(inFile, 'r') as file:

        for line in file:

            #print(line) # debug, prints raw line data

            # each element is separated into a list using semicolons as sepatators
            elements = line.split(";")

            # creates item object from elements, (name, quantity)
            currItem = item(elements[5], elements[6])
            #currItem.list() # Debug, prints item attributes

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

end_read = time.perf_counter_ns()



                                # ***File output***

start_output = time.perf_counter_ns()

#name of output file, can be whatever you want
outFile = "Python_Lootlog.txt"


try:
    with open(outFile, 'w') as file:
        # Open output file, start looping through list of players
        for i in range(len(players)):

            currPlayer = players[i]
            currItems = currPlayer.getItems()

            # Put together header that shows info about player
            line1 = "PLAYER: " + currPlayer.getName() + "    ALLIANCE: " + currPlayer.getAlliance() + "    GUILD: " + currPlayer.getGuild()
            file.write(line1 + '\n')

            # For each player, list all items and their attributes
            for j in range(len(currItems)):

                line2 = "   Item: " + currItems[j].getName() + '\n'
                line4 = "       Qty : " + currItems[j].getQty() + '\n'
                file.write(line2 + line4)

            file.write('\n')

# in case file creation fails for some reason
except Exception as e:
    print(f"An error occurred: {e}")

end_output = time.perf_counter_ns()
end_main = time.perf_counter_ns()

# Printing measurement results to console
mb = 1024 * 1024
main_total = (end_main - start_main) # should be in nanoseconds...
read_total = round((end_read - start_read), 2)
output_total = round((end_output - start_output), 2) 
mem_usage = round(process.memory_info().rss / mb, 2)

print("PROGRAM METRICS:")
print("    Whole program time: " + str(main_total) + " nanoseconds")
print("    File reading and sorting time: " + str(read_total) + " nanoseconds")
print("    File output time: " + str(output_total) + " nanoseconds")
print("    Memory usage: " + str(mem_usage) + " megabytes")