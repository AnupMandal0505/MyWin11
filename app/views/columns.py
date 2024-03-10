from django.shortcuts import render,redirect
import pandas as pd
import tempfile
from app.models import Csv
import os
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required


@login_required(login_url='signin')
def delete_columns(request, id):
    if request.method == 'POST':
        # Get list of columns to delete from user input
        columns_to_delete = request.POST.getlist('columns_to_delete')

        # Retrieve the Csv object based on the ID
        obj = Csv.objects.get(id=id)
        
        # Read CSV file into a DataFrame
        df = pd.read_csv(obj.old_csv)
        
        # Check if the DataFrame is empty
        if df.empty:
            return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})

        # Drop selected columns
        df.drop(columns=columns_to_delete, inplace=True)

        # Save modified DataFrame to a new CSV file

        new_csv_path = 'Upload/old_csv_file/'
        file_name = str(id)  # Convert id to string and append '.csv' extension
        file_path = os.path.join(new_csv_path, file_name)
        df.to_csv(file_path, index=False)
        print(45455)
        # # Update the 'old_csv' field value with the path of the modified CSV file
        obj.old_csv.name = file_path
        obj.save()

        return redirect('show_data', id=obj)

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

            return render(request, "delete_columns.html", {'data': data, 'id': id})
        except Exception as e:
            return render(request, "error.html", {'error_message': str(e)})

@login_required(login_url='signin')
def rename_columns(request,id):
    
    if request.method == 'POST':
       # Get column names from form input
        new_columns = request.POST.getlist('columns_to_rename')

        # Read CSV file
        obj=Csv.objects.get(id=id)
        df = pd.read_csv(obj.old_csv)
        
        
        old_columns=list(df.columns)

        # Create a dictionary mapping old column names to new column names
        column_mapping = dict(zip(old_columns, new_columns))

        # Rename the columns in the DataFrame
        df.rename(columns=column_mapping, inplace=True)

    
        if df.empty:
            return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})


        if not new_columns:
            return render(request, "error.html", {'error_message': 'No columns selected for renaming.'})
        
        new_csv_path = 'Upload/old_csv_file/'
        file_name = str(id)  # Convert id to string and append '.csv' extension
        file_path = os.path.join(new_csv_path, file_name)
        a=df.to_csv(file_path, index=False)
        # # Update the 'old_csv' field value with the path of the modified CSV file
        obj.old_csv.name = file_path
        obj.save()
        
        return redirect('show_data', id=obj)
    else:
        try:
            # Read CSV file using pandas
            obj=Csv.objects.get(id=id)
            df = pd.read_csv(obj.old_csv)
            # Check if the DataFrame is empty
            if df.empty:
                return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})

            # Convert DataFrame to dictionary
            data = df.to_dict(orient='records')

            return render(request, "columns_rename.html",{'data': data,'id':obj})
        except Exception as e:
            return render(request, "error.html", {'error_message': str(e)})
