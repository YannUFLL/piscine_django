import sys

def return_dic():
    states = {
    "Oregon" : "OR",
    "Alabama" : "AL",
    "New Jersey": "NJ",
    "Colorado" : "CO"
    }
    capital_cities = {
    "OR": "Salem",
    "AL": "Montgomery",
    "NJ": "Trenton",
    "CO": "Denver"
    }

    return (states, capital_cities)

def conditional_print_capital(word, states, capital_cities):
    state = states.get(word)
    if state is not None:
        print(f"{word} is the state of {capital_cities[state]}")
        return (True)
    return (False)


def conditional_print_state(word, states, capital_cities):
    abbreviation = None 
    for abbr, city in capital_cities.items():
        if city == word:
            abbreviation = abbr
            break
    if abbreviation is None:
        return (False)
    else: 
        for state, abbr in states.items():
            if abbr == abbreviation:
                print(f"{word} is the capital of {state}")
                return (True)

def main():
    nb_args = len(sys.argv)
    if nb_args != 2: 
        sys.exit(0)
    arg = sys.argv[1]
    states, capital_cities = return_dic()
    if ",," in arg:
        sys.exit(0)
    for word in arg.split(','):
        split_token = word.strip().split(' ')
        for i in range(len(split_token)):
            split_token[i] = split_token[i].capitalize()
        cword = ' '.join(split_token)
        if (not conditional_print_capital(cword, states, capital_cities) and
        not conditional_print_state(cword, states, capital_cities)): 
            print(f"{word} is neither a capital city nor a state")



if __name__ == "__main__":
    main()

