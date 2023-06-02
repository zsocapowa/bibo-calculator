from django import forms

CHOICES_BOOL = ((True, 'Igen'), (False, 'Nem'))
CHOICES_BA_MA = ((True, 'Alapszakos'), (False, 'Mesterszakos'))


class ContactForm(forms.Form):
    last_name = forms.CharField(required=False, label="Vezetéknév",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, label="Keresztnév",
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    mail = forms.CharField(required=False, label="E-mail cím", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True, label="Üzenet")

    def create_mail(self):
        self.clean()
        msg = self.cleaned_data.get("message")
        last_name = self.cleaned_data.get("last_name")
        first_name = self.cleaned_data.get("first_name")
        mail = self.cleaned_data.get("mail", "Ismeretlen")
        cleaned_names = list(filter(None, (last_name, first_name)))
        name = ' '.join(cleaned_names) if cleaned_names else "Ismeretlen"
        mail = f'Feladó: {name}\nCím: {mail}\nÜzenet: {msg}'
        return mail


class CalcForm1(forms.Form):
    initial_penalty = forms.IntegerField(required=True, label="Büntetőpontok száma az adott félév elején?",
                                         widget=forms.NumberInput(
                                             attrs={
                                                 'id': "penalty_point",
                                                 'value': "0",
                                                 'name': "initial_penalty",
                                                 'step': "1",
                                                 'min': "-10",
                                                 'max': "3",
                                                 'class': 'form-control rounded-4'
                                             }
                                         )
                                         )
    mean = forms.FloatField(required=True, label="Tanulmányi átlag értéke?", widget=forms.NumberInput(attrs={
        'id': "mean_score",
        'step': "0.01",
        'min': "1.00",
        'max': "5.00",
        'value': "4.00",
        'name': "mean",
        'class': 'form-control rounded-4'
    }))
    ba_ma = forms.ChoiceField(required=True, choices=CHOICES_BA_MA,
                              widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                              label="Alap, vagy mesterszakos hallgató vagy?")


class CalcForm2(forms.Form):
    lecture = forms.IntegerField(label="Kurzus",
                                 widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                 'value': "0",
                                                                 'min': "0",
                                                                 'max': "5",
                                                                 'step': "1"}))
    research_group = forms.IntegerField(label="Kutatócsoport",
                                        widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                        'value': "0",
                                                                        'min': "0",
                                                                        'max': "3",
                                                                        'step': "1"}))
    research_paper = forms.IntegerField(label="Tutori dolgozat",
                                         widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                         'value': "0",
                                                                         'min': "0",
                                                                         'max': "3",
                                                                         'step': "1"}))
    other_pillars = forms.MultipleChoiceField(
        label="Milyen további pilléreket teljesítettél?",
        required=False,
        choices=(("internship", "Szakmai gyakorlat"),
                 ("secretary", "Műhelytitkári poszt betöltése")),
        widget=forms.CheckboxSelectMultiple(attrs={'class': "form-check-input"}))
    previous_internship = forms.ChoiceField(required=True, choices=CHOICES_BOOL,
                                            widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                                            label="Tanulmányaid alatt teljesítettél szakmai gyakorlatot?")


class CalcForm3(forms.Form):
    previous_paper = forms.ChoiceField(required=True, choices=CHOICES_BOOL,
                                       widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                                       label="Az aktuális képzésen korábban írtál tutori dolgozatot?")
    tdk = forms.ChoiceField(required=True, choices=CHOICES_BOOL, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input'}),
                            label="Kari TDK konferencián bekerült-e az első négy közé nem szak/évfolyam dolgozattal?")
    last_semester = forms.ChoiceField(required=True, choices=CHOICES_BOOL,
                                      widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                                      label="Utolsó féléved-e az adott képzésen?")
    on_time = forms.ChoiceField(required=True, choices=CHOICES_BOOL,
                                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                                label="Tanulmányait időben befejezi-e?")


class CalcForm4(forms.Form):
    passive_limit = forms.ChoiceField(required=True, choices=CHOICES_BOOL,
                                      widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                                      label="Egyetemi hallgatói jogviszonyát maximum kétszer szüneteltette?")
    package = forms.ChoiceField(required=True, choices=CHOICES_BOOL,
                                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                                label="Időben benyújtottad a szakmai pakkot az adott félévben?")
    assembly = forms.ChoiceField(required=True, choices=CHOICES_BOOL,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                                 label="Részt vettél a műhelyülésen az adott félévben, vagy igazolta-e a hiányzását?")
    prof_day = forms.ChoiceField(required=True, choices=CHOICES_BOOL,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                                 label="Részt vett-e a szakmai napokon hallgatóságként az adott félévben vagy igazolta-e hiányzását?")
