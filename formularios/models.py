from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome ou Razão Social")
    documento = models.CharField(max_length=14, verbose_name="CPF ou CNPJ", null=True, blank=True)
    nome_rep = models.CharField(max_length=255, verbose_name="Nome Rep Legal", null=True, blank=True)
    cpf_rep = models.CharField(max_length=11, verbose_name="CPF Rep Legal", null=True, blank=True)
    contato_1 = models.CharField(max_length=255, verbose_name="Contato 1",null=True, blank=True)
    contato_2 = models.CharField(max_length=255, verbose_name="Contato 2",null=True, blank=True)
    contato_3 = models.CharField(max_length=255, verbose_name="Contato 3",null=True, blank=True)
    cep = models.CharField(max_length=8, verbose_name="CEP",null=True, blank=True)
    numero = models.CharField(max_length=5, verbose_name="Número ",null=True, blank=True)
    logradouro = models.CharField(max_length=455, verbose_name="Logradouro",null=True, blank=True)
    complemento = models.CharField(max_length=255, verbose_name="Complemento",null=True, blank=True)
    bairro = models.CharField(max_length=255, verbose_name="Bairro",null=True, blank=True)
    municipio = models.CharField(max_length=255, verbose_name="Município",null=True, blank=True)
    uf = models.CharField(max_length=2, verbose_name="UF",null=True, blank=True)
    ponto_referencia = models.CharField(max_length=255, verbose_name="Ponto De Referência",null=True, blank=True)
    email = models.EmailField(verbose_name="Email",null=True, blank=True)
    tags = models.ManyToManyField("Tags", related_name="clientes")

    def __str__(self) -> str:
        return self.nome

    
classes = (
    ('bg-primary', "Primária"),
    ('bg-secondary', "Secundária"),
    ('bg-success', "Sucesso"),
    ('bg-info', "Informativa"),
    ('bg-warning', "Aviso"),
    ('bg-danger', "Perigo"),
    ('bg-dark', "Fundo Escuro"),
    ('bg-light', "Fundo Claro"),
) 
class Tags(models.Model):
    class Meta:
        verbose_name_plural = "Tag"
    nome = models.CharField(max_length=255, verbose_name="Nome da Tag")
    classe = models.CharField(max_length=255,
    choices=classes,
     verbose_name="Classe da Tag")

    def __str__(self) -> str:
        return self.nome

