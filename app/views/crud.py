# views.py
import os
from django.shortcuts import render,redirect
import pandas as pd
from app.models import User,Csv  # Import your model if you're fetching data from a database
from django.contrib.auth.decorators import login_required



@login_required(login_url='signin')
def dasboard(request):
    user=request.user
    data=Csv.objects.filter(user=user)
    # Your code to read data here
    return render(request, 'history.html', {'data': data})  # Pass the data to the template


@login_required(login_url='signin')
def show_data(request,id):
    try:
        # Read CSV file using pandas
        obj=Csv.objects.get(id=id)
        df = pd.read_csv(obj.old_csv)
        
        # Check if the DataFrame is empty
        if df.empty:
            return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})

        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient='records')
        # print(789)
        return render(request, "show_data.html", {'data': data,'id':id})
    except Exception as e:
        return render(request, "error.html", {'error_message': str(e)})
        
    # # You need to retrieve the 'data' variable from the request context
    # data = request.context.get('data')
    # return render(request, "show_data.html", {'data': data})

from django.http import Http404


@login_required(login_url='signin')
def delete_file(request, id):
    try:
        obj = Csv.objects.get(id=id)
    except Csv.DoesNotExist:
        raise Http404("Csv matching query does not exist.")
        # Get the file path from the Csv object
    
    file_path = obj.old_csv.path

    # Delete the file from the file system
    if os.path.exists(file_path):
        os.remove(file_path)


    obj.delete()

    return redirect('dasboard')

