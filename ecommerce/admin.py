import csv
from datetime import timezone
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import *
from django.urls.resolvers import URLPattern
from .models import *




class csvImporter(forms.Form):
    csv_upload = forms.FileField()

class CatagoryAdmin(admin.ModelAdmin) :
    list_display = ('name','image','description','status','created_at')
    def active(self, obj): 
        status = obj.status
        return status == 1 
    
  
    active.boolean = True
  
    def make_active(modeladmin, request, queryset): 
        queryset.update(status = 1) 
        messages.success(request, "Selected Record(s) Marked as Active Successfully !!") 
  
    def make_inactive(modeladmin, request, queryset): 
        queryset.update(status = 0) 
        messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!") 
        
    def get_urls(self)  :
        urls = super().get_urls()
        new_urls = [path('upload_csv/',self.upload_csv),]
        return new_urls + urls
        
    
    def upload_csv(self,request) :
                
     if request.method == 'POST':
            form = csvImporter(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_upload']

                # Decode the CSV file
                decoded_file = csv_file.read().decode('utf-8')
                csv_reader = csv.reader(decoded_file.splitlines(), delimiter=',')

                # Skip header row if necessary
                next(csv_reader, None)

                for row in csv_reader:
                    Catagory.objects.create(
                        name=row[0],
                        image=row[1],
                        description=row[2],
                        status=row[3],
                    )
                    # Add more fields as needed

                Catagory.message_user(request, "CSV data imported successfully.")
                return HttpResponseRedirect(request.get_full_path())

     else:
            form = csvImporter()

        # Render the form to allow users to upload a CSV file
       
     return render(request,'admin/ecommerce/csv_upload.html',{'forms':form})
    

class ProductAdmin(admin.ModelAdmin) :
    list_display = ['catagory','name','vendor',
                    'image','quantity','original_price',
                    'selling_price','description',
                    'status','trending','created_at']
    

    
        
    
    
    


admin.site.add_action(CatagoryAdmin.make_active, "Make Active") 
admin.site.add_action(CatagoryAdmin.make_inactive, "Make Inactive") 
admin.site.register(Catagory,CatagoryAdmin)
admin.site.register(Product,ProductAdmin)

# Register your models here.
