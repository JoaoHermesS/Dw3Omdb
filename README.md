# flask movie API

Esta é uma API desenvolvida com Flask e PostgreSQL que permite buscar filmes por título ou ID, consultando primeiro um banco de dados local e, se necessário, a API pública da OMDb (Open Movie Database).

## funcionalidades

- Busca de filmes por título
- Busca de filmes por ID IMDb
- Consulta ao banco de dados local
- Consulta externa à OMDb API quando o filme não é encontrado localmente
- Inserção automática no banco de dados após consulta à OMDb

## requisitos

- Python 3.x
- PostgreSQL
- Bibliotecas Python:
  - Flask
  - psycopg (nova versão do psycopg2)
  - requests

Instale as dependências com:

```bash
pip install flask psycopg requests
