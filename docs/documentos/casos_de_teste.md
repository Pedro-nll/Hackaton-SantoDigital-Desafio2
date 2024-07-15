| Test Case | Rota                  | Descrição                                                                                      | Feito |
|-----------|-----------------------|------------------------------------------------------------------------------------------------|-------|
| TC1       | POST /products/       | Verificar se todos os atributos do produto podem ser salvos no banco de dados com a resposta correta |       |
| TC2       | POST /products/       | Verificar se apenas admin pode postar produtos                                                 |       |
| TC3       | POST /products/       | Validar os dados recebidos no corpo da solicitação                                             |       |
| TC4       | POST /products/       | Verificar resposta de erro ao postar produto com dados inválidos                               |       |
| TC5       | GET /products/        | Verificar se todos os produtos são recuperados com a resposta correta                          |       |
| TC6       | GET /products/        | Testar funcionalidade de paginação                                                             |       |
| TC7       | GET /products/        | Testar funcionalidade de ordenação                                                             |       |
| TC8       | GET /products/        | Testar funcionalidade de filtragem                                                             |       |
| TC9       | GET /products/{id}    | Verificar se os detalhes do produto para um ID específico são recuperados corretamente         |       |
| TC10      | GET /products/{id}    | Garantir que qualquer usuário pode acessar detalhes do produto pelo ID                         |       |
| TC11      | GET /products/{id}    | Verificar resposta de erro ao tentar recuperar um produto com ID inexistente                   |       |
| TC12      | PUT /products/{id}    | Verificar se alguns atributos do produto podem ser salvos no banco de dados com a resposta correta |       |
| TC13      | PUT /products/{id}    | Verificar se apenas admin pode atualizar produtos                                              |       |
| TC14      | PUT /products/{id}    | Validar os dados recebidos no corpo da solicitação                                             |       |
| TC15      | PUT /products/{id}    | Verificar resposta de erro ao tentar atualizar um produto com ID inexistente                   |       |
| TC16      | DELETE /products/{id} | Verificar se o produto pode ser deletado com a resposta correta                                |       |
| TC17      | DELETE /products/{id} | Verificar se apenas admin pode deletar produtos                                                |       |
| TC18      | DELETE /products/{id} | Verificar resposta de erro ao tentar deletar um produto com ID inexistente                     |       |
