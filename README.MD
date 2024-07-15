# Introdução
Este repositório contém minha solução para o Desafio 2 do hackathon da Santo Digital em parceria com a PUC Minas. 

## Organização dos artefatos
Os dados, documentos e imagens se encontram na pasta docs. Dentro dela, a pasta Data contém os arquivos referentes ao banco de dados fornecido. A pasta images e documentos contém imagens e arquivos auxiliares utilizados para compor este README. Além disso, está presente em docs um arquivo JSON que pode ser importado para o Postman com requests para teste da API. 
A aplicação toda se encontra na pasta "app". Dentro dela temos o arquivo "main.py" que instancia a aplicação e diversas pastas:
- config: Configurações relacionadas ao token JWT
- entities: classes das entidades relevantes ao contexto do problema
- interfaces/repositories: interfaces utilizadas para a inversão de dependência entre a camada de persistência e as entidades
- interfaces/usecases: interfaces utilizadas para a inversão de dependência entre a camada externa e a camada lógica da aplicação
- repositories/sqlite: implementação das interfaces de repositório utilizando o SQLite
- routers: camada externa da aplicação que ouve as chamadas HTTP e direciona elas propriamente
- schemas: classes para a validação de dados de entrada e saída utilizando o pydantic
- usecases: implementação da lógica da aplicação 

## Tecnologias utilizadas
- FastAPI
- Pydantic
- SQLite
- pyjwt/passlib

## Premissas
Na parte 3 do desafio é requisitada a seguinte porta:

> Rota 4: GET /sales/top-sellers
> Retorna os vendedores que tiveram vendas com valor acima da média no último ano fiscal

Porém, no banco de dados fornecido (https://www.kaggle.com/datasets/ukveteran/adventure-works?select=AdventureWorks_Territories.csv) não há informações sobre "vendedores". Portanto, assumi que vendedores se refiriam aos territórios de venda.

## Meu passo a passo
Ao iniciar o projeto, dediquei-me primeiramente à compreensão dos requisitos da aplicação. Organizei o que foi pedido em uma tabela para facilitar o acompanhamento das tarefas e do progresso durante o desenvolvimento. Priorizei inicialmente as partes 1 e 2 do desafio, dado que a parte 3 dependia das entidades definidas nas etapas anteriores. Além disso, esbocei alguns casos de teste simples, que poderiam ser realizados manualmente para visualizar se a aplicação estava de acordo com o esperado.
[Link para a Tabela de Requisitos](./docs/documentos/tabelaRequisitos.md)
[Link para a Tabela com casos de teste](./docs/documentos/casos_de_teste.md)

Após entender o contexto do problema, baixei os dados fornecidos do banco de dados e converti para CSV, tornando mais fácil o uso nos scripts Python para a inicialização de dados no BD. Organizei um esboço das entidades e seus atributos, além de um Diagrama de Entidade-Relacionamento para entender melhor as relações entre elas.
[Link para o esboço das entidades](./docs/Images/Models.png)
[Link para o esboço das entidades](./docs/Images/DER.png)

Optei por implementar a arquitetura limpa, uma escolha motivada pela manutenção e evolução de software e por ser um tópico que tenho estudado recentemente, sendo uma ótima oportunidade para colocar em prática o que vi em teória. Esta arquitetura separa claramente as camadas da aplicação, protegendo as entidades do domínio e desacoplando a lógica de negócios e a persistência de dados através de interfaces. Como as entidades definem o contexto do problema, elas se tornam o centro da aplicação e o ponto de maior "proteção". Ou seja, elas não importam nem herdam nada externo a elas. Assim, a aplicação se torna mais extendível e ao não adotar as "opniões" que essas ferramentas externas trazem a aplicação é possível adicionar/trocar componentes com menos custos. [Link para um diagrama da arquitetura](./docs/Images/Arquitetura.png)

Diante desse cenário, para utilizar a camada de persistência na aplicação sem depender de suas implementações, criei interfaces de repositório. Essas interfaces estão definidas em "./app/interfaces/repositories/" e contem a definição dos métodos necessários a serem realiazados nas tabelas de cada entidade da aplicação. A implementação dessas interfaces utilizando o SQLite se encontra em "./app/repositories". Nas quais, além das funções das respectivas interfaces, são inicializadas as tabelas de cada entidades e uma função para a implementação das transações. 

Na camada lógica da aplicação, adaptei ligeiramente a arquitetura limpa tradicional. Ao invés de criar uma interface de caso de uso para cada caso de uso, criei uma interface de casos de uso por entidade, o que se aproxima da camada de "services" de arquiteturas como a MVC. Como as tecnologias utilizadas nesse desafio são mais voltadas para o desenvolvimento rápido de aplicações, considerei que os custos e benéficios da minha implementação e julguei que valeria a pena para este projeto, considerando o tempo para desenvolvimento da solução, sua vida útil e sua complexidade. Essas interfaces estão definidas em "./app/interfaces/usecases/".

A implementação das interfaces de caso de uso se encontra em "./app/usecases". As classes ali presentes são injetadas com instâncias das interfaces de repositórios em sua inicialização. Com isso, a lógica da aplicação passa a depender apenas das interfaces, e não das implementações delas, isso faz com que a interface de repositório se torne um ponto de extensão da aplicação e seja possível adotar diversas aplicações, caso necessário, sem custo extra. 

Por último, os roteadores em "./app/routers/" são responsáveis pela camada externa da aplicação, lidando com as requisições HTTP e direcionando-as para os casos de uso apropriados. As classes ali presentes são injetadas com as interfaces de caso de uso. Além disso, elas utilizam as classes definidas em "./app/schemas" para a validação de dados com o pydantic. 

Com a arquitetura definida, avancei para a implementação em código.