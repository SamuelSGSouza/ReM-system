from django import forms
from . import models 
from django.core.exceptions import ValidationError
from validate_docbr import CPF, CNPJ

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
        if len(contato) < 15:
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
        documento = self.cleaned_data['documento'] or ''
        if len(documento) != 0:
            print(type(documento))
            if len(documento) == 18: #CNPJ
                cnpj = CNPJ()
                documento = str(documento)
                if cnpj.validate(documento):
                    documento = re.sub('[^0-9]', '', documento)
                    documento = str(documento)
                    return documento
                else:
                    raise ValidationError('Insira um CNPJ válido')
                
            elif len(documento) == 14: #CPF
                cpf = CPF()
                documento = str(documento)
                if cpf.validate(documento):
                    documento = re.sub('[^0-9]', '', documento)
                    documento = str(documento)
                    return documento
                else:
                    raise ValidationError('Insira um CPF válido')
            else:
                raise ValidationError('Preencha corretamente o documento')

        else:
            return documento

    def clean_cpf_rep(self): 
        documento = self.cleaned_data['cpf_rep'] or ""
        if len(documento) != 0:
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
        else:
            return documento

    def clean_uf(self): 
        uf = self.cleaned_data['uf']
        if type(uf) == str:
            uf = (uf).upper()
        return uf