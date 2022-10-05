import pandas as pd
from formularios.models import Cliente
import datetime

def gera_csv(queryset, path):
    #pegando values do queryset
    queryset = queryset.values()
    #padronizando qs da receita federal
    i=0
    f = 10000
    val=queryset[i:f]
    df = pd.DataFrame(val)
    comprimento_df = len(df.index)
    print(f'fiz o df {comprimento_df}')
    le = queryset.count()
    while comprimento_df < le:
        i+= 10000
        f+= 10000
        val = queryset[i:f]
        df_atual = pd.DataFrame(val)
        comprimento_df += len(df_atual.index)
        df = pd.concat([df, df_atual], axis=0)
        print(f'Ciclo {i//10000}')
    
    df.to_csv(path, sep='\t', encoding='utf-8')
    # gera um csv a partir do dataframe
    pass

def filtra_qs(model, filtros: dict):
    qs = model.objects.filter()
    if filtros != {}:
        #filtrando vendedor
        vendedor = filtros['vendedor']
        if vendedor != "":
            qs = qs.filter(vendedor__icontains=vendedor)

        #filtrando nome cliente
        cliente = filtros["nome_cliente"]
        if cliente != "":
            qs = qs.filter(nome__icontains=cliente)

        #filtrando documento
        documento = filtros["documento"]
        if documento != "":
            qs = qs.filter(documento__icontains=documento)

        #filtrando cep
        cep = filtros["cep"]
        if cep != "":
            qs = qs.filter(cep__icontains=cep)

        #filtrando data
        data = filtros["single-date-pick"]
        hoje = datetime.date.today().strftime("%Y-%m-%d")
        if hoje != data[0]:
            print("Filtrando data")
            data_inicio = datetime.datetime.strptime(data[0], "%Y-%m-%d")
            data_final = datetime.datetime.strptime(data[1], "%Y-%m-%d")
            qs = qs.filter(created__range=[data_inicio, data_final])
        
        #filtrando as tags
        try:
            tags = filtros['tags']
        except:
            tags = ""
        
        if tags != "":
            qs = qs.filter(tags__id__in=tags)
    

    return qs