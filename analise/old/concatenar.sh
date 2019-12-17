#!/usr/bin/env bash

nomes=$1
prefix=$2

echo "Criando header..."
./criaHeader.py $nomes > concatenados/$prefix.csv

echo "Contando linhas na fonte:"
wc -l ${prefix}/${prefix}_??.txt | tail -n 1
echo "Concatenando arquivos para o arquivo com header..."
cat ${prefix}/${prefix}_??.txt >> concatenados/$prefix.csv
echo "Contando linhas na saída:"
wc -l concatenados/$prefix.csv | awk '{print $1}'
