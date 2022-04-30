"""

 This file contains the bfs implementation for a tournament creation.
 It uses the queue implemented in 'util.py'.
 Note: Throughout the project the same structure for tournament representation is used.
 A tournament is a list containing rounds (lists of maximum size 3). Each round contains
 matches (lists of exactly size 2). Each match has in the first index the team playing at home
 and in second index, the team playing against it.
"""

import random
import copy
import time
from util import Queue
from constraints import *

participatingTeams = 6
totalRounds = 5

# Creating statement tournament
def createFixedMatches():
    country = ["FR","IT","SC","IR","WA","EN"]
    matches=[]
    for i in country:
        home = i
        for j in country:
            if j!=i:
                away = j
                match = [home,away]
                matches.append(match)
    return matches

# Creating the list of possible matches based on any number of teams
def createMatches(teamNumber):
    matches = []
    for i in range(0, teamNumber):
        for j in range(0, teamNumber):
            # A team can't play against itself
            if j != i:
                matches.append([i, j])
    return matches

# Creating the mirror of a tournament as defined in the statement
def createMirror(tournament):
    # Creating a deepcopy or the current tournament to avoid modifying it
    mirrored = copy.deepcopy(tournament)
    for r in tournament:
        # Creating a new mirror round of the current one
        round = []
        for m in r:
            round.append([m[1], m[0]])
        # Adding the new mirrored round at the end of the tournament
        mirrored.append(round)
    return mirrored


def bfs(matches):
    # Keeping track of the number of nodes explored for later analysis
    nodesExplored = 0

    tournament = []
    frontier = Queue()

    # Creating possible tournaments based on all matches
    for m in matches:
        frontier.push([[m]])

    while True:
        # No more nodes to explore
        if frontier.isEmpty():
            print("--- Nodes explored: %s ---" % nodesExplored)
            return []  # failure

        # Getting a tournament to explore from the frontier
        tournament = frontier.pop()

        # New node exploring
        nodesExplored += 1

        # If the tournament creation is complete (5 rounds of 3 matches each)
        # and it satisfies the conditions on the final round, return solution
        if isGoal(tournament, totalRounds):
            print("--- Nodes explored: %s ---" % nodesExplored)
            return createMirror(tournament)

        # Setting a maximum length for a tournament, no exploring is done if the tournament is complete        
        if len(tournament) < totalRounds or (len(tournament) == totalRounds and len(tournament[totalRounds-1]) < 3):
            # Looping through all the matches
            for m in matches:
                newMatch = True
                # Checking if the current match or its mirror is already in the tournament to avoid duplicate matches
                for r in tournament:
                    if m in r or [m[1], m[0]] in r:
                        newMatch = False

                # If it is a new match, expand its possiblities
                        # Setting a maximum length for a tournament, no exploring is done if the tournament is complete        
        if len(tournament) < totalRounds or (len(tournament) == totalRounds and len(tournament[totalRounds-1]) < 3):
            # Looping through all the matches
            for m in matches:
                newMatch = True
                # Checking if the current match or its mirror is already in the tournament to avoid duplicate matches
                for r in tournament:
                    if m in r or [m[1], m[0]] in r:
                        newMatch = False

                # If it is a new match and the action is valid, expand its possiblities
                if newMatch and validAction(tournament, m):
                    # Adding new round to the tournament
                    if len(tournament[len(tournament)-1]) == 3:
                        newTournament = copy.deepcopy(tournament)
                        newTournament.append([m])
                        frontier.push(newTournament)
                    # Adding neww match to the last round in the tournament
                    else:
                        newTournament = copy.deepcopy(tournament)
                        newTournament[len(tournament)-1].append(m)
                        frontier.push(newTournament)


if __name__ == "__main__":
    # starting timer to compute execution time
    start_time = time.time()
    # Creating match
    matches = createMatches(6)

    print("--- BFS algorithm ---")
    # Fetching tournament
    '''tournament = bfs(matches)
    # Total exuction time
    print("--- Time: %s seconds ---" % (time.time() - start_time))
    # Solution if any
    print("--- Tournament solution ---")
    print(tournament)'''
    exectime = []
    for i in range (0,5):
        random.shuffle(matches)
        start_time = time.time()
        bfs(matches)
        exectime.append(time.time() - start_time)
    print(sum(exectime)/len(exectime))
    