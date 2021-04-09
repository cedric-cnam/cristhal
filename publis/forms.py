
from django.forms import ModelForm
from django import forms
from django.forms.widgets import *
from .models import Publication, ClassementPubli, Collection
from django.db.transaction import commit

from .constants import CODE_CONFIG_DEFAUT

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit,Fieldset, MultiField, Row, Column, Div


class ClassementPubliForm(ModelForm):
    '''
      Formulaire permettant de classer une publi
    '''
    
    def __init__(self, *args, **kwargs):
        super(ClassementPubliForm, self).__init__(*args, **kwargs)
        self.fields['titre'].required = False
        self.fields['type'].required = False
        self.fields['annee'].required = False
        # self.fields['auteurs'].required = False
        self.fields['conf_titre'].required = False
        self.fields['revue_titre'].required = False

    class Meta:
        model = Publication
        fields = ['titre','annee', 'type', 'conf_titre', 'revue_titre', 'classement', 'classement_valide']
        
    def save(self,commit=True):
        '''
           On surcharge la méthode save() pour ne conserve
        '''
        form_data = super(ClassementPubliForm, self).save(commit=False)
        publi = Publication.objects.get(idHal=form_data.idHal)
        publi.classement = form_data.classement
        publi.classement_valide = form_data.classement_valide
        publi.save()
        

    
class PubliSearchForm(forms.Form):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.action = 'publis:publications'
        
        self.fields['collection'] = forms.ModelChoiceField(queryset=Collection.objects.all(),initial=0,required=False,empty_label="Toutes")
        self.fields['classement'] = forms.ModelChoiceField(queryset=ClassementPubli.objects.all(),empty_label="Tous")
        self.fields['classement'].required = False
        self.fields['auteur'] = forms.CharField(label="Nom d'auteur (ou laisser blanc)", required=False)
        #elf.fields['auteur'].required = False         
        self.fields['annee_min'] = forms.IntegerField(label='Année min.') 
        self.fields['annee_max'] = forms.IntegerField(label='Année min.') 

        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
         Div(
                Column('collection', css_class='form-group col-md-4 mb-0'),
                Column('auteur', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
          Div(
                Column('classement', css_class='form-group col-md-4 mb-0'),                
                Column('annee_min', css_class='form-group col-md-4 mb-0'),
                Column('annee_max', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Exécuter la recherche')
        )

