
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, render_to_response
from django.core.mail import send_mail
from . import forms

from .forms import ContactForm

from formtools.wizard.views import SessionWizardView
from collections import ChainMap

from .business_logic import StudyOutcome


# TODO: https://stackoverflow.com/questions/33052063/django-csrf-verifcation-failed-class-based-views
class CalcWizard(SessionWizardView):
    template_name = "calc/calc_form_v1.html"

    def done(self, form_list, **kwargs):
        form_data = process_form_data(form_list)

        return render_to_response('calc/calc_result.html', {'form_data': form_data})


def process_form_data(form_list):
    final_input_dict = {}
    form_data = [form.cleaned_data for form in form_list]
    input_for_calc = dict(ChainMap(*form_data))
    for item, value in input_for_calc.items():
        if value == 'True':
            final_input_dict[item] = True
        elif value == 'False':
            final_input_dict[item] = False
        else:
            final_input_dict[item] = value
    outcome_object = StudyOutcome(**final_input_dict)
    outcome_result = outcome_object.calculate_overall_performance()
    return outcome_result


def index(request):
    return render(request, 'calc/index.html')


def pmtsz(request):
    return render(request, 'calc/pmtsz_display.html')


def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            try:
                # after 2022.05.30. it isn't going to work:
                # https://support.google.com/accounts/answer/6010255?hl=hu
                mail_body = form.create_mail()
                send_mail("CALC_FORM_CONTACT", mail_body, None, ['zsoca.powa@gmail.com'])
            except Exception as e:
                print(e)
            finally:
                return render(request, 'calc/thanks_for_contact.html')
                # TODO: save it to the db, with 'is_sent': True or False
    contact_form = ContactForm()
    return render(request, 'calc/contact_form.html', {'form': contact_form})

