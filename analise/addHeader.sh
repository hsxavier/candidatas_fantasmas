#!/usr/bin/env bash

# Para todos os arquivos passados como input para esse script,
# ele faz o seguinte:
# -- Retira a primeira aspas do header;
# -- Retira a primeira aspas de cada linha do arquivo .txt de dados;
# -- Retira a última aspas do header;
# -- Retira a última aspas de cada linha do arquivo .txt de dados;
# Dessa forma, as colunas ficam separadas por ";" (as aspas também fazem parte);
# -- Escreve o header no arquivo de mesmo nome, mas com extensão .csv;
# -- Escreve nesse arquivo os dados, embaixo do header.
# -- Muda o encoding do texto para UTF-8.
#
# EXEMPLO: addHeader.sh votacao_candidato_munzona_2012_*.txt
#
# Escrito por Henrique S. Xavier (hsxavier@if.usp.br) em 13/05/2018


for file in $@; do
    new=`echo $file | sed 's/.txt/.csv/g'`
    sed -e 's/^\"//g' -e 's/\"$//g' header.txt > temp.csv
    sed -e 's/^\"//g' -e 's/\".$//g' $file >> temp.csv 
    sed 's/\"$//g' temp.csv | sed 's/\";$/\";\"/g' | iconv -f ISO-8859-1 -t UTF-8 > $new
done

rm -f temp.csv

