
script=~/pessoal/analises/canditatos_meRepresenta/analise/distrib-votos.py

UF=$1

$script consulta_cand_2008/consulta_cand_2008_$UF.csv votacao_candidato_munzona_2008/votacao_candidato_munzona_2008_$UF.csv

$script consulta_cand_2012/consulta_cand_2012_$UF.csv votacao_candidato_munzona_2012/votacao_candidato_munzona_2012_$UF.csv

