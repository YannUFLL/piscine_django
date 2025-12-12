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

def main():
    nb_args = len(sys.argv)
    if nb_args != 2: 
        sys.exit(0)
    arg = sys.argv[1]
    states, capital_cities = return_dic()
    state = states.get(arg)
    if state is None:
        print("Unknown state")
    else:
        print(capital_cities[state])

if __name__ == "__main__":
    main()