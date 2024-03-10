from django.shortcuts import render


def other_page(request):
    received_data = request.GET.get('data')  # Get data from query parameter
    return render(request, 'other_page.html', {'data': received_data})
