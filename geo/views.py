from django.shortcuts import render

def location(request):
    """
    Render the location page.
    """
    return render(request, 'Gis/map.html')