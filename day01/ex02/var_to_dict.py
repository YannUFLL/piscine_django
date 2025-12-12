def create_tuples_data():
    d = [
    ('Hendrix' , '1942'),
    ('Allman' , '1946'),
    ('King' , '1925'),
    ('Clapton' , '1945'),
    ('Johnson' , '1911'),
    ('Berry' , '1926'),
    ('Vaughan' , '1954'),
    ('Cooder' , '1947'),
    ('Page' , '1944'),
    ('Richards' , '1943'),
    ('Hammett' , '1962'),
    ('Cobain' , '1967'),
    ('Garcia' , '1942'),
    ('Beck' , '1944'),
    ('Santana' , '1947'),
    ('Ramone' , '1948'),
    ('White' , '1975'),
    ('Frusciante', '1970'),
    ('Thompson' , '1949'),
    ('Burton' , '1939')
    ]
    return (d)

def convert_tuples_to_dictionnary(t):
    result = {}

    for name, year in t:
        if year not in result:
            result[year] = []
        result[year].append(name)
    return (result)

def print_dictionnary(d):
    for year in sorted(d.keys()):
        print(year, ":", ' '.join(d[year]))

def main():
    td = create_tuples_data()
    d = convert_tuples_to_dictionnary(td)
    print_dictionnary(d)


if __name__ == "__main__":
    main()
