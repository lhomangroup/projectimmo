from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .forms import *
from .models import File
from django import template
from account.models import *

register = template.Library()


# Create your views here.
@login_required(login_url='login-annonce', redirect_field_name='workflow')
def workflow(request):
    global contentFile
    form = NewFile()
    heure_debut = request.POST.get('heure_debut')
    heure_fin = request.POST.get('heure_fin')
    rue = request.POST.get('rue')
    voie = request.POST.get('voie')
    ville = request.POST.get('ville')
    region = request.POST.get('region')
    zip = request.POST.get('zip')
    pays = request.POST.get('pays')
    # if request.method == 'POST':
    #     form.save()
    if request.method == 'POST':
        form = NewFile(request.POST)
        f_name = request.POST.get('nom')
        s_name = request.POST.get('prenom')
        mail = ''
        redirect_adress = request.POST.get('redirect_adress')
        if redirect_adress == '':
            mail = request.POST.get('email')
        else:
            mail = redirect_adress
        my_file_avis = request.POST.get('document_avis', False)
        my_file_quittance = request.POST.get('document_quittance', False)
        my_file_paye = request.POST.get('document_paye', False)
        if form.is_valid():
            form.heure_debut = heure_debut
            form.heure_fin = heure_fin
            myAdress = AdressWorkflow.objects.create(rue=rue, voie=voie, ville=ville, region=region, zipCode=zip,
                                                     pays=pays)
            myAdress.save()
            lastAdress = AdressWorkflow.objects.latest('id')
            form.save()
            myId = File.objects.latest('id')
            myId.address = lastAdress
            user = Account.objects.get(email=mail)
            myId.user = user
            myId.save()
            myId = myId.id
            data = {
                'id': myId,
                'f_name': f_name,
                's_name': s_name,
                'mail': mail,
                'my_file_avis': my_file_avis,
                'my_file_quittance': my_file_quittance,
                'my_file_paye': my_file_paye,
            }

            message = '''
                New customer: {} {}

                Hello,
                Here the message with a folder of our customer.
                Thank you for taking care of it.
                Click on the link for send your verdict:
                http://127.0.0.1:8000/workflow/workrep/{}
                Have nice day

                His folder: {}, {}, {}

                From: {}
                '''.format(data['f_name'], data['s_name'], data['id'], data['my_file_avis'], data['my_file_quittance'],
                           data['my_file_paye'], data['mail'])
            send_mail(data['f_name'], message, '', [mail])
    context = {'form': form}
    return render(request, 'workflow/workflow.html', context)


@register.simple_tag
def get_verbose_field_name(instance, field):
    """
    Returns verbose_name for a field.
    """
    return instance.get_field_display()


@login_required(login_url='login')
def workrep(request, pk):
    Files = File.objects.get(id=pk)
    form = UpdateFile(request.POST or None, instance=Files)
    if request.method == 'POST':
        form = UpdateFile(request.POST or None, instance=Files)
        mail = ''
        redirect_adress = request.POST.get('redirect_adress')
        if redirect_adress == '':
            mail = request.POST.get('email')
        else:
            mail = redirect_adress
        commentaire_value = request.POST.getlist('commentaire_nek')
        length = len(commentaire_value)
        for i in range(length):
            com = Commentaire_nek.objects.create(commentaire=commentaire_value[i])
            com.save()
            com_save = Commentaire_nek.objects.latest('id')
            Files.commentaire_nek.add(com_save)
            Files.save()
            if form.is_valid():
                form.save()
        verdict = request.POST.get('verdict')
        data1 = {
            'verdict': verdict,
            'id': pk,
        }

        message = '''
            Hello,
            Here the answer about the folder of our customer.
            His verdict : {}
            click the link to see or make comments and to return on site :
            http://127.0.0.1:8000/workflow/final/{}
                Have nice day
            '''.format(data1['verdict'], data1['id'])

        send_mail(data1['verdict'], message, '', [mail])

    context = {'Files': Files, 'form': form}
    return render(request, 'workflow/workrep.html', context)


def workfinal(request, pk):
    Files = File.objects.get(id=pk)
    form = FinalFile(request.POST or None, instance=Files)
    comment = ""
    decision = ""
    if request.method == 'POST':
        form = UpdateFile(request.POST or None, instance=Files)
        mail = ''
        redirect_adress = request.POST.get('redirect_adress')
        if redirect_adress == '':
            mail = request.POST.get('email')
        else:
            mail = redirect_adress
        commentaire_value = request.POST.getlist('commentaire_nek')
        rdv_value = request.POST.get('rdv')
        rdv = request.POST.get('date_rdv')

        if rdv_value == '1':
            Files.date_reunion = rdv
            Files.verdict = 'attn'
            decision = "Prise de rendez vous le :" + Files.date_reunion
            Files.save()
        elif rdv == '0':
            Files.verdict = 'acct'
            decision = "Dossier pris en charge"
            Files.save()

        Files.date_reunion = rdv
        Files.save()
        length = len(commentaire_value)
        for i in range(length):
            com = Commentaire_demeya.objects.create(commentaire=commentaire_value[i])
            com.save()
            com_save = Commentaire_demeya.objects.latest('id')
            Files.commentaire_demaya.add(com_save)
            Files.save()
            comment = comment + '\{}'.format(commentaire_value[i])
            if form.is_valid():
                form.save()

        data2 = {
            'comment': comment,
            'verdict': Files.verdict,
            'decision': decision,
        }

        message = '''

        Hello,
        Here the comment to the folder of our customer : 
        My comment : {}
        Décision : {} 
        {}
        if you want to return on site and see details of the offer :
        http://127.0.0.1:8000/annonce-profil

        Have nice day

        '''.format(data2['comment'], data2['verdict'], data2['decision'])
        send_mail(data2['comment'], message, '', [mail])
    context = {'Files': Files, 'form': form}
    return render(request, 'workflow/final.html', context)