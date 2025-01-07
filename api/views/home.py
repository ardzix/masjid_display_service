from django.shortcuts import render

def homepage(request):
    """
    Renders the homepage with a modern design.
    """
    return render(request, 'homepage.html', {})