#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import sys
from glob import glob
import math
import matplotlib.pyplot as pl

#filecand  = sys.argv[1]
#filevotos = sys.argv[2]

############################
### Definição de funções ###
############################

# Para mudar formatação de data fora do padrão:
MonthDic = {'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', \
            'JUL':'07', 'AUG':'08', 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}
MonthMax = {'01':31,'02':29,'03':31,'04':30,'05':31,'06':30,\
            '07':31,'08':31,'09':30,'10':31,'11':30,'12':31}
def FormatDate(date):
    # Caso campo em branco:
    if type(date)==float and math.isnan(date):
        return ''
    # Caso campo contendo espaços:
    if date.find(' ')!=-1:
       if len(date)==7:
           date = date.replace(' ', '')
           togo = ['0'+date[0:1],'0'+date[1:2],date[2:]]
       else:
           togo = [str(int(date[:2])).zfill(2),str(int(date[2:4])).zfill(2),date[4:]]
    # Caso campo apenas números:
    elif date.isdigit()==True:
        if len(date)==6:
            if date[2:4]=='19':
                togo = ['0'+date[0:1],'0'+date[1:2],date[2:]]
            else:
                togo = [date[:2],date[2:4],'19'+date[4:]]
        elif len(date)==7:
            if date[3:5]=='19':
                if int(date[1:3])>12:
                    togo = [date[:2],'0'+date[2:3],date[3:]]
                else:
                    togo = ['0'+date[:1],date[1:3],date[3:]]
            elif date[4:6]=='19':
                togo = [date[:2],date[2:4],date[4:]+'0']
            else:
                print 'Data ininteligível 1:', date
                return date
        else:
            togo = [date[:2],date[2:4],date[4:]]
        if int(togo[0])>MonthMax[togo[1]]:
            togo[0]=str(int(togo[0])-1)
        if togo[0]=='29' and togo[1]=='02' and (int(togo[2])-1900)%4!=0:
            togo[0]='28'
    # Caso separação por traços:
    elif date.find('-')!=-1:
        togo = date.split('-')
        if togo[1].isdigit()==False:
            togo[1] = MonthDic[togo[1]]
            if len(togo[2])==2:
                togo[2] = '19'+togo[2]
            else:
                print 'Data ininteligível 2:', date
        else:
            print 'Data ininteligível 3:', date
    # Caso separação por barra:
    else:
        togo = date.split('/')
    # Casos de ano apenas com dois dígitos:
    if int(togo[2])<1800 or int(togo[2]>2100):
        return togo[0]+'/'+togo[1]+'/19'+togo[2][2:]
    # Caso ano com 4 dígitos:
    else:
        return '/'.join(togo)
    
# Calcula idade:
def CalculaIdade(DataNasc, AnoEleicao):
    if type(DataNasc)==str:
        print DataNasc
    return (pd.to_datetime('01/10/'+str(AnoEleicao),format="%d/%m/%Y")-DataNasc).days/365
# Corrige idades absurdas:
def ArrumaIdade(Idade, DataNasc,AnoEleicao):
    if Idade < 0 or Idade > 200:
        return CalculaIdade(DataNasc, AnoEleicao)
    else:
        return Idade


####################################
### Definição dos tipos de dados ###
####################################

CandTypes = {'DATA_GERACAO':str,'HORA_GERACAO':str,'ANO_ELEICAO':int,\
            'NUM_TURNO':int,'DESCRICAO_ELEICAO':str,'SIGLA_UF':str,\
            'SIGLA_UE':str,'DESCRICAO_UE':str,'CODIGO_CARGO':int,\
            'DESCRICAO_CARGO':str,'NOME_CANDIDATO':str,'SEQUENCIAL_CANDIDATO':int,\
            'NUMERO_CANDIDATO':str,'CPF_CANDIDATO':str,'NOME_URNA_CANDIDATO':str,\
            'COD_SITUACAO_CANDIDATURA':int,'DES_SITUACAO_CANDIDATURA':str,\
            'NUMERO_PARTIDO':int,'SIGLA_PARTIDO':str,'NOME_PARTIDO':str,\
            'CODIGO_LEGENDA':int,'SIGLA_LEGENDA':str,'COMPOSICAO_LEGENDA':str,\
            'NOME_LEGENDA':str,'CODIGO_OCUPACAO':int,'DESCRICAO_OCUPACAO':str,\
            'DATA_NASCIMENTO':str,'NUM_TITULO_ELEITORAL_CANDIDATO':str,\
            'IDADE_DATA_ELEICAO':int,'CODIGO_SEXO':int,'DESCRICAO_SEXO':str,\
            'COD_GRAU_INSTRUCAO':int,'DESCRICAO_GRAU_INSTRUCAO':str,\
            'CODIGO_ESTADO_CIVIL':int,'DESCRICAO_ESTADO_CIVIL':str,\
            'CODIGO_COR_RACA':int,'DESCRICAO_COR_RACA':str,\
            'CODIGO_NACIONALIDADE':int,'DESCRICAO_NACIONALIDADE':str,\
            'SIGLA_UF_NASCIMENTO':str,'CODIGO_MUNICIPIO_NASCIMENTO':int,\
            'NOME_MUNICIPIO_NASCIMENTO':str,'DESPESA_MAX_CAMPANHA':float,\
            'COD_SIT_TOT_TURNO':str,'DESC_SIT_TOT_TURNO':str,'NM_EMAIL':str}
   
VotoTypes = {'DATA_GERACAO':str,'HORA_GERACAO':str,'ANO_ELEICAO':int,\
            'NUM_TURNO':int,'DESCRICAO_ELEICAO':str,'SIGLA_UF':str,\
            'SIGLA_UE':str,'CODIGO_MUNICIPIO':int,'NOME_MUNICIPIO':str,\
            'NUMERO_ZONA':int,'CODIGO_CARGO':int,'NUMERO_CAND':str,\
            'SQ_CANDIDATO':int,'NOME_CANDIDATO':str,'NOME_URNA_CANDIDATO':str,\
            'DESCRICAO_CARGO':str,'COD_SIT_CAND_SUPERIOR':str,\
            'DESC_SIT_CAND_SUPERIOR':str,'CODIGO_SIT_CANDIDATO':int,\
            'DESC_SIT_CANDIDATO':str,'CODIGO_SIT_CAND_TOT':str,
            'DESC_SIT_CAND_TOT':str,'NUMERO_PARTIDO':int,'SIGLA_PARTIDO':str,\
            'NOME_PARTIDO':str,'SEQUENCIAL_LEGENDA':int,'NOME_COLIGACAO':str,\
            'COMPOSICAO_LEGENDA':str,'TOTAL_VOTOS':int,'TRANSITO':str}

BemTypes  = {'DATA_GERACAO':str,'HORA_GERACAO':str,'ANO_ELEICAO':int,\
            'DESCRICAO_ELEICAO':str,'SIGLA_UF':str,'SQ_CANDIDATO':int,\
            'CD_TIPO_BEM_CANDIDATO':int,'DS_TIPO_BEM_CANDIDATO':str,\
            'DETALHE_BEM':str,'VALOR_BEM':float,'DATA_ULTIMA_ATUALIZACAO':str,\
            'HORA_ULTIMA_ATUALIZACAO':str}


DadosRelevantes = ['ANO_ELEICAO','SIGLA_UF','SIGLA_UE','DESCRICAO_UE',\
                'CODIGO_CARGO','DESCRICAO_CARGO','NOME_CANDIDATO',\
                'SEQUENCIAL_CANDIDATO','NUMERO_CANDIDATO','CPF_CANDIDATO',\
                'NOME_URNA_CANDIDATO','COD_SITUACAO_CANDIDATURA',\
                'DES_SITUACAO_CANDIDATURA','NUMERO_PARTIDO','SIGLA_PARTIDO',\
                'CODIGO_LEGENDA','COMPOSICAO_LEGENDA',\
                'CODIGO_OCUPACAO','DESCRICAO_OCUPACAO',\
                'NUM_TITULO_ELEITORAL_CANDIDATO','IDADE_DATA_ELEICAO',\
                'CODIGO_SEXO','DESCRICAO_SEXO','COD_GRAU_INSTRUCAO',\
                'DESCRICAO_GRAU_INSTRUCAO','CODIGO_ESTADO_CIVIL',\
                'DESCRICAO_ESTADO_CIVIL','CODIGO_COR_RACA',\
                'DESCRICAO_COR_RACA','CODIGO_NACIONALIDADE',\
                'DESCRICAO_NACIONALIDADE','SIGLA_UF_NASCIMENTO',\
                'NOME_MUNICIPIO_NASCIMENTO','DESPESA_MAX_CAMPANHA',\
                'COD_SIT_TOT_TURNO','DESC_SIT_TOT_TURNO','NM_EMAIL',\
                'NUMERO_BENS','VALOR_BEM','TOTAL_VOTOS']    
    
########################
### Código principal ###    
########################

# FAZER!
# Ver se # sequencial se repete sem/com inclusão de prefeitos, governadores:
# R: sim, se repete.
# FIM DO FAZER.

path = '/home/skems/pessoal/analises/canditatos_meRepresenta/dados/'

#ano='2016'
#bempath = path+'bem_candidato_'+ano+'/'
#bemfiles = glob(bempath+'bem_candidato_'+ano+'_??.csv')
#bemfiles.sort()

#filebem = bemfiles[-1]
#bem = pd.read_csv(filebem, sep='\";\"', converters=BemTypes, engine='python')
#bemGrouped = bem.groupby('SQ_CANDIDATO')
#NumBens = bemGrouped.size()
#ValorBens = bemGrouped['VALOR_BEM'].sum()

allBases=[]    
# LOOP sobre anos:    
for a in range(2004,2018,2):
    ano = str(a)    

    # Lista arquivos de dados:    
    candpath = path+'consulta_cand_'+ano+'/'
    candfiles = glob(candpath+'consulta_cand_'+ano+'_??.csv')
    candfiles.sort()
    bempath = path+'bem_candidato_'+ano+'/'
    bemfiles = glob(bempath+'bem_candidato_'+ano+'_??.csv')
    bemfiles.sort()
    votospath = path+'votacao_candidato_munzona_'+ano+'/'
    votosfiles = glob(votospath+'votacao_candidato_munzona_'+ano+'_??.csv')
    votosfiles.sort()
    if np.any([cand[-6:]!=votos[-6:] for cand,votos in zip(candfiles,votosfiles)]):
        print '!! Arquivos de candidatos e votos não estão alinhados por UF !!'
    if np.any([cand[-6:]!=bem[-6:] for cand,bem in zip(candfiles,bemfiles)]):
        print '!! Arquivos de candidatos e bens não estão alinhados por UF !!'

    # LOOP sobre estados:
    for filecand,filebem,filevotos in zip(candfiles,bemfiles,votosfiles):
        print '**',filecand[-6:-4], ano, '**'
        # Carrega arquivo de candidatos:
        cand = pd.read_csv(filecand, sep='\";\"', converters=CandTypes, engine='python')
        print "Total de candidatos:", len(cand)
        # Seleciona apenas votos para cargos de Deputado Federal, Estadual, Distrital e Vereador
        cand = cand.loc[cand['CODIGO_CARGO'].isin([6,7,8,13])]
        print "Candidatos a vereador e deputados:", len(cand)
        # Seleciona apenas candidatos aptos: Deferidos, e Deferidos e Indeferidos c/ Recurso:
        cand = cand.loc[cand['COD_SITUACAO_CANDIDATURA'].isin([2,16,4])]
        print "Candidatos aptos:", len(cand)
    
        # Carrega arquivos de bens:
        print 'Carregando bens...'
        bem = pd.read_csv(filebem, sep='\";\"', converters=BemTypes, engine='python')
        bemGrouped = bem.groupby('SQ_CANDIDATO')
        # Conta número de bens:         
        NumBens = bemGrouped.size()
        NumBens.name = 'NUMERO_BENS'
        # Totaliza valor dos bens:
        ValorBens = bemGrouped['VALOR_BEM'].sum() 
    
        # Carrega arquivo de votos:
        print 'Carregando votos...'
        votos = pd.read_csv(filevotos, sep='\";\"', converters=VotoTypes, engine='python')
        # Seleciona apenas votos para cargos de Deputado Federal, Estadual, Distrital e Vereador:
        votos = votos.loc[votos['CODIGO_CARGO'].isin([6,7,8,13])]
        # Seleciona apenas candidatos aptos: Deferidos, e Deferidos e Indeferidos c/ Recurso:
        votos = votos.loc[votos['CODIGO_SIT_CANDIDATO'].isin([2,16,4])]
    
        # Teste de sanidade: queremos apenas um nome por núm. seq. do candidato:
        # !! Em 2008 existiam códigos iguais em estados diferentes !!
        # !! Em 2004 existiam códigos iguais em cidades diferentes !!
        if ano!='2004':
            nomes = votos.groupby('SQ_CANDIDATO')['NOME_CANDIDATO'].nunique()
            if len(nomes) != np.sum(nomes):
                print '!!! Múltiplos candidatos com mesmo # sequencial !!!'
                        
        # Agrega votos de cada candidato pelas zonas eleitorais
        # E junta o resultado à base de candidatos:
        print 'Juntando cand, votos e bens...'
        if ano=='2004':
            votosTotais = pd.DataFrame({'TOTAL_VOTOS' : votos.groupby(['SIGLA_UE','SQ_CANDIDATO'])['TOTAL_VOTOS'].sum()}).reset_index()            
            base = pd.merge(cand,votosTotais, how='left',left_on=['SIGLA_UE','SEQUENCIAL_CANDIDATO'], right_on=['SIGLA_UE','SQ_CANDIDATO'])
        else:
            votosTotais = votos.groupby('SQ_CANDIDATO')['TOTAL_VOTOS'].sum()
            base = cand.join(NumBens, on='SEQUENCIAL_CANDIDATO')
            base = base.join(ValorBens, on='SEQUENCIAL_CANDIDATO')            
            base = base.join(votosTotais, on='SEQUENCIAL_CANDIDATO')
            
        # Prepara datas de nascimento e calcula idade dos candidatos caso inexistente:
        print 'Calculando idades...'
        base['DATA_NASCIMENTO'] = base['DATA_NASCIMENTO'].apply(FormatDate)
        base['DATA_NASCIMENTO'] = pd.to_datetime(base['DATA_NASCIMENTO'],format="%d/%m/%Y", errors='raise', coerce=True)
        base['IDADE_DATA_ELEICAO'] = base.apply(lambda row: ArrumaIdade(row['IDADE_DATA_ELEICAO'], row['DATA_NASCIMENTO'],row['ANO_ELEICAO']),axis=1)
        
        # Coloca base do estado na lista:
        print 'Agrupando bases...'
        allBases.append(base[sort(list(set(base.columns.values) & set(DadosRelevantes)))])

# Concatena as bases de todas as UFs na mesma base:
base = pd.concat(allBases, ignore_index=True)

# Adiciona colunas de novos indicadores, calculados a partir dos originais:

# Categoria de profissões:
profFile = '/home/skems/pessoal/analises/canditatos_meRepresenta/analise/profissoes.txt'
CategProfis = pd.read_csv(profFile,sep=';')
ProfisDic = {prof:cat for prof,cat in zip(CategProfis.PROFISSAO.values,CategProfis.CATEGORIA.values)}
Categoria = base['DESCRICAO_OCUPACAO'].map(ProfisDic)

# Tamanho de nomes e tamanho de coligações:
NumNomesUrna = base.NOME_URNA_CANDIDATO.astype(str).str.split().apply(lambda x:len(x)).values
NumNomesCand = base.NOME_CANDIDATO.astype(str).str.split().apply(lambda x:len(x)).values
TamanhoColigacao = base.COMPOSICAO_LEGENDA.apply(lambda x: x.count('/')+1)

# Número de votos em eleições anteriores:
base['NUM_TITULO_ELEITORAL_CANDIDATO'] = \
base.NUM_TITULO_ELEITORAL_CANDIDATO.astype(str).str.replace(' ','').str.replace('#NI#','-1').astype(int)
ByTitEleitor = base.groupby('NUM_TITULO_ELEITORAL_CANDIDATO')
def NumPrevElections(candidate, year):
    return np.sum((ByTitEleitor.get_group(candidate)['ANO_ELEICAO']<year).astype(int))
def PrevVotes(candidate, year):
    temp = ByTitEleitor.get_group(candidate)
    return np.sum(temp.loc[temp.ANO_ELEICAO<year].TOTAL_VOTOS)
NumEleicoesAntes = base[['NUM_TITULO_ELEITORAL_CANDIDATO','ANO_ELEICAO']].apply(lambda x: NumPrevElections(*x), axis=1)
NumVotosAntes = base[['NUM_TITULO_ELEITORAL_CANDIDATO','ANO_ELEICAO']].apply(lambda x: PrevVotes(*x), axis=1)


base.insert(loc=len(base.columns)-1, column='DESCRICAO_CATEGORIA', value=Categoria)
base.insert(loc=len(base.columns)-1, column='TAMANHO_NOME', value=NumNomesCand)
base.insert(loc=len(base.columns)-1, column='TAMANHO_NOME_URNA', value=NumNomesUrna)
base.insert(loc=len(base.columns)-1, column='TAMANHO_LEGENDA', value=TamanhoColigacao)
base.insert(loc=len(base.columns)-1, column='NUM_ELEICOES_ANTERIORES', value=NumEleicoesAntes)
base.insert(loc=len(base.columns)-1, column='TOTAL_VOTOS_ANTERIORES', value=NumVotosAntes)

togo = base[['ANO_ELEICAO', 'CODIGO_CARGO', 'CODIGO_COR_RACA',
       'CODIGO_ESTADO_CIVIL', 'CODIGO_LEGENDA', 'CODIGO_NACIONALIDADE',
       'CODIGO_OCUPACAO', 'CODIGO_SEXO', 'COD_GRAU_INSTRUCAO',
       'COD_SITUACAO_CANDIDATURA', 'COD_SIT_TOT_TURNO',
       'COMPOSICAO_LEGENDA', 'CPF_CANDIDATO', 'DESCRICAO_CARGO',
       'DESCRICAO_COR_RACA', 'DESCRICAO_ESTADO_CIVIL',
       'DESCRICAO_GRAU_INSTRUCAO', 'DESCRICAO_NACIONALIDADE',
       'DESCRICAO_OCUPACAO', 'DESCRICAO_SEXO', 'DESCRICAO_UE',
       'DESC_SIT_TOT_TURNO', 'DESPESA_MAX_CAMPANHA',
       'DES_SITUACAO_CANDIDATURA', 'IDADE_DATA_ELEICAO', 'NM_EMAIL',
       'NOME_CANDIDATO', 'NOME_MUNICIPIO_NASCIMENTO',
       'NOME_URNA_CANDIDATO', 'NUMERO_BENS', 'NUMERO_CANDIDATO',
       'NUMERO_PARTIDO', 'NUM_TITULO_ELEITORAL_CANDIDATO',
       'SEQUENCIAL_CANDIDATO', 'SIGLA_PARTIDO', 'SIGLA_UE', 'SIGLA_UF',
       'SIGLA_UF_NASCIMENTO', 'VALOR_BEM', 'DESCRICAO_CATEGORIA',
       'TAMANHO_NOME', 'TAMANHO_NOME_URNA', 'TAMANHO_LEGENDA',
       'NUM_ELEICOES_ANTERIORES', 'TOTAL_VOTOS_ANTERIORES', 
       'TOTAL_VOTOS']]

togo.to_csv('../dados/concatenados/completa+bens.csv', sep='>', index=False)

#sys.exit()

sort(base.IDADE_DATA_ELEICAO.unique())


totalCandidatos = float(len(base))

# Divide a base em grupos (femininos):
femininos  = base.loc[base['CODIGO_SEXO']==4]
femNan     = femininos.loc[femininos['TOTAL_VOTOS'].isnull()]
fem0       = femininos.loc[femininos['TOTAL_VOTOS']==0]
fem1       = femininos.loc[femininos['TOTAL_VOTOS']==1]
fem10      = femininos.loc[(femininos['TOTAL_VOTOS']>1) & (femininos['TOTAL_VOTOS']<=10)]
# Conta candidatos em cada grupo:
femTot    = float(len(femininos))
femNanTot = float(len(femNan))
fem0Tot   = float(len(fem0))
fem1Tot   = float(len(fem1))
fem10Tot  = float(len(fem10))


# Divide a base em grupos (masculinos):
masculinos  = base.loc[base['CODIGO_SEXO']==2]
mascNan     = masculinos.loc[masculinos['TOTAL_VOTOS'].isnull()]
masc0       = masculinos.loc[masculinos['TOTAL_VOTOS']==0]
masc1       = masculinos.loc[masculinos['TOTAL_VOTOS']==1]
masc10      = masculinos.loc[(masculinos['TOTAL_VOTOS']>1) & (masculinos['TOTAL_VOTOS']<=10)]
# Conta candidatos em cada grupo:
mascTot    = float(len(masculinos))
mascNanTot = float(len(mascNan))
masc0Tot   = float(len(masc0))
masc1Tot   = float(len(masc1))
masc10Tot  = float(len(masc10))

print ""
print "Fem  (%): {:.1f}".format(femTot/totalCandidatos*100)
print "Masc (%): {:.1f}".format(mascTot/totalCandidatos*100)
print "                             {:>10} {:>10} {:>10} {:>10}".format('NaN','0 votos','1 voto','<=10 votos')
print "Distribuição dos masculinos: {:10.2f} {:10.2f} {:10.2f} {:10.2f}".format(mascNanTot/mascTot*100,masc0Tot/mascTot*100,masc1Tot/mascTot*100,masc10Tot/mascTot*100)
print "Distribuição dos femininos:  {:10.2f} {:10.2f} {:10.2f} {:10.2f}".format(femNanTot/femTot*100,fem0Tot/femTot*100,fem1Tot/femTot*100,fem10Tot/femTot*100)

# Comparação de distribuições de parâmetros entre potenciais fantasmas e controle:
zero = base.loc[base['TOTAL_VOTOS']==0]
nonzero = base.loc[base['TOTAL_VOTOS']==6]
x='DESPESA_MAX_CAMPANHA'

xbins=np.linspace(0,1e6,50)
zcounts, zedges = np.histogram(zero[x],bins=xbins)
zcenter = ((np.insert(zedges,0,0)+np.append(zedges,0))/2.0)[1:-1]
zerr = np.sqrt(zcounts)
znorm = np.sum(zcounts)
pl.errorbar(zcenter, zcounts.astype(float)/znorm, yerr=zerr/znorm, fmt='or')

nzcounts, nzedges = np.histogram(nonzero[x],bins=xbins)
nzcenter = ((np.insert(nzedges,0,0)+np.append(nzedges,0))/2.0)[1:-1]
nzerr = np.sqrt(nzcounts)
nznorm = np.sum(nzcounts)
pl.errorbar(nzcenter, nzcounts.astype(float)/nznorm, yerr=nzerr/nznorm, fmt='ob')
#pl.yscale('log')
pl.show()

# Outra comparação:
# !! Problema: é preciso que 
x='NUMERO_PARTIDO'
x='CODIGO_OCUPACAO'
zlabels = zero.groupby(x).groups.keys()
zcounts = zero.groupby(x).size()
zerr = np.sqrt(zcounts)
znorm = float(np.sum(zcounts))/100.0

pl.errorbar(zlabels,zero.groupby(x).size()/znorm,yerr=np.array(zerr)/znorm, fmt='or');
pl.plot(nonzero.groupby(x).groups.keys(),nonzero.groupby(x).size()/len(nonzero)*100, 'ob');
#pl.xlim([0,1e6])
pl.show()
