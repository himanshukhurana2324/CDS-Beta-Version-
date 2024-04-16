from django.shortcuts import render
from django.http import HttpResponse
from . import cds6 as cds 

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

