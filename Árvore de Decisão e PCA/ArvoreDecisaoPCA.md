# Atividade — PCA e Árvore de Decisão com o Dataset Iris

## Objetivo

Comparar como uma Árvore de Decisão identifica a importância direta de cada atributo e como o PCA sintetiza esses mesmos atributos em novos componentes.

Aplicar Análise de Componentes Principais (PCA) para reduzir a dimensionalidade de um conjunto de dados real e o modelo de Árvore de Decisão para seleção de atributos relevantes.

Utilizar o dataset Iris (disponível no `sklearn`), que possui apenas 4 atributos e 150 amostras, facilitando a visualização e a compreensão matemática da redução de dimensionalidade.

---

# Questões

## 1)

Observe o gráfico de barras.

Qual atributo a Árvore de Decisão considerou o mais importante para classificar as flores?

---

## 2)

No PCA, nós ainda conseguimos ver esse atributo específico no gráfico?

Explique a diferença entre:

- “Selecionar o melhor atributo”
- “Transformar os atributos em algo novo”

---

## 3)

Sobre Integração de Dados, existe outro tipo de redundância muito relevante em mineração, que é a situação na qual determinado objeto ou atributo pode ser obtido de um ou mais objetos ou atributos da base.

Por exemplo:

Em uma base de dados, o tempo de estudo de uma pessoa pode estar diretamente relacionado à sua titulação; quanto maior o tempo de estudo, maior sua titulação e vice-versa.

Se o PCA explicou uma variância muito alta (exemplo: > 90%) apenas com o PC1, o que isso nos diz sobre a correlação (redundância) entre as 4 medidas originais da flor?

---

## 4)

O PCA é considerado uma técnica de suavização de dados, pois remove “ruídos” de atributos menos significativos.

Olhando para o gráfico de dispersão, as classes de flores parecem:

- bem separadas
- ou misturadas?

Isso valida a eficácia da redução de dimensionalidade?

---

# Entrega

Enviar:

- Código utilizado
- Gráficos gerados
- Respostas das questões
- Breve conclusão sobre PCA e Árvore de Decisão