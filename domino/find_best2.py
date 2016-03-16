# score - [0, 0, 532, 0, 543, 545]
import domino

print "[1. random] [2. greedy] [3. defensive] [4. antigreedy]"
print "[5. cooperative] [6. offensive]"

behaviors = [3, 5, 6]
behavior_wins = [0,0,0,0,0,0]
length = 10

for p0 in behaviors:
	for p1 in behaviors:
		for p2 in behaviors:
			for p3 in behaviors:
				w_c = domino.run([p0, p1, p2, p3], length)
				if w_c[0] >= 7 or w_c[1] >=7:
						print "Team 1: {0}, {1}. Team 2: {2}, {3}".format(p0, p2, p1, p3)
						print w_c
				behavior_wins[p0-1] += w_c[0]
				behavior_wins[p1-1] += w_c[1]
				behavior_wins[p2-1] += w_c[0]
				behavior_wins[p3-1] += w_c[1]


print "Total Behavior Wins:"
print behavior_wins