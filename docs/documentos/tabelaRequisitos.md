| Rota               | Corpo                       | Resposta         | Autenticação | Validação de dados recebidos | Transações | Extra                        | Feito |
|--------------------|-----------------------------|------------------|--------------|-----------------------------|------------|------------------------------|-------|
| POST /products/    | Todos os atributos de produto | Any              | Admin        | ✓                           | ✓          |                              |    Sim   |
| GET /products/     | None                        | Todos os produtos| Any          | ✗                           | ✗          | Paginação, Ordenação, Filtragem |  Sim     |
| GET /products/{id} | None                        | Detalhes do produto identificado por {id} | Any | ✗           | ✗          |                              |  Sim     |
| PUT /products/{id} | Alguns atributos de produto | Any              | Admin        | ✓                           | ✓          |                              |    Sim   |
| DELETE /products/{id} | None                    | Any              | Admin        | ✗                           | ✗          |                              |   Sim    |


| Requisitos Extra              | Feito |
|-------------------------------|-------|
| Documentação (Swagger - Automático com fastAPI) |   Sim    |
| Logs com data/hora, usuário e dados | Sim |
| Testes de integração e unitários + cobertura e DB em memória |  |
