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

if __name__ == "__main__":
    nb_args = len(sys.argv)
    if nb_args != 2: 
        sys.exit(0)
    arg = sys.argv[1]
    states, capital_cities = return_dic()
    abbreviation = None 
    for abbr, city in capital_cities.items():
        if city == arg:
            abbreviation = abbr
            break
    if abbreviation is None:
        print("Unknown capital city")
    else: 
        for state, abbr in states.items():
            if abbr == abbreviation:
                print(state)
                break

    
        
