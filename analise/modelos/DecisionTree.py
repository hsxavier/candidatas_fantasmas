# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:10:22 2018

@author: skems
"""

import pandas as pd
import numpy as np

############################
### Processamento prévio ###
############################

# Carrega os dados já selecionados:
base = pd.read_csv('../dadosParaModelar/deputados2010.csv')

# Codifica as variáveis que ainda estão em forma de texto:
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
base.SIGLA_UF = encoder.fit_transform(base.SIGLA_UF)
base.DESCRICAO_CATEGORIA = encoder.fit_transform(base.DESCRICAO_CATEGORIA)

# Define o critério para ser fantasma:
base.TOTAL_VOTOS = (base.TOTAL_VOTOS<=5).astype(int)

# separa em variáveis preditivas e classe (fantasma ou não):
X = base.iloc[:,:-1].values
y = base.iloc[:,-1].values


########################################
### Treinamento e previsão do modelo ###
########################################

# Divide os dados entre treinamento e teste:
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# Treina a Decision Tree na amostra de treinamento:
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion='entropy', 
                                    min_samples_leaf=20, min_samples_split=40)
classifier.fit(X_train, y_train)

# Prediz para a amostra de testes se são fantasmas ou não:
y_pred = classifier.predict(X_test)


################################################################
### Análise dos resultados e comparação com amostra de teste ###
################################################################

# Calcula a matriz de confusão:
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
#print cm

# Queremos um modelo com alta pureza e com maior número de selecionados:
print '# de selecionados como fantasmas: {}'.format(np.sum(cm[:,1]))
print 'Pureza dos selecionados: {:.2f}%'\
.format(float(cm[1,1])/np.sum(cm[1,1]+cm[0,1])*100)

# Salva a Decision Tree num arquivo para visualização:
from sklearn.tree import export_graphviz
export_graphviz(classifier, out_file='tree.dot',  
                filled=True, rounded=True)

