# Fake female candidates in Brazilian elections

This repository contains the analysis done prior to 2018 Brazilian elections, with the goal of
profiling and identifying possible fake female candidates. This study was conducted in collaboration
with [#meRepresenta](http://merepresenta.org.br) and [AzMina](https://azmina.com.br) and
used by journalists to write the articles:

* <https://azmina.com.br/especiais/laranjas-profissionais-com-zero-votos-em-eleicoes-anteriores-elas-sao-candidatas-em-2018>
* <https://theintercept.com/2018/09/19/partidos-mulheres-laranjas-cota-eleicoes>

The final and complete report can be found at: <http://www.fma.if.usp.br/~hsxavier/analises/fantasmas.html>

### Background

Since 2009, the Brazilian law mandates that 30% of each party's candidates must be female, but most parties
fulfill this requirement by enrolling women that don't campaign, don't get support from their parties and don't
even vote for themselves (what we called 'fake candidates'). Besides profiling the fake candidates, our goal was to
identify them prior to elections, in order to discourage parties to employ them.

## Project's structure

Unfortunately this repository is a bit disorganized, is mostly commented in Portuguese and was not published at the
time of elaboration. In this README I try, in retrospect, to explain the project's structure.

* The `dados` folder used to contain 24GB of data gathered from
[Tribunal Superior Eleitoral](http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1/repositorio-de-dados-eleitorais),
namely the candidate's details, wealth records and voting results databases, from 2004 to 2018 (voting results for 2018 were not
available at the time). I only uploaded to github auxiliary data I created.

* The `analise` folder contains Jupyter notebooks used in the analysis, tables in `.csv` and Excel format with
the final selection of potential fake candidates. It also contains auxiliary ETL scripts.

* The `analise` sub-folder `tabelas` contains tables that resulted from my profiling and that was used by journalists in their
article.

* The `analise` sub-folder `modelos` contains machine learning models used to predict possible fake candidates for
the 2018 elections.

## Credits

The analysis and modeling was done by Henrique S. Xavier. The news articles were written by Helena Bertho and edited by
Carolina Oms. We also collaborated with [#meRepresenta](http://merepresenta.org.br).