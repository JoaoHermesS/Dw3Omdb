from flask import Flask, request, jsonify
import psycopg
import requests

app = Flask(__name__)

db_conn = psycopg.connect("dbname=tralalero user=postgres password=3f@db host=164.90.152.205 port=80")

@app.route("/requisicao/<tipo>", methods=["POST"])
def sender(tipo):

    dado = request.get_json()
    informacao = dado.get('informacao') 

    if tipo == 'titulo':
        procurar_por_titulo(informacao)
    else:
        procurar_por_id(informacao)

@app.route('/filme/nome', methods=['GET'])
def procurar_por_titulo(titulo):
    lista_filmes = []
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM filmes WHERE titulo ILIKE %s", (f"%{titulo}%",)) 
        resultado_query = cursor.fetchall() 

        if resultado_query: 

            for item in resultado_query:
                lista_filmes.append({ 
                    "id": item[0],
                    "imdb_id": item[1],
                    "titulo": item[2],
                    "ano": item[3],
                    "tipo": item[4]
                })

            return jsonify({ 
                "mensagem": f"{len(lista_filmes)} filme(s) localizado(s).",
                "filmes": lista_filmes
            })


        resposta_api = requests.get(f"http://www.omdbapi.com/?apikey=58cc3cb5&t={titulo}")
        if resposta_api.status_code == 200:
            dados_filme = resposta_api.json()

            if dados_filme.get('Response') == 'True': 
                cursor.execute("""
                    INSERT INTO filmes_series (
                    imdb_id, titulo, tipo, ano,
                    nota, lancamento, duracao, genero,
                    diretor, escritores, sinopse, linguagem,
                    pais, premiacoes, poster, metascore,
                    imdbrating, imdbvotes
                ) VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s
                )
                """,
                (
                    
                    dados_filme['imdbId'], dados_filme['Title'], dados_filme['Type'], dados_filme['Year'],
                    dados_filme['Rated'], dados_filme['Released'], dados_filme['Runtime'], dados_filme['Genre'],
                    dados_filme['Director'], dados_filme['Writer'], dados_filme['Plot'], dados_filme['Language'],
                    dados_filme['Country'], dados_filme['Awards'], dados_filme['Metascore'],
                    dados_filme['imdbRating'], dados_filme['imdbVotes']
                )
                )
                db_conn.commit()
                return jsonify({ 
                    "mensagem": "Filme obtido da OMDb e gravado no banco.",
                    "filme": {
                        "imdb_id": dados_filme['imdbID'],
                        "titulo": dados_filme['Title'],
                        "ano": dados_filme['Year'],
                        "tipo": dados_filme['Type']
                    }
                });

@app.route('/filme/id', methods=['GET'])
def procurar_por_id(codigo):
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM filmes WHERE imdb_id = %s", (codigo))
        filme_encontrado = cursor.fetchone()

        if filme_encontrado:
            return jsonify({
                "mensagem": "Filme localizado no banco de dados.",
                "filme": {
                    "id": filme_encontrado[0],
                    "imdb_id": filme_encontrado[1],
                    "titulo": filme_encontrado[2],
                    "ano": filme_encontrado[3],
                    "tipo": filme_encontrado[4]
                }
            })

        resposta_api = requests.get(f"http://www.omdbapi.com/?apikey=58cc3cb5&t={codigo}")
        if resposta_api.status_code == 200:
            dados_filme = resposta_api.json()

            if dados_filme.get('Response') == 'True':
                cursor.execute("""
                    INSERT INTO filmes_series (
                    imdb_id, titulo, tipo, ano,
                    nota, lancamento, duracao, genero,
                    diretor, escritores, sinopse, linguagem,
                    pais, premiacoes, poster, metascore,
                    imdbrating, imdbvotes
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s
                )
                """,
                (
                    dados_filme['imdbId'], dados_filme['Title'], dados_filme['Type'], dados_filme['Year'],
                    dados_filme['Rated'], dados_filme['Released'], dados_filme['Runtime'], dados_filme['Genre'],
                    dados_filme['Director'], dados_filme['Writer'], dados_filme['Plot'], dados_filme['Language'],
                    dados_filme['Country'], dados_filme['Awards'], dados_filme['Metascore'],
                    dados_filme['imdbRating'], dados_filme['imdbVotes']
                )
                )
                db_conn.commit()
                return jsonify({
                    "mensagem": "Filme obtido da OMDb e gravado no banco.",
                    "filme": {
                        "imdb_id": dados_filme['imdbID'],
                        "titulo": dados_filme['Title'],
                        "ano": dados_filme['Year'],
                        "tipo": dados_filme['Type']
                    }
                });
