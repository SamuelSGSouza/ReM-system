from django import forms
from . import models 
from django.core.exceptions import ValidationError
from validate_docbr import CPF

import re

class ClienteForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Cliente 
        fields = "__all__" 
    
    def clean_nome(self): 
        nome = self.cleaned_data['nome'] 
        if len(nome) < 5:
            raise ValidationError('Este campo precisa ter mais que 5 caracteres')
        else:
            return nome 
    
    def clean_contato_1(self): 
        contato = self.cleaned_data['contato_1'] 
        if len(contato) < 16:
            raise ValidationError('Este campo precisa ser preenchido corretamente')
        else:
            contato = re.sub('[^0-9]', '', contato)
            return contato

    def clean_contato_2(self): 
        contato = str(self.cleaned_data['contato_2'])
        if len(contato) > 0:
            contato = re.sub('[^0-9]', '', contato)
        return contato

    def clean_contato_3(self): 
        contato = str(self.cleaned_data['contato_3']) 
        if len(contato) > 0:
            contato = re.sub('[^0-9]', '', contato)
        return contato
    
    def clean_documento(self): 
        documento = self.cleaned_data['documento'] 
        if len(documento) < 11:
            raise ValidationError('Este campo precisa ser preenchido corretamente')
        else:
            cpf = CPF()
            documento = str(documento)
            if cpf.validate(documento):
                documento = re.sub('[^0-9]', '', documento)
                documento = str(documento)
                return documento
            else:
                raise ValidationError('Insira um CPF válido')
    
    def clean_uf(self): 
        uf = str(self.cleaned_data['uf']).upper()
        return uf