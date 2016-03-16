#results after 5 hours
#Team being tested: 3, 3
#Wins - 2284; Losses - 1316

#Team being tested: 3, 5
#Wins - 2264; Losses - 1336

#Team being tested: 3, 6
#Wins - 2313; Losses - 1287

import domino

print "[1. random] [2. greedy] [3. defensive] [4. antigreedy]"
print "[5. cooperative] [6. offensive]"

behaviors  = [1, 2, 3, 4, 5, 6]
behavior_wins = [0,0,0,0,0,0]
length = 100

def run_simulation(p0, p2):
	total_wins = [0,0]
	for p1 in behaviors:
		for p3 in behaviors:
			w_c = domino.run([p0, p1, p2, p3], length)
			total_wins[0] += w_c[0]
			total_wins[1] += w_c[1]
			behavior_wins[p0-1] += w_c[0]
			behavior_wins[p1-1] += w_c[1]
			behavior_wins[p2-1] += w_c[0]
			behavior_wins[p3-1] += w_c[1]

	print "Team being tested: {0}, {1}".format(p0, p2)
	print "Wins - {0}; Losses - {1}\n".format(total_wins[0], total_wins[1])

run_simulation(3, 3)
run_simulation(3, 5)
run_simulation(3, 6)
run_simulation(5, 5)
run_simulation(5, 6)
run_simulation(6, 6)