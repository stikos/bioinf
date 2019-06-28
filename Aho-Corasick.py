"""
Implementation of the Aho-Corasick algorithm for pattern matching
"""

# FILE INPUT & INITIALIZATIONS #

lines = [line.rstrip('\n') for line in open('patterns.txt')]
pattern_dir = dict()
for pat in lines:
    pattern_dir.update({pat: 0})

abc = ['A', 'T', 'C', 'G']


# GOTO() #

def goTo(lines):
    output = ['' for i in range(20)]
    g = {}
    newstate = 0
    for pattern in lines:
        state = 0
        j = 0
        while (pattern[j], state) in g:
            state = g[(pattern[j], state)]
            j += 1
        for p in range(j, len(pattern)):
            newstate += 1
            g[(pattern[p], state)] = newstate
            state = newstate
        output[state] = pattern
    for char in abc:
        if (char, 0) not in g: g[(char, 0)] = 0
    return g, output


# FAILURE_FUN() #

def failureFun(g, output):
    f = [0 for i in range(20)]
    queue = []
    for key in abc:
        if g[(key, 0)] != 0:
            queue.append(g[(key, 0)])
            f[g[(key, 0)]] = 0
    while queue:
        r = queue.pop(0)
        for key in abc:
            if (key, r) in g:
                queue.append(g[(key, r)])
                state = f[r]
                while (key, state) not in g:
                    state = f[state]
                f[g[(key, r)]] = g[(key, state)]
                if output[f[g[(key, r)]]] != '': output[g[(key, r)]] += (', ' + output[f[g[(key, r)]]])
    return f


# --------------------------------#

# Pattern Matching Machine #

def Automaton(g, f, output):
    text = 'CTAATGTTGAATGGCCACTACCGTGAATGCCGTGTGAATGCTA'
    state = 0
    skip_count = 0
    comp_count = 0
    for i, char in enumerate(text):
        comp_count += 1
        while (char, state) not in g:
            state = int(f[state])
            if not state: skip_count += 1
        state = g[(char, state)]
        if len(output[state]) >= 2:
            print ('In position ' + str(i) + ' found pattern(s) ' + output[state])
            for pat_count in pattern_dir:
                if pat_count in output[state]:
                    pattern_dir[pat_count] += 1
    print ('#Skip/count: ' + str(skip_count))
    print (pattern_dir)
    print ('#Comparisons: ' + str(comp_count))


if __name__ == "__main__":
    g, output = goTo(lines)
    f = failureFun(g, output)
    Automaton(g, f, output)
