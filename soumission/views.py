from django.http import HttpResponseRedirect
from .forms import *
from django_xhtml2pdf.utils import pdf_decorator
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from soumission.models import checkboxcourses


def savevalues(request):
    if request.method == "POST":
        if request.POST.get('coursename'):
            savedata = checkboxcourses()
            savedata.coursename = request.POST.get('coursename')
            savedata.save
            return render(request, 'indexcheckbox.html')
        else:
            return render(request, 'indexcheckbox.html')


def validate(request, pk):
    # return render(request, 'admin/specialite_compositions.html', context={})
    print('your id: {}'.format(self.pk))


def soumission(request):
    return render(request, 'soumission-submit.html', context={})


class SoumissionCreateView(CreateView):
    # model = ClientCli
    form_class = ClientForm
    # fields = '__all__'
    template_name = "soumission/client_submission.html"


class SoumissionSigner(CreateView):
    # model = SignerCli
    form_class = SignerForm
    # fields = '__all__'
    template_name = "soumission/signer.html"


# Imaginary function to handle an uploaded file.


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})