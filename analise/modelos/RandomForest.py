# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:10:22 2018

@author: skems
"""

import pandas as pd
import numpy as np


CodDescDict = {'CODIGO_CARGO': {6: 'DEPUTADO FEDERAL',7: 'DEPUTADO ESTADUAL',
  8: 'DEPUTADO DISTRITAL',13: 'VEREADOR'},
 'CODIGO_COR_RACA': {1: 'BRANCA',2: 'PRETA',3: 'PARDA',4: 'AMARELA',
  5: 'IND\xc3\x8dGENA'},
 'CODIGO_ESTADO_CIVIL': {0: 'N\xc3\x83O INFORMADO',1: 'SOLTEIRO(A)',
  3: 'CASADO(A)',5: 'VI\xc3\x9aVO(A)',7: 'SEPARADO(A) JUDICIALMENTE',
  9: 'DIVORCIADO(A)'},
 'CODIGO_NACIONALIDADE': {0: 'N\xc3\x83O INFORMADA',1: 'BRASILEIRA NATA',
  2: 'BRASILEIRA (NATURALIZADA)',3: 'PORTUGUESA COM IGUALDADE DE DIREITOS',
  4: 'ESTRANGEIRO'},
 'CODIGO_SEXO': {0: 'N\xc3\x83O INFORMADO', 2: 'MASCULINO', 4: 'FEMININO'},
 'COD_GRAU_INSTRUCAO': {0: 'N\xc3\x83O INFORMADO',1: 'ANALFABETO',
  2: 'L\xc3\x8a E ESCREVE',3: 'FUNDAMENTAL INCOMPLETO',
  4: 'FUNDAMENTAL COMPLETO',5: 'M\xc3\x89DIO INCOMPLETO',
  6: 'M\xc3\x89DIO COMPLETO',7: 'SUPERIOR INCOMPLETO',8: 'SUPERIOR COMPLETO'},
 'COD_SITUACAO_CANDIDATURA': {2: 'DEFERIDO',4: 'INDEFERIDO COM RECURSO',
  16: 'DEFERIDO COM RECURSO'},
 'NUMERO_PARTIDO': {10: 'PRB',11: 'PP',12: 'PDT',13: 'PT',14: 'PTB',
  15: 'PMDB',16: 'PSTU',17: 'PSL',18: 'REDE',19: 'PTN',20: 'PSC',
  21: 'PCB',22: 'PR',23: 'PPS',25: 'DEM',26: 'PAN',27: 'PSDC',28: 'PRTB',
  29: 'PCO',30: 'NOVO',31: 'PHS',33: 'PMN',35: 'PMB',36: 'PTC',40: 'PSB',
  43: 'PV',44: 'PRP',45: 'PSDB',50: 'PSOL',51: 'PEN',54: 'PPL',55: 'PSD',
  56: 'PRONA',65: 'PC do B',70: 'PT do B',77: 'SD',90: 'PROS'}}


############################
### Processamento prévio ###
############################

# Carrega os dados já selecionados:
#base = pd.read_csv('../dadosParaModelar/deputados2010.csv')
base = pd.read_csv('../../dados/concatenados/completa+bens.csv',sep='>')

# IPCA para deflacionar valores (todos em outubro, com exceção de 2018 (em junho)):
anos   = [2004,2006,2008,2010,2012,2014,2016, 2018]
ipca   = np.array([608.7, 668.6, 740.8, 812.0, 915.6, 1033.0, 1224.9,1300.0])
deflate = dict(zip(anos,ipca[-1]/ipca))
DeflacBem = base.VALOR_BEM*(base.ANO_ELEICAO.map(deflate))
# COLOCA VALORES DEFLACIONADOS NA BASE:
base['VALOR_BEM_DEFLAC'] = DeflacBem

# Carrega categorias de profissões:
profBase = pd.read_csv('../profissoes-v2.txt',sep=';')
profDict = profBase.groupby('PROFISSAO')['CATEGORIA'].unique().apply(lambda x: x[-1]).to_dict()

# Seleciona dados relevantes:
DataToModel = base.loc[(base.CODIGO_CARGO.isin([6,7])) & \
                       ((base.ANO_ELEICAO==2010) | (base.ANO_ELEICAO==2014)) & \
#                       (base.CODIGO_SEXO==4)]\
#DataToModel = base.loc[((base.ANO_ELEICAO>2009) | (base.ANO_ELEICAO<=2016)) & \
#                       (base.CODIGO_SEXO==4)]\
[['ANO_ELEICAO','CODIGO_CARGO','CODIGO_ESTADO_CIVIL','CODIGO_NACIONALIDADE','COD_GRAU_INSTRUCAO',\
#[['ANO_ELEICAO','CODIGO_ESTADO_CIVIL','CODIGO_NACIONALIDADE','COD_GRAU_INSTRUCAO',\
  'COD_SITUACAO_CANDIDATURA','DESPESA_MAX_CAMPANHA','IDADE_DATA_ELEICAO','NUMERO_PARTIDO','SIGLA_UF',\
  'DESCRICAO_OCUPACAO', 'TAMANHO_NOME', 'TAMANHO_NOME_URNA', 'NUM_ELEICOES_ANTERIORES',\
  'TOTAL_VOTOS_ANTERIORES','VALOR_BEM_DEFLAC','NUMERO_BENS','TOTAL_VOTOS']]

# Codifica as variáveis que ainda estão em forma de texto:
from sklearn.preprocessing import LabelEncoder
encoderUF = LabelEncoder()
DataToModel.SIGLA_UF = encoderUF.fit_transform(DataToModel.SIGLA_UF)
encoderCAT = LabelEncoder()
DataToModel = DataToModel.replace({'DESCRICAO_OCUPACAO': profDict})
DataToModel.DESCRICAO_OCUPACAO = encoderCAT.fit_transform(DataToModel.DESCRICAO_OCUPACAO)
# E ajusta as problemáticas:
DataToModel.TOTAL_VOTOS[DataToModel.TOTAL_VOTOS.isnull()==True] = -1
DataToModel.TOTAL_VOTOS_ANTERIORES[DataToModel.TOTAL_VOTOS_ANTERIORES.isnull()==True] = -1
DataToModel.NUMERO_BENS[DataToModel.NUMERO_BENS.isnull()==True] = -1
DataToModel.VALOR_BEM_DEFLAC[DataToModel.VALOR_BEM_DEFLAC.isnull()==True] = -1
#DataToModel.VALOR_BEM[DataToModel.VALOR_BEM.isnull()==True] = -1
#DataToModel.TOTAL_VOTOS_ANTERIORES = np.nan_to_num(DataToModel.TOTAL_VOTOS_ANTERIORES)
#DataToModel.NUMERO_BENS = np.nan_to_num(DataToModel.NUMERO_BENS)
#DataToModel.VALOR_BEM = np.nan_to_num(DataToModel.VALOR_BEM)

# Define o critério para ser fantasma:
DataToModel.TOTAL_VOTOS = ((DataToModel.TOTAL_VOTOS>=0) & \
                           (DataToModel.TOTAL_VOTOS<=5)).astype(int)

# Seleciona dados para modelar:
# separa em variáveis preditivas e classe (fantasma ou não):
X = DataToModel.loc[DataToModel.ANO_ELEICAO<2014].iloc[:,1:-1].values
y = DataToModel.loc[DataToModel.ANO_ELEICAO<2014].iloc[:,-1].values

# Seleciona dados para aplicar:
last_X = DataToModel.loc[DataToModel.ANO_ELEICAO==2014].iloc[:,1:-1].values
last_y = DataToModel.loc[DataToModel.ANO_ELEICAO==2014].iloc[:,-1].values

########################################
### Treinamento e previsão do modelo ###
########################################

# Divide os dados entre treinamento e teste:
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# Treina o modelo nos dados:
# Se selecionarmos min_samples_leaf=2, parece que o modelo se torna, na 
# maioria das vezes, bem criterioso (alta pureza mas baixo número de 
# selecionados).
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 100, criterion = 'entropy',\
                                    n_jobs=-1)
classifier.fit(X_train, y_train)

# Prediz para a amostra de testes se são fantasmas ou não:
y_pred = classifier.predict(X_test)


################################################################
### Análise dos resultados e comparação com amostra de teste ###
################################################################

# Calcula a matriz de confusão:
from sklearn.metrics import confusion_matrix
# Completeza e pureza p/ amostra teste:
# Queremos um modelo com alta pureza e com maior número de selecionados:
print '# de selecionados como fantasmas: {}'.format(np.sum(cm[:,1]))
print 'Pureza dos selecionados: {:.2f}%'\
.format(float(cm[1,1])/np.sum(cm[1,1]+cm[0,1])*100)
print 'Completeza:              {:.2f}%'\
.format(float(cm[1,1])/np.sum(cm[1,1]+cm[1,0])*100)


# Vamos usar validaçao k-fold (do udemy):
#from sklearn.model_selection import cross_val_score
#accuracies = cross_val_score(classifier, X_train, y_train, cv=10, n_jobs=5)

# Função que retorna completeza e pureza em %:
def ComplPur(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    return [float(cm[1,1])/np.sum(cm[1,1]+cm[1,0])*100,\
            float(cm[1,1])/np.sum(cm[1,1]+cm[0,1])*100]
# Calculando confusion matrix em cross-validation:
from sklearn.cross_validation import KFold
kf = KFold(len(y_train), n_folds=5)
ComplPurKfold = []
for train_index, test_index in kf:
   kf_X_train, kf_X_test = X_train[train_index], X_train[test_index]
   kf_y_train, kf_y_test = y_train[train_index], y_train[test_index]
   classifier.fit(kf_X_train, kf_y_train)
   ComplPurKfold.append(ComplPur(kf_y_test, classifier.predict(kf_X_test)))
ComplPurMean = np.mean(ComplPurKfold,axis=0)
ComplPurDev  = np.std(ComplPurKfold,axis=0,ddof=1)
print '== Cross-validation =='
print 'Compl.: {:.2f} +/- {:.2f} %'.format(ComplPurMean[0],ComplPurDev[0])
print 'Pureza: {:.2f} +/- {:.2f} %'.format(ComplPurMean[1],ComplPurDev[1])

# Teste com ano deixado de fora:
classifier.fit(X_train, y_train)
last_y_pred = classifier.predict(last_X)
c,p = ComplPur(last_y,last_y_pred)
print 'Pureza dos selecionados: {:.2f}%'.format(p)
print 'Completeza:              {:.2f}%'.format(c)


# Vamos ver as características dos selecionados:
Xlabels   = DataToModel.columns.values[:-1]
Xselected = X_test[y_pred==1].astype(int)
Yselected = y_test[y_pred==1].astype(int)
selec = pd.DataFrame()
for i in range(0,len(Xlabels)):
    selec[Xlabels[i]] = pd.Series(Xselected[:,i])
for i in [0,1,2,3,4,5,8]:    
    selec[Xlabels[i]] = selec[Xlabels[i]].map(CodDescDict[Xlabels[i]])
selec['SIGLA_UF'] = encoderUF.inverse_transform(selec['SIGLA_UF'])
selec['DESCRICAO_CATEGORIA'] = \
encoderCAT.inverse_transform(selec['DESCRICAO_CATEGORIA'])
selec['FANTASMA'] = pd.Series(Yselected)
selec.transpose()