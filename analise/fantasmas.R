library(electionsBR) # Para baixar os dados
library(ROCR) # Para fazer a curva ROC
# library(neuralnet) # Para rede neural?
# Abre ou baixa os detalhes de candidatos
if (! file.exists("cands14.rda")) {
    cands14 = electionsBR::candidate_fed(2014)
    # Seleciona apenas as colunas e dados relevantes para 
    # otimizar uso de memória
    cands14 = subset(cands14, DESCRICAO_CARGO %in% c("DEPUTADO DISTRITAL", "DEPUTADO ESTADUAL", "DEPUTADO FEDERAL"))
    names(cands14)[33] = "Escolaridade"
    names(cands14)[35] = "Estado_Civil"
    names(cands14)[37] = "Cor_Raca"
    cands14 = cands14[, c(6, 10, 11, 12, 13, 14, 15, 17, 19, 23, 26, 29, 31, 33, 35, 37, 39, 40, 42, 43, 45, 46)]
    # Converte os dados numéricos:
    cands14$IDADE_DATA_ELEICAO = as.numeric(cands14$IDADE_DATA_ELEICAO)
    cands14$DESPESA_MAX_CAMPANHA = as.numeric(cands14$DESPESA_MAX_CAMPANHA)
    save(cands14, file="cands14.rda")
} else {
    load("cands14.rda")
}
# Abre ou baixa os dados de votação
if (! file.exists("vote14.rda")) {
    vote14 = electionsBR::vote_mun_zone_fed(2014)
    # Seleciona apenas as colunas e dados relevantes para 
    # otimizar uso de memória
    vote14 = subset(vote14, DESCRICAO_CARGO %in% c("DEPUTADO DISTRITAL", "DEPUTADO ESTADUAL", "DEPUTADO FEDERAL"))
    vote14 = vote14[, c(7, 9, 10, 12, 13, 14, 15, 16, 18, 20, 22, 24, 29) ]
    vote14$TOTAL_VOTOS = as.numeric(vote14$TOTAL_VOTOS)
    save(vote14, file="vote14.rda")
} else {
    load("vote14.rda")
}
# São considerados "APTOS" os candidatos com situação de candidatura:
# Deferido; Deferido com recurso; Indeferido com recurso; Substituto pendente de julgamento
# TODO: verificar inconsistencias entre sit. cand. do arquivo de detalhes e do arquivo de votação

# TODO: espacialização do indicador de fantasma?
# TODO: fuzzy match entre nome e nome urna?

# Soma os votos de cada candidato e "gruda" essa tabela na tabela
# detalhe de candidatos. Estamos usando também a coluna 
# "DESC_SIT_CANDIDATO" na tabela de votação para poder comparar as duas
vot_agg = aggregate(vote14$TOTAL_VOTOS, sum, by=list(
            vote14$SQ_CANDIDATO, 
            vote14$DESC_SIT_CANDIDATO))
names(vot_agg) = c("SEQUENCIAL_CANDIDATO", "DESC_SIT_CAND_VOTE", "TOTAL_VOTOS")
cands_agg = merge(cands14, vot_agg, by = "SEQUENCIAL_CANDIDATO")

# Há 25168 candidatos registrados para os cargos de interesse
length(unique(cands14$SEQUENCIAL_CANDIDATO))
# Mas apenas 22039 com votação:
length(unique(vote14$SQ_CANDIDATO))
# E curiosamente, apenas 22025 com detalhes E votação...
length(unique(cands_agg$SEQUENCIAL_CANDIDATO))

# Quais são os candidatos sem dados de votação? Cancelados, renúncias, etc
sem_votacao = subset(cands14, ! cands14$SEQUENCIAL_CANDIDATO %in% vot_agg$SEQUENCIAL_CANDIDATO)
table(sem_votacao$DES_SITUACAO_CANDIDATURA)
sem_detalhes = subset(vot_agg, ! vot_agg$SEQUENCIAL_CANDIDATO %in% cands14$SEQUENCIAL_CANDIDATO)
table(sem_detalhes$DESC_SIT_CAND_VOTE)
# Das candidaturas com voto, mas sem detalhes, há 10 deferidas; inclusive uma com 15 mil votos!

cands_agg$VOTO_CLASSE = cut(cands_agg$TOTAL_VOTOS, breaks = c(-1, 0, 1, 5, 10, 100,1000, 1524361)) 
table(cands_agg$VOTO_CLASSE)
# No total, estão registradas 986 candidaturas com 0 votos, 1072 com até um voto, 1309 com até cinco votos, 1535 com até 10 votos.
# No entanto, esses números são ilusórios, pois a vasta maioria das candidaturas com zero votos (713) se referem a candidaturas indeferidas. 

cands_agg = subset(cands_agg, DES_SITUACAO_CANDIDATURA %in% c("DEFERIDO", "DEFERIDO COM RECURSO"))
# Agora vemos 86 candidaturas com zero votos, 172 com até um, 409 com até cinco, 635 com até dez...
table(cands_agg$VOTO_CLASSE)

# Vamos calcular o total de votos nominais válidos para cada UF, para
# poder depois comparar cada candidatura com a porcentagem de votos no estado
voto_uf = aggregate(cands_agg$TOTAL_VOTOS, by=list(cands_agg$SIGLA_UF), sum)
names(voto_uf) = c("SIGLA_UF", "VOTO_UF")
cands_agg = merge(cands_agg, voto_uf)

# Tentativa: vamos considerar apenas as candidaturas com até cinco votos OU até 0.001% dos votos do estado
cands_agg$FANTASMA = (cands_agg$TOTAL_VOTOS <= cands_agg$VOTO_UF * 1e-5 | cands_agg$TOTAL_VOTOS < 5)
# Ou use a linha seguinte para pegar os votos estritamente zero
# cands_agg$FANTASMA = (cands_agg$TOTAL_VOTOS == 0)

# Agora vamos analisar as colunas do nosso dataset
names(cands_agg)
# Colunas relevantes
# TODO: estudar colinearidade
# 1 - UF
# 3 - Desc Cargo
# 4 - Nome
# 5 - Numero
# 6 - CPF
# 7 - Nome urna
# 8 - Desc situação candidatura
# 9 - Partido
# 10 - Composição legenda
# 21 - Sit tot turno
# 23 - Desc situação candidatura (da tabela de votação)
#### Preditoras
# 11 - Ocupação
# 12 - Idade
# 13 - Sexo
# 14 - Instrução
# 15 - Estado civil
# 16 - Raça
# 17 - Nacionalidade
# 18 - UF nascimento (maybe comparar?)
# 19 - Municipio nascimento
# 20 - Despesa máxima campanha
# 21 - Sit tot turno
# 22 - E-mail
# TODO: separar em 2 modelos??
# cands_fed = subset(cands_agg, DESCRICAO_CARGO == "DEPUTADO FEDERAL")
# cands_est = subset(cands_agg, DESCRICAO_CARGO %in% c("DEPUTADO DISTRITAL", "DEPUTADO ESTADUAL"))

# Alguns modelinhos para analisar efeito simples (um fator por vez)
# Modelo neutro: sem efeito de variaveis
model0 = glm(FANTASMA ~ 1, data=cands_agg, family="binomial")
# Modelo simples, sem intercepto
model1 = glm(FANTASMA ~ SIGLA_PARTIDO, data=cands_agg, family="binomial")
# Modelo simples, sem intercepto 
model1 = glm(FANTASMA ~ SIGLA_PARTIDO - 1, data=cands_agg, family="binomial")
# Diferencas de AIC dos modelos com um fator por vez:
# partido (ind); uf (+ uf nascimento); cargo; 
# idade (+ jovens + fantasmas); sexo (mulher + fantasma)
# escolaridade (detalhar); est. civil (+ solteiro / casado)
# cor/raça (+ parda, mt - indigena, amarela)

###########################################################################
# GLM
# Fazendo um modelo seriamente. Dividindo o conjunto entre test/train
cands_agg$train = sample(c(TRUE, FALSE), size=nrow(cands_agg), replace = TRUE, prob = c(0.8, 0.2))
train = subset(cands_agg, train)
test = subset(cands_agg, !train)
# Fazemos um modelo sobre o conjunto de train
model  = glm(FANTASMA ~ SIGLA_PARTIDO + SIGLA_UF + DESCRICAO_CARGO + IDADE_DATA_ELEICAO + DESCRICAO_SEXO + Escolaridade + Estado_Civil + Cor_Raca + DESPESA_MAX_CAMPANHA,  data = train, family="binomial")
# Simples ajuste:
predicted = predict(model, newdata=test, type='response')
# Tabela de confusão:
table((predicted>0.05), test$FANTASMA)
# Plot de ROC
pr = ROCR::prediction(predicted, test$FANTASMA)
plot(performance(pr, measure='tpr', x.measure='fpr'), main='Classificador para candidaturas fantasma', xlab='Taxa de falso positivo', ylab='Taxa de verdadeiro positivo')
abline(0,1, col="gray50", lty=3)
text(0.85,0.01,paste("AUC = ",format(performance(pr, measure='auc')@y.values[[1]], digits=2)))
