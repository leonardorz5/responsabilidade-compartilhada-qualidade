\# Responsabilidade Compartilhada pela Qualidade



\## 1. Contexto



Este projeto apresenta um estudo de caso simulado sobre responsabilidade

compartilhada pela qualidade em uma equipe de desenvolvimento de software.



O cenário representa uma equipe responsável por uma aplicação de comércio

eletrônico. No modelo inicial, a identificação de defeitos é concentrada

principalmente no profissional de QA, fazendo com que problemas sejam

descobertos em etapas tardias do desenvolvimento.



A proposta do estudo é demonstrar como práticas de colaboração entre Produto,

Desenvolvimento, QA e DevOps podem antecipar a identificação de falhas e

incorporar qualidade ao próprio fluxo de desenvolvimento.



\---



\## 2. Problema



Em um modelo tradicional de desenvolvimento, é comum que o fluxo aconteça da

seguinte forma:



Desenvolvimento → QA → Correção → QA → Produção



Nesse cenário, a qualidade pode ser percebida como responsabilidade exclusiva

do QA.



Esse modelo tende a aumentar:



\- detecção tardia de defeitos;

\- retrabalho;

\- ciclos de correção;

\- tempo de feedback;

\- risco de defeitos chegarem à produção.



\---



\## 3. Objetivo



Demonstrar, por meio de um estudo de caso prático, como a responsabilidade

compartilhada pela qualidade pode antecipar a detecção de defeitos utilizando:



\- critérios de aceite;

\- testes automatizados;

\- integração contínua;

\- Pull Requests;

\- revisão antes da integração;

\- Quality Gates.



\---



\## 4. Regra de negócio utilizada



O projeto utiliza uma regra simples de cálculo de frete:



\- compras com valor igual ou superior a R$ 200 possuem frete grátis;

\- compras abaixo de R$ 200 possuem frete de R$ 20.



Implementação esperada:



```python

def calcular\_frete(valor\_compra):

&#x20;   if valor\_compra >= 200:

&#x20;       return 0



&#x20;   return 20

