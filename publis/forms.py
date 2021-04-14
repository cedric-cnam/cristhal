
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
        publi = Publication.objects.get(id_hal=form_data.id_hal)
        publi.classement = form_data.classement
        publi.classement_valide = form_data.classement_valide
        publi.save()
        

    
class PubliSearchForm(forms.Form):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.action = 'publis:publications'
        
        choix_coll = [("toutes", "Toutes")]
        for coll in Collection.objects.all():
            choix_coll.append ((coll.code, coll.nom))
        choix_class = [("tous", "Tous")]
        for classement in ClassementPubli.objects.all():
            choix_class.append ((classement.code, classement.libelle))
        self.fields['collection'] = forms.ChoiceField(choices=choix_coll)
        self.fields['classement'] = forms.ChoiceField(choices=choix_class)
        self.fields['auteur'] = forms.CharField(label="Nom d'auteur (ou laisser blanc)", required=False)
        self.fields['annee_min'] = forms.IntegerField(label='Année min') 
        self.fields['annee_max'] = forms.IntegerField(label='Année max') 

        self.helper.layout = Layout(
         Row(
                Column('collection', css_class='form-group col-md-6 mb-0'),
                Column('auteur', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
          Row(
                Column('classement', css_class='form-group col-md-4'),                
                Column('annee_min', css_class='form-group col-md-3'),
                Column('annee_max', css_class='form-group col-md-3'),
                css_class='form-row'
            ),
            Submit('submit', 'Exécuter la recherche')
        )

