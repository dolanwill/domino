import domino

print "Hello!"
print "Available team attributes: "
print "[1. random] [2. greedy] [3. defensive] [4. antigreedy]"
print "[5. cooperative] [6. offensive]"
t1_attr = input("Select team 1's behavior: ")
t2_attr = input("Select team 2's behavior: ")
length = input("Enter the number of sets you wish to be played: ")

win_counts = domino.run([t1_attr, t2_attr, t1_attr, t2_attr], length)

print "\nTeam 1 Score, Team 2 Score: {0}".format(win_counts)

