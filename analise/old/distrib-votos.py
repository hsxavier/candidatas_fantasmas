#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import sys
from glob import glob

#filecand  = sys.argv[1]
#filevotos = sys.argv[2]

ano = str(2008)

path = '/home/skems/pessoal/analises/canditatos_meRepresenta/dados/'
candpath = path+'consulta_cand_'+ano+'/'
candfiles = glob(candpath+'consulta_cand_'+ano+'_??.csv')
candfiles.sort()
votospath = path+'votacao_candidato_munzona_'+ano+'/'
votosfiles = glob(votospath+'votacao_candidato_munzona_'+ano+'_??.csv')
votosfiles.sort()
if np.any([cand[-6:]!=votos[-6:] for cand,votos in zip(candfiles,votosfiles)]):
    print '!! Arquivos de candidatos e votos não estão alinhados por UF !!'


filecand = '/home/skems/pessoal/analises/canditatos_meRepresenta/dados/concatenados/consulta_cand_2008.csv'
filevotos= '/home/skems/pessoal/analises/canditatos_meRepresenta/dados/concatenados/votacao_candidato_munzona_2008.csv'
#filecand = '/home/skems/pessoal/analises/canditatos_meRepresenta/dados/concatenados/consulta_cand_2012.csv'
#filevotos= '/home/skems/pessoal/analises/canditatos_meRepresenta/dados/concatenados/votacao_candidato_munzona_2012.csv'

# Carrega arquivo de candidatos:
cand = pd.read_csv(filecand, sep='\";\"')
print "Total de candidatos:", len(cand)
# Seleciona apenas votos para cargos de Deputado Federal, Estadual, Distrital e Vereador:
cand = cand.loc[cand['CODIGO_CARGO'].isin([6,7,8,13])]
print "Candidatos a vereador e deputados:", len(cand)
# Seleciona apenas candidatos aptos: Deferidos, e Deferidos e Indeferidos c/ Recurso:
cand = cand.loc[cand['COD_SITUACAO_CANDIDATURA'].isin([2,16,4])]
print "Candidatos aptos:", len(cand)

# Carrega arquivo de votos:
votos = pd.read_csv(filevotos, sep='\";\"')
# Seleciona apenas votos para cargos de Deputado Federal, Estadual, Distrital e Vereador:
votos = votos.loc[votos['CODIGO_CARGO'].isin([6,7,8,13])]
# Seleciona apenas candidatos aptos: Deferidos, e Deferidos e Indeferidos c/ Recurso:
votos = votos.loc[votos['CODIGO_SIT_CANDIDATO'].isin([2,16,4])]

# Teste de sanidade: queremos apenas um nome por núm. seq. do candidato:
# !! Em 2008 existiam códigos iguais em estados diferentes !! 
nomes = votos.groupby('SQ_CANDIDATO')['NOME_CANDIDATO'].nunique()
print "# de SQ_CAND e NOME_CAND:", len(nomes), np.sum(nomes)

# Agrega votos de cada candidato pelas zonas eleitorais:
votosTotais = votos.groupby('SQ_CANDIDATO')['TOTAL_VOTOS'].sum()

# Junta a base dos candidatos com a base dos votos:
base = cand.join(votosTotais, on='SEQUENCIAL_CANDIDATO')
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