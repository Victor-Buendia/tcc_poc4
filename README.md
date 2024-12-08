# Trabalho de Conclusão de Curso: PoC 4

Este repositório é fruto de um TCC com o foco de pesquisa sendo **"Um Estudo Exploratório Sobre Privacidade de Dados na Quarta Revolução Industrial"**.

# Pré Requisitos

O projeto precisa do Docker versão 26.1.4 ou superior e Docker Compose 2.27.0 ou superior para funcionar de maneira correta. Também é utilizado Node v.22.11.0 para a instalação da biblioteca Cartesi v1.5.

1. Instale o Docker e Docker Compose
2. Instale o Node
3. Instale a biblioteca [Cartesi v1.5](https://docs.cartesi.io/cartesi-rollups/1.5/quickstart/)
4. Clone o repositório

# Como Executar o Projeto

1. Execute `make build` para criar a imagem do projeto no Cartesi
2. Execute os seguintes comandos em ordem:
    ```bash
    make run-node     # Inicia o nó Cartesi
    make run-backend  # Inicia o backend da aplicação
    make run-server   # Inicia o frontend/API da aplicação
    ```

# Modo de Uso

Todos os códigos podem ser consultados no [Makefile](https://github.com/Victor-Buendia/tcc_poc4/blob/main/Makefile) do projeto, sendo o próprio código a documentação de seu uso. Para executar o pipeline completo, altere os valores de volume em [`docker.env`](https://github.com/Victor-Buendia/tcc_poc4/blob/main/docker.env) e execute `make pipeline`.

---
# Licença de Uso

A licença para uso e redistribuição deste material é [**ATRIBUIÇÃO-COMPARTILHAIGUAL 4.0 INTERNACIONAL**](https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br) (CC BY-SA 4.0) e pode ser encontrada em [LICENSE](https://github.com/Victor-Buendia/tcc_poc4?tab=MIT-1-ov-file) a versão específica e válida para este repositório.

O *software* não deve ser usado para atividades ilegais ou que violem a privacidade de dados de terceiros e é obrigatória a atribuição de crédito ao autor original, não sendo permitido plágio.

## Isenção de Responsabilidade

O *software* é fornecido "como está" (*as is*), sem garantia de qualquer tipo, expressa ou implícita, incluindo, mas não se limitando a, garantias de comercialização ou adequação a um propósito específico em sua implementação particular. Em nenhum caso o autor será responsável por qualquer dano decorrente do mal uso do *software*.