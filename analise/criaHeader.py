#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Este script pega um arquivo de texto <NOMES> com nomes das colunas 
(um por linha) e escreve na tela uma linha onde os nomes das colunas 
aparecem sepadados por ";", que será o mesmo separador dos dados.

USO:     criaHeader.py <NOMES>
EXEMPLO: criaHeader.py colunas_votacao_candidato_munzona_ate2012.txt

Criado por Henrique S. Xavier (hsxavier@if.usp.br) em 13/05/2018.
"""

import sys

# Docstring output:
if len(sys.argv) != 1 + 1:
    print(__doc__)
    sys.exit(1)


# Definição de função:
# Lê arquivo com lista (um elemento por linha) e salva numa lista do python:
def read_list(path):
    with open(path) as f:
        output = [item.strip(' ') for item in f.read().splitlines()]
    return output


# SCRIPT PRINCIPAL:
# Carrega arquivos com nomes das colunas:
colunas = sys.argv[1]
header = read_list(colunas)

# Imprime header no formato dos dados:
for name in header[:-1]:
    sys.stdout.write('\"'+name+'\";')
sys.stdout.write('\"'+header[-1]+'\"\n')



