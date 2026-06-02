
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Certificate, Profile
from .utils import calculate_points, verify_name

@login_required
def student_dashboard(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        level = request.POST.get('level')
        file = request.FILES.get('file')
        
        points = calculate_points(category, level)
        
        cert = Certificate(
            student=request.user,
            category=category,
            level=level,
            file=file,
            points_awarded=points
        )
        cert.save()
        return redirect('student_dashboard')

    certs = Certificate.objects.filter(student=request.user)
    total_points = sum(c.points_awarded for c in certs if c.status == 'Approved')
    return render(request, 'student_dash.html', {'certs': certs, 'total': total_points})

@login_required
def teacher_dashboard(request):
    if not request.user.profile.is_teacher:
        return redirect('student_dashboard')
    
    # Filter logic
    batch = request.GET.get('batch')
    certs = Certificate.objects.all()
    if batch:
        certs = certs.filter(student__profile__batch=batch)
        
    return render(request, 'teacher_dash.html', {'certs': certs})

def approve_cert(request, cert_id):
    cert = Certificate.objects.get(id=cert_id)
    cert.status = 'Approved'
    cert.save()
    return redirect('teacher_dashboard')