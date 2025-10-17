def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            elements = file.readlines()
            return (elements)
    except FileNotFoundError:
        raise 

def parse_elements(elements):
    l_elements = []
    for element in elements:
        name, data = element.split("=", 1)
        pairs = [item.strip() for item in data.split(",")]
        dic = {}
        for p in pairs:
            key, value = p.split(":", 1)
            dic[key.strip()] = value.strip()
        dic["name"] = name
        l_elements.append(dic)
    return (l_elements)

def create_html_header():
    h = """<!DOCTYPE html5>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Periodic table</title>
<body>


        """
    return (h)


if __name__ == "__main__":
    elements = read_file("periodic_table.txt")
    dic = parse_elements(elements)
    print(dic)
    print(create_html_header())
