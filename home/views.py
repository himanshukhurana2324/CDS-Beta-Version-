from django.shortcuts import render
from django.http import HttpResponse
from . import cds6 as cds 
from django.http import JsonResponse

import google.generativeai as genai 
from dotenv import load_dotenv
import os

# Create your views here.
def home(request):
    return render(request,"index.html")
    # return HttpResponse('Hello, World!')

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
    
    
    # # return render(request,'result.html')
    
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
    response = bot(user_message) ;
    return JsonResponse({'response': response})


def login(request):
    return render(request,"login.html")
