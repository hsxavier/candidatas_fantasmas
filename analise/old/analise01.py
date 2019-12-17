# -*- coding: utf-8 -*-
"""
Created on Sat May  5 19:57:06 2018

@author: skems
"""

from glob import glob
import pandas as pd


##################
### Definições ###
##################

# Definição do diretório dos dados:
data_dir = '../dados'


###############
### Funções ###
###############

# Lê arquivo com lista (um elemento por linha) e salva numa lista do python:
def read_list(path):
    with open(path) as f:
        output = [item.strip(' ') for item in f.read().splitlines()]
    return output
    
# Acha posições das colunas selecionadas na lista completa:
# (ignora colunas inexistentes)
def column_index(all_cols, selection):
    indexes = [all_cols.index(item) if item in all_cols else -1 for item in selection]
    return filter(lambda item: item != -1, indexes)
 
   
########################
### Script principal ###   
########################
   
# Carrega nome de todas as colunas e das que queremos:
# Dos arquivos dos candidatos:
cols_cand_selec = read_list(data_dir+'/colunas_consulta_cand_selecao.txt')
# Até 2010:
cols_cand_2010  = read_list(data_dir+'/colunas_consulta_cand_ate2010.txt')
index_cand_2010 = column_index(cols_cand_2010,cols_cand_selec)
names_cand_2010 = [cols_cand_2010[i] for i in index_cand_2010]
# 2012:
cols_cand_2012  = read_list(data_dir+'/colunas_consulta_cand_2012.txt')
index_cand_2012 = column_index(cols_cand_2012,cols_cand_selec)
names_cand_2012 = [cols_cand_2012[i] for i in index_cand_2012]
# A partir de 2014:
cols_cand_2014  = read_list(data_dir+'/colunas_consulta_cand_apartir2014.txt')
index_cand_2014 = column_index(cols_cand_2014,cols_cand_selec)
names_cand_2014 = [cols_cand_2014[i] for i in index_cand_2014]
# Dos arquivos das votações:
cols_voto_selec = read_list(data_dir+'/colunas_votacao_candidato_munzona_selecao.txt')
# Até 2012:
cols_voto_2012  = read_list(data_dir+'/colunas_votacao_candidato_munzona_ate2012.txt')
index_voto_2012 = column_index(cols_voto_2012,cols_voto_selec)
names_voto_2012 = [cols_voto_2012[i] for i in index_voto_2012]
# A partir de 2014:
cols_voto_2014  = read_list(data_dir+'/colunas_votacao_candidato_munzona_apartir2014.txt')
index_voto_2014 = column_index(cols_voto_2014,cols_voto_selec)
names_voto_2014 = [cols_voto_2014[i] for i in index_voto_2014]

# Carrega arquivos dos candidatos:
cand_dirs  = glob(data_dir+'/consulta_cand_2008')
cand_files = glob(cand_dirs[0]+'/consulta_cand_????_??.txt')
cand_files.sort()
cand = pd.read_csv(cand_files[0],sep=';', usecols=index_cand_2010, names=names_cand_2010)

# Carrega arquivos dos votos:
voto_dirs  = glob(data_dir+'/votacao_candidato_munzona_2008')
voto_files = glob(voto_dirs[0]+'/votacao_candidato_munzona_????_??.txt').sort()
voto_files.sort()
voto = pd.read_csv(voto_files[0],sep=';', usecols=index_voto_2012, names=names_voto_2012)

total_votos = voto.groupby('SQ_CANDIDATO')['TOTAL_VOTOS'].sum()
grouped = pd.merge(cand,total_votos, on='SQ_CANDIDATO')