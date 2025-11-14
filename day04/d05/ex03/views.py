from django.shortcuts import render

def table_view(request):
    shades = []

    for i in range(1, 51):
        v = int(i * (255 / 50))
        shades.append({"black": f"rgb({v},{v},{v})",
                       "red": f"rgb({v},0,0)",
                       "green": f"rgb(0,{v},0)",
                       "blue": f"rgb(0,0,{v})"}) 
    
    return (render(request, "ex03/table.html", {"shades": shades}))