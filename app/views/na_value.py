from django.shortcuts import render,redirect
from app.models import Csv
import pandas as pd
import os

def dropna(request,id):
    if request.method == 'POST':
        # Get list of columns to delete from user input
        dropna_by_column = request.POST.getlist('fillna')
        # # Retrieve the Csv object based on the ID
        obj = Csv.objects.get(id=id)
        
        # # Read CSV file into a DataFrame
        df = pd.read_csv(obj.old_csv)
        
        # # Check if the DataFrame is empty
        if df.empty:
            return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})

        # # Drop selected columns
        try:
            df.dropna(subset=dropna_by_column,inplace=True)
        except:
            pass

        if df.empty:
            return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})


        new_csv_path = 'Upload/old_csv_file/'
        file_name = str(id)  # Convert id to string and append '.csv' extension
        file_path = os.path.join(new_csv_path, file_name)
        a=df.to_csv(file_path, index=False)
        # # Update the 'old_csv' field value with the path of the modified CSV file
        obj.old_csv.name = file_path
        obj.save()

        return redirect('show_data', id=id)

    else:
        try:
            # Retrieve the Csv object based on the ID
            obj = Csv.objects.get(id=id)

            # Read CSV file into a DataFrame
            df = pd.read_csv(obj.old_csv)

            # Check if the DataFrame is empty
            if df.empty:
                return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})

            # Convert DataFrame to dictionary
            data = df.to_dict(orient='records')
            # print(data)
            return render(request, "dropna.html",{'data':data,'id':id})
        except Exception as e:
            return render(request, "error.html", {'error_message': str(e)})

    # return render(request, 'fillna.html')


def fillna(request,id):
    obj = Csv.objects.get(id=id)
        
    # # Read CSV file into a DataFrame
    df = pd.read_csv(obj.old_csv)
    
    # # Check if the DataFrame is empty
    if df.empty:
        return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})

    # # Drop selected columns
    df.fillna(4)


    if df.empty:
        return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})


    new_csv_path = 'Upload/old_csv_file/'
    file_name = str(id)  # Convert id to string and append '.csv' extension
    file_path = os.path.join(new_csv_path, file_name)
    a=df.to_csv(file_path, index=False)
    # # Update the 'old_csv' field value with the path of the modified CSV file
    obj.old_csv.name = file_path
    obj.save()

    return redirect('show_data', id=id)
