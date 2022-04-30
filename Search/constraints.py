"""

 This file contains all the constraints for a tournament.
 During the testing, these were used in different combinations.
"""

import copy

# No team should play twice in one round constraint
def teamsInRound(round):
    # Camparing based on current round length
    if len(round) == 3:
        if round[0][0] in round[1] or round[0][1] in round[1] or round[0][0] in round[2] or round[0][1] in round[2] or round[1][0] in round[2] or round[1][1] in round[2]:
            return False
    if len(round) == 2:
        if round[0][0] in round[1] or round[0][1] in round[1]:
            return False
    return True

# No team should play twice at home in consecutive rounds, or twice away in consecutive rounds
def teamsConsRounds(round1, round2):
    if len(round2) == 3:
        for j in range(0, 3):
            for k in range(0, 3):
                if round1[j][0] == round2[k][0] or round1[j][1] == round2[k][1]:
                    return False
    if len(round2) == 2:
        for j in range(0, 3):
            for k in range(0, 2):
                if round1[j][0] == round2[k][0] or round1[j][1] == round2[k][1]:
                    return False
    if len(round2) == 1:
        for j in range(0, 3):
            if round1[j][0] == round2[0][0] or round1[j][1] == round2[0][1]:
                return False
    return True

# No team plays against ITALY or FRANCE away twice in consecutive rounds
def itFrAway(round1, round2):
    for r in round1:
        j = 0
        while j < len(round2):
            if (r[0] == 'FR' and round2[j][0] == 'IT' and r[1] == round2[j][1]) or (r[0] == 'IT' and round2[j][0] == 'FR' and r[1] == round2[j][1]):
                return False
            j += 1
    return True

# On the last day ENGLAND plays against FRANCE
def enVsFr(tournament):
    if ['FR', 'EN'] in tournament[len(tournament) - 1] or ['EN', 'FR'] in tournament[len(tournament) - 1]:
        return True
    return False

# On the first day IRELAND and ITALY cannot play home
def irVsIt(tournament):
    for i in range(0, 3):
        if tournament[0][i][0] == 'IR' or tournament[0][i][0] == 'IT':
            return False
    return True


def generalConstraints(round1, round2):
    #if teamsInRound(matches) and teamsConsRounds(matches) and itFrAway(matches) and teamsConsRounds(round1, round2): and mirror(matches):# and teamsConsRounds(round1, round2)
    if teamsInRound(round2) and itFrAway(round1, round2):
        return True
    return False


def validAction(tournament, match):
    newTournament = []
    if len(tournament[len(tournament)-1]) == 3:
        newTournament = copy.deepcopy(tournament)
        newTournament.append([match])
    else:
        newTournament = copy.deepcopy(tournament)
        newTournament[len(tournament)-1].append(match)
    
    # If we only have one round, we cannot check constraints between rounds
    if len(newTournament) == 1:
        # Checking if no team plays twice in this round
        if teamsInRound(newTournament[0]):
            # If we reach the end of a round (3 matches), the next match to add is in a new round
            if len(newTournament[len(newTournament)-1]) % 3 == 0:
                return irVsIt(newTournament)
            # Adding match to the current round
            return True
    
    # If the tournament has at least two rounds
    else:
        # Checking if all constraints are respected
        return generalConstraints(newTournament[len(newTournament)-2], newTournament[len(newTournament)-1])

def isGoal(tournament, totalRounds):
    if len(tournament) == totalRounds and len(tournament[totalRounds-1]) == 3 and enVsFr(tournament) and teamsInRound(tournament[totalRounds-1]):
        return True
    return False