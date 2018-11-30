# PSE - Image

## Introdução
Problem Solving Environment (PSE)  é um software de computador completo, integrado e especializado 
para resolver uma classe de problemas, combinando métodos automatizados de solução de problemas com 
ferramentas orientadas para humanos, para orientar a resolução de problemas. Um PSE também pode ajudar 
os usuários na formulação de resolução de problemas, na seleção de algoritmos, simulação de valores numéricos 
e na visualização e análise de resultados.  

Este Problem Solving Environment (PSE), possui como proposta a implementação de um software utilizando a 
terceira versão da linguagem de programação python. Tem-se o objetivo de demonstrar, através de uma interface 
amigável e pelo uso do conceito de fluxo de dados, a aplicação de variados processos envolvendo o processamento 
de imagens, podendo este ser definido como "qualquer forma de processamento de dados que apresentam entradas e 
saídas no formato de imagens“. 

Para esse trabalho foram implementados a interpolação pelo vizinho mais próximo, plotagem de histogramas, e 
filtros passa-baixa, passa-alta e morfológicos, com o uso de máscaras de convolução nos formatos (3x3. 5x5, 7x7. 
9x9, 11x11). No total, foram implementados na primeira versão do programa 12 filtros, sendo 3 deles passa-baixa (média
mediana e gaussiano), 4 passa-alta (laplaciano, laplaciano do gaussiano, prewitt, roberts e sobel) e 4 morfológicos
(erosão e dilatação, bem como abertura e fechamento).

## Conceitos Aplicados
A seguir esclarecemos os principais conceitos implementados.

### Interpoladores
Permitem um aumento artificial da resolução das imagens, ao adicionar pixels de cores intermediárias entre 
os já existentes. Com isto é possível evitar que os pixels da imagem “estourem” ao ampliar/esticar uma imagem 
de baixa resolução entretanto este processo não aumenta o detalhamento das imagens.

#### Interpolador Vizinho Mais Próximo
A Interpolação pelo vizinho mais próximo é um método de interpolação determinista no qual o valor estimado é sempre 
igual à sua amostra mais próxima não considerando qualquer outra. Dada a sua simplicidade é regularmente utilizado 
para interpolações rápidas e em áreas de estudo bem amostradas. 

Para cada localização a ser interpolada deverá ser calculado a distância de todos os pontos amostrais a essa mesma 
localização e determinar qual deles terá a distância mínima sendo o valor correspondente a interpolação. Sendo (x0 , y0) 
as amostra é feita o cálculo da distância.

    Parâmetro: Ampliação/Redução: 0.10 / 0.50


## Desenvolvedores
Gabriel Luciano Gomes  
Geovane Fonseca de Souza Santos  
Luigi Domenico Cecchini Soares  
Saul Gustavo Caldeira Melo  
