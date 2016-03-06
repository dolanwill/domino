import domino_full

print "Hello!"
print "Available team attributes: [1. random] [2. greedy] [3. defensive]\n"
team1_attr = input("Select team 1's attribute: ")
team2_attr = input("Select team 2's attribute: ")
set_length = input("Please enter the number of sets you wish to be played\n")

i = 0
results = []
win_counts = [0,0]
while(i != set_length):
	series = domino_full.Series(attrs = [team1_attr, team2_attr])
	scores = series.run_games()
	results.append(scores)
	if(scores[0] > scores[1]):
		win_counts[0] +=1
	else:
		win_counts[1] +=1
	i += 1

print results
print win_counts

