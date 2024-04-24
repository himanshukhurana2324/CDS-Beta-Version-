import json
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import cds6 as cds 
from django.http import JsonResponse
from home.models import Symptoms
from user.models import signup
import google.generativeai as genai 
from dotenv import load_dotenv
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import os
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
@login_required
def home(request):
    return render(request,"index.html")
    # return HttpResponse('Hello, World!')

@login_required
def dashboard(request):
    current_user = signup.objects.get(email=request.user.email)
    try:
        symptoms = Symptoms.objects.get(patient=current_user)
        print("Symptoms found:", symptoms)

        # Get the cdsAnalysis data
        cds_analysis_data = symptoms.cdsAnalysis
        print("CDS Analysis data:", cds_analysis_data)

        # Create two lists: one for dates and one for cdsAnalysis values
        dates = [item['timestamp'] for item in cds_analysis_data]
        cds_analysis_values = [item['value'] for item in cds_analysis_data]
        print("Dates and values:", dates, cds_analysis_values)
    
    except ObjectDoesNotExist :
        print("No symptoms found for user")
        # If the user has not been tested, set dates and cds_analysis_values to empty lists
        dates = []
        cds_analysis_values = []
    data = {
        'dates': json.dumps(dates),
        'cds_analysis_values': json.dumps(cds_analysis_values),
        'userName': current_user.username,
    }
    print(data)

    # Pass the data to the template
    return render(request, "overviewContainer.html", data)

def output(request):
    ap = float(request.POST.get("ap"))
    an = float(request.POST.get("an"))
    di = float(request.POST.get("di"))
    vo = float(request.POST.get("vo"))
    we = float(request.POST.get("we"))
    bmi = float(request.POST.get("bmi"))
    
    cds.Abdominal_Pain_var = ap
    cds.Anemia_var = an
    cds.Diarrhea_var = di
    cds.Vomiting_var = vo
    cds.Weight_Loss_var = we
    cds.Bmi_var = bmi
    
    res = round(float(cds.Calculate()))
     # Get the user who is currently logged in
    current_user = signup.objects.get(email=request.user.email)

    # Get the existing Symptoms instance for the current user, or create a new one if it doesn't exist
    symptoms, created = Symptoms.objects.get_or_create(patient=current_user)

    # Append the new values to the existing values in the JSON fields
    symptoms.abdPain.append({"value": ap, "timestamp": timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
    symptoms.anemmia.append({"value": an, "timestamp": timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
    symptoms.diarhea.append({"value": di, "timestamp": timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
    symptoms.vomit.append({"value": vo, "timestamp": timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
    symptoms.bmi.append({"value": bmi, "timestamp": timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
    symptoms.cdsAnalysis.append({"value": res, "timestamp": timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
    symptoms.weightLoss.append({"value": we, "timestamp": timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
    # Save the Symptoms instance back to the database
    symptoms.save()
    
    # return render(request,'result.html',{'res':res})
    print(res)
    return JsonResponse({'result': res})
def bot(message):
    load_dotenv()
    API_KEY = os.getenv('GEMINI_API_KEY')

    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    instruction = " In this chat, kindly respond solely as Mr. Health Advisor, addressing queries regarding health, diseases, symptoms, and related terms. Apologies in advance for any non-related queries other than greetings . Remember to Give answers of not more than 50 words at a time "
    question = message
    response = chat.send_message(instruction + question) 
    Text = f"{response.text}"
    return Text


def run_script(request):
    user_message = request.GET.get('userMessage', '')
    response = bot(user_message)
    return JsonResponse({'response': response})
    


def overview(request):
    current_user = signup.objects.get(email=request.user.email)
    try:
        symptoms = Symptoms.objects.get(patient=current_user)
        print("Symptoms found:", symptoms)

        # Get the cdsAnalysis data
        cds_analysis_data = symptoms.cdsAnalysis
        print("CDS Analysis data:", cds_analysis_data)

        # Create two lists: one for dates and one for cdsAnalysis values
        dates = [item['timestamp'] for item in cds_analysis_data]
        cds_analysis_values = [item['value'] for item in cds_analysis_data]
        print("Dates and values:", dates, cds_analysis_values)
    
    except ObjectDoesNotExist :
        print("No symptoms found for user")
        # If the user has not been tested, set dates and cds_analysis_values to empty lists
        dates = []
        cds_analysis_values = []
    data = {
        'dates': json.dumps(dates),
        'cds_analysis_values': json.dumps(cds_analysis_values),
        'userName': current_user.username,
    }
    print(data)

    # Pass the data to the template
    return render(request, "overviewContainer.html", data)
    

def product(request): 
    return render(request,"productContainer.html")

def settings(request):

    current_user = signup.objects.get(email=request.user.email)
    # values = Symptoms.objects.get(patient=current_user)
    details = {"userName": current_user.username, "userEmail": current_user.email,"userGender": current_user.gender,
               "userBG": current_user.bloodGroup, "userState": current_user.state, "userAge": current_user.age}
    return render(request,"settingsContainer.html", details)        
    # print(current_user.username, current_user.email)

def faq(request):
    return render(request,"faqContainer.html")

def profileUpdate(request):

    if request.method == 'POST':
        profileGender = request.POST.get('profileGender', None)
        profileBG = request.POST.get('profileBG', None)
        profileState = request.POST.get('profileState', None)
        profileName = request.POST.get('profileName', None)
        profileAge = request.POST.get('profileAge', None)
        # Get the user's profile
        current_user = signup.objects.get(email=request.user.email)
      

        # Update the fields with the new values
        if profileName is not None and profileName != '' and re.match(r'^[a-zA-Z\s]+$', profileName):
            current_user.username = profileName

        if profileAge is not None and profileAge != '' and re.match(r'^\d+$', profileAge )and (int(profileAge) > 0) and (int(profileAge) < 90):
            current_user.age = profileAge

        if profileGender is not None and profileGender != '' and re.match(r'^(Male|Female|Other)$', profileGender, re.I):
            current_user.gender = profileGender

        if profileBG is not None and profileBG != '' and re.match(r'^(A|B|AB|O)[+-]$', profileBG):
            current_user.bloodGroup = profileBG

        if profileState is not None and profileState != '' and re.match(r'^[a-zA-Z\s]+$', profileState):
            current_user.state = profileState
            
        

        # Save the updated profile
        current_user.save()

       

        return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('login')
