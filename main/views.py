from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .filters import PatientFilter
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.views import View
from io import BytesIO
from django.template.loader import get_template

# Create your vie

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            return render(request, 'main/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')


def dashboard(request):
    patients = Patient.objects.all()
    patient_count = patients.count()
    patients_recovered = Patient.objects.filter(status="Recovered")
    patients_deceased = Patient.objects.filter(status="Deceased")
    deceased_count = patients_deceased.count()
    recovered_count = patients_recovered.count()
    beds = Bed.objects.all()
    beds_available = Bed.objects.filter(occupied=False).count()
    context = {
        'patient_count': patient_count,
        'recovered_count': recovered_count,
        'beds_available': beds_available,
        'deceased_count':deceased_count,
        'beds':beds
    }
    print(patient_count)
    return render(request, 'main/dashboard.html', context)

def add_patient(request):
    beds = Bed.objects.filter(occupied=False)
    doctors = Doctor.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        phone_num = request.POST['phone_num']
        patient_relative_name = request.POST['patient_relative_name']
        patient_relative_contact = request.POST['patient_relative_contact']
        address = request.POST['address']
        symptoms = request.POST['symptoms']
        prior_ailments = request.POST['prior_ailments']
        bed_num_sent = request.POST['bed_num']
        bed_num = Bed.objects.get(bed_number=bed_num_sent)
        dob = request.POST['dob']
        status = request.POST['status']
        doctor = request.POST['doctor']
        doctor = Doctor.objects.get(name=doctor)
        print(request.POST)
        patient = Patient.objects.create(
            name = name,
        phone_num = phone_num,
        patient_relative_name = patient_relative_name,
        patient_relative_contact = patient_relative_contact, 
        address = address, 
        symptoms = symptoms, 
        prior_ailments = prior_ailments, 
        bed_num = bed_num,
        dob = dob, 
        doctor=doctor,
        status = status
        )
        patient.save()

        bed = Bed.objects.get(bed_number=bed_num_sent)
        bed.occupied = True
        bed.save()
        id = patient.id
        return redirect("patient_list")
        
    context = {
        'beds': beds,
        'doctors': doctors
    }
    return render(request, 'main/add_patient.html', context)

def add_patient_report(request):
    if request.method == "POST":
        phone = request.POST['phone']

        test1 = request.POST['test1']
        desc1 = request.POST['desc1']

        test2 = request.POST['test2']
        desc2 = request.POST['desc2']
        
        test3 = request.POST['test3']
        desc3 = request.POST['desc3']
        
        test4 = request.POST['test4']
        desc4 = request.POST['desc4']
        
        test5 = request.POST['test5']
        desc5 = request.POST['desc5']
        
        test6 = request.POST['test6']
        desc6 = request.POST['desc6']
        
        test7 = request.POST['test7']
        desc7 = request.POST['desc7']
        
        test8 = request.POST['test8']
        desc8 = request.POST['desc8']
        
        test9 = request.POST['test9']
        desc9 = request.POST['desc9']
        
        test10 = request.POST['test10']
        desc10 = request.POST['desc10']
        
        try:
            patient = Patient.objects.get(phone_num=phone)
        except:
            messages.add_message(request, messages.WARNING, "Patient dosen't exist.")
            return redirect('add_patient_report')

        t_d = Report.objects.create(patient_id=patient.id,desc1=desc1, desc2=desc2, desc3=desc3, desc5=desc5, desc4=desc4, desc6=desc6, desc7=desc7, desc8=desc8, desc9=desc9, desc10=desc10,
                test1=test1, test2=test2, test3=test3, test4=test4, test5=test5, test6=test6, test7=test7, test8=test8, test9=test9, test10=test10)
        t_d.save()

        return redirect('patient_list')
    else:
        return render(request, 'main/add_patient_report.html')

def patient(request, pk):
    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        doctor = request.POST['doctor']
        doctor_time = request.POST['doctor_time']
        doctor_notes = request.POST['doctor_notes']
        mobile = request.POST['mobile']
        mobile2 = request.POST['mobile2']
        relativeName = request.POST['relativeName']
        address  = request.POST['location']
        print(doctor_time)
        print(doctor_notes)
        status = request.POST['status']
        doctor = Doctor.objects.get(name=doctor)
        print(doctor)
        patient.phone_num = mobile
        patient.patient_relative_contact = mobile2
        patient.patient_relative_name = relativeName
        patient.address = address
        patient.doctor = doctor
        patient.doctors_visiting_time = doctor_time
        patient.doctors_notes = doctor_notes
        print(patient.doctors_visiting_time)
        print(patient.doctors_notes)
        patient.status = status
        patient.save()
    context = {
        'patient': patient
    }
    return render(request, 'main/patient.html', context)

def patient_report(request, id):
    patient = Patient.objects.get(id=id)
    # print(patient.id)
    reports = Report.objects.filter(patient_id=id)

    print(reports)
    return render(request, 'main/patient_report.html',{
        "reports":reports,
        "patient":patient,
    })  

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class view_report(View):    
    def get(self, request, rid, *args, **kwargs):
        context = {'report':Report.objects.get(id=rid)}
        Report.objects.filter(id=rid).update(seen=True)
        pdf = render_to_pdf('main/report_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

def DownloadReportasPDF(request, rid):
    report = Report.objects.get(id=rid)
    patient = Patient.objects.get(id=report.patient_id)
    context = {
        'report':report,
        'patient':patient,
    }
    pdf = render_to_pdf('main/report_pdf.html', context)
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Lab_Test_Report_%s.pdf"
    content = "attachment; filename=%s" %(filename)
    response['Content-Disposition'] = content
    return response

def patient_list(request):
    patients = Patient.objects.all()

    # filtering
    myFilter = PatientFilter(request.GET, queryset=patients)

    patients = myFilter.qs
    context = {
        'patients': patients,
        'myFilter': myFilter
    }

    return render(request, 'main/patient_list.html', context)

'''
def autocomplete(request):
    if patient in request.GET:
        name = Patient.objects.filter(name__icontains=request.GET.get(patient))
        name = ['js', 'python']
        
        names = list()
        names.append('Shyren')
        print(names)
        for patient_name in name:
            names.append(patient_name.name)
        return JsonResponse(names, safe=False)
    return render (request, 'main/patient_list.html')
'''

def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Patient.objects.filter(name__icontains=query_original)
    mylist = []
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)

def autodoctor(request):
    query_original = request.GET.get('term')
    queryset = Doctor.objects.filter(name__icontains=query_original)
    mylist = []
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)

def info(request):
    return render(request, "main/info.html")