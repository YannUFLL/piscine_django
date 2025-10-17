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

def conditional_print_capital(word, states, capital_cites):
    state = states.get(word)
    if state is not None:
        print(f"{word} is the state of {capital_cities[state]}")
        return (True)
    return (False)


def conditional_print_state(word, states, capital_cites):
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


if __name__ == "__main__":
    nb_args = len(sys.argv)
    if nb_args != 2: 
        sys.exit(0)
    arg = sys.argv[1]
    states, capital_cities = return_dic()
    tempword = None
    for word in arg.replace(",", " ").split():
        cword = word.capitalize()
        if cword == "New":
            tempword = "New"
            continue
        if tempword == "New" and cword == "Jersey":
            cword = "New Jersey"
            tempword = None
        if (not conditional_print_capital(cword, states, capital_cities) and
        not conditional_print_state(cword, states, capital_cities)): 
            print(f"{cword} is neither the capital city nor a state")
         


    
        
