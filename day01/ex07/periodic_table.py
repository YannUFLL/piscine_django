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
    h = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Periodic table</title>
    <style>
        table {
                border-collapse: collapse;
                border: 1px solid black;
        }
        td {

                border: 1px solid black;
                text-align: center;
        }
        ul {
            padding: 0;
        }
        li {
                font-size: 10px; 
                list-style: none;

        }
        h2 {
                font-size: 18px; 
        }
    </style>
</head>
<body>


        """
    return (h)

def create_footer():
    f = """</body></html>"""
    return (f)

def create_table(elements): 
    t = "<table>\n"
    i = 0
    elements.sort(key=lambda e: int(e["number"]))
    for row in range(7):
        t += f" <tr>\n" 
        for col in range(18):
            element = None 
            if int(elements[i]["position"]) == col:
                element = elements[i]
                i += 1
            if (element): 
                t += f"     <td><h4>{element['name']} </h4>\n"
                t += f"        <ul>\n"
                t += f"            <li>{element['small']}</li>\n"
                t += f"            <li>number: {element['number']}</li>\n"
                t += f"            <li>molar: {element['molar']}</li>\n"
                t += f"            <li>electron: {element['electron']}</li>\n"
                t += f"        </ul>\n"
                t += f"     </td>\n"
            else: 
                t += f"     <td> </td>\n"
        t += f" </tr>\n" 
    t+= "</table>\n"
    return (t)

def generate_html(elements):
    html = create_html_header()
    html += create_table(elements)
    html += create_footer()
    return (html)

def main():
    elements = read_file("periodic_table.txt")
    dic = parse_elements(elements)
    html = generate_html(dic)
    with open("periodic_table.html", "w") as file :
        file.write(html)

if __name__ == "__main__":
    main()
 