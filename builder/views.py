from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import CV, CoverLetter
from .services import generate_cover_letter
from .forms import CVForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def index(request):
    letter = None
    cvs = CV.objects.filter(user=request.user)

    if request.method == "POST":
        cv_id = request.POST.get("cv_id")
        job_description = request.POST.get("job_description")

        # Security: ensure user owns the CV
        selected_cv = CV.objects.get(id=cv_id, user=request.user)

        # Include education in the AI prompt
        cv_text = (
            f"Education: {selected_cv.education}\n"
            f"Skills: {selected_cv.skills}\n"
            f"Experience: {selected_cv.experience}"
        )

        letter = generate_cover_letter(cv_text, job_description)

        # CRITERION 1.2: Save the result to the CoverLetter model
        CoverLetter.objects.create(
            user=request.user,
            cv=selected_cv,
            job_title="Generated Application",
            company_name="Various",
            generated_content=letter
        )

    return render(
        request,
        "builder/index.html",
        {
            "cvs": cvs,
            "letter": letter
        }
    )


@login_required
def cv_create(request):
    if request.method == "POST":
        form = CVForm(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            # Crucial: Link the CV to the logged-in user
            cv.user = request.user
            cv.save()
            return redirect('index')
    else:
        form = CVForm()

    return render(request, 'builder/cv_form.html', {'form': form})


@login_required
def dashboard(request):
    # This grabs your CVs
    user_cvs = CV.objects.filter(user=request.user)

    # This grabs your Letters (latest ones first)
    user_letters = (
        CoverLetter.objects
        .filter(user=request.user)
        .order_by('-created_at')
    )

    return render(request, 'builder/dashboard.html', {
        'cvs': user_cvs,
        'letters': user_letters
    })


@login_required
def cv_update(request, pk):
    # Security: Only let the owner edit this CV
    cv = get_object_or_404(CV, pk=pk, user=request.user)

    if request.method == "POST":
        # 'instance=cv' fills the form with existing data
        form = CVForm(request.POST, instance=cv)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CVForm(instance=cv)

    return render(
        request,
        'builder/cv_form.html',
        {'form': form, 'edit_mode': True}
    )


@login_required
def cv_delete(request, pk):
    cv = get_object_or_404(CV, pk=pk, user=request.user)
    if request.method == "POST":
        cv.delete()
        return redirect('dashboard')
    return render(request, 'builder/cv_confirm_delete.html', {'cv': cv})
