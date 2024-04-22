from django.shortcuts import render
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



# Create your views here.
@login_required
def home(request):
    return render(request,"index.html")
    # return HttpResponse('Hello, World!')

@login_required
def dashboard(request):
    current_user = signup.objects.get(email=request.user.email)
    # values = Symptoms.objects.get(patient=current_user)
    # details = {"username": current_user.username, "email": current_user.email, 
    #            "abdPain": values.abdPain[0], "anemmia": values.anemmia, "diarhea": values.diarhea,
    #            "vomit": values.vomit, "bmi": values.bmi, "cdsAnalysis": values.cdsAnalysis, "weightLoss": values.weightLoss}
    return render(request,"overviewContainer.html") 

def output(request):
    ap = float(request.GET["ap"])
    an = float(request.GET["an"])
    di = float(request.GET["di"])
    vo = float(request.GET["vo"])
    we = float(request.GET["we"])
    bmi = float(request.GET["bmi"])
    
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
    
    return render(request,'result.html',{'res':res})

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
    response = bot(user_message) 
    return JsonResponse({'response': response})


def overview(request):
    return render(request,"overviewContainer.html")

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

