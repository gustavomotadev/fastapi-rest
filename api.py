from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from http import HTTPStatus
from repositorio import RepositorioDeArte as repositorio

LIMITE = 99999

class Estilo(BaseModel):
    nome: str

class Autor(BaseModel):
    nome: str
    ano_nascimento: int
    ano_falecimento: int
    pais_origem: str
    url_imagem: str

class Obra(BaseModel):
    titulo: str
    autor: int
    ano: int
    estilo: int
    material: str
    url_imagem: str

class URLImagem(BaseModel):
    url_imagem: str

app = FastAPI()

@app.get('/v1/obras')
async def get_obras(ano_inicial: int = -LIMITE, ano_final: int = LIMITE):
    if ano_inicial != -LIMITE or ano_final != LIMITE:
        return repositorio.listar_obras_por_periodo(ano_inicial, ano_final)
    else:
        return repositorio.listar_todas_obras()

@app.get('/v1/obra/{id}')
async def get_obra_id(id: int):
    encontrado = repositorio.obter_obra_por_id(id)
    if encontrado:
        return encontrado
    else:
        raise HTTPException(404, detail='Erro: obra não encontrada.')

@app.get('/v1/obras/{titulo}')
async def get_obras_titulo(titulo: str):
    return repositorio.obter_obras_por_titulo(titulo)

@app.get('/v1/autores')
async def get_autores():
    return repositorio.listar_todos_autores()

@app.get('/v1/autor/{id}')
async def get_autor_id(id: int):
    encontrado = repositorio.obter_autor_por_id(id)
    if encontrado:
        return encontrado
    else:
        raise HTTPException(404, detail='Erro: autor não encontrado.')

@app.get('/v1/autor/{nome}')
async def get_autor_nome(nome: str):
    encontrado = repositorio.obter_autor_por_nome(nome)
    if encontrado:
        return encontrado
    else:
        raise HTTPException(404, detail='Erro: autor não encontrado.')

@app.get('/v1/estilos')
async def get_estilos():
    return repositorio.listar_todos_estilos()

@app.get('/v1/estilo/{id}')
async def get_estilo_id(id: int):
    encontrado = repositorio.obter_estilo_por_id(id)
    if encontrado:
        return encontrado
    else:
        raise HTTPException(404, detail='Erro: estilo não encontrado.')

@app.get('/v1/estilo/{nome}')
async def get_estilo_nome(nome: str):
    encontrado = repositorio.obter_estilo_por_nome(nome)
    if encontrado:
        return encontrado
    else:
        raise HTTPException(404, detail='Erro: estilo não encontrado.')

@app.get('/v1/autor/{id}/obras')
async def get_obras_autor_id(id: int):
    encontrado = repositorio.obter_autor_por_id(id)
    if encontrado:
        return repositorio.listar_obras_por_id_autor(id)
    else:
        raise HTTPException(404, detail='Erro: autor não encontrado.')

@app.get('/v1/autor/{nome}/obras')
async def get_obras_autor_nome(nome: str):
    encontrado = repositorio.obter_autor_por_nome(nome)
    if encontrado:
        return repositorio.listar_obras_por_nome_autor(nome)
    else:
        raise HTTPException(404, detail='Erro: autor não encontrado.')

@app.get('/v1/estilo/{id}/obras')
async def get_obras_estilo_id(id: int):
    encontrado = repositorio.obter_estilo_por_id(id)
    if encontrado:
        return repositorio.listar_obras_por_id_estilo(id)
    else:
        raise HTTPException(404, detail='Erro: estilo não encontrado.')

@app.get('/v1/estilo/{nome}/obras')
async def get_obras_estilo_nome(nome: str):
    encontrado = repositorio.obter_estilo_por_nome(nome)
    if encontrado:
        return repositorio.listar_obras_por_nome_estilo(nome)
    else:
        raise HTTPException(404, detail='Erro: estilo não encontrado.')

@app.post('/v1/estilo', status_code=HTTPStatus.CREATED)
async def post_estilo(estilo: Estilo):
    sucesso = repositorio.inserir_estilo(estilo.nome)
    if sucesso:
        return {'Mensagem': 'Estilo inserido com sucesso.'}
    else: 
        raise HTTPException(400, detail='Erro: nome do Estilo deve ser único.')

@app.post('/v1/autor', status_code=HTTPStatus.CREATED)
async def post_autor(autor: Autor):
    sucesso = repositorio.inserir_autor(autor.nome, autor.ano_nascimento, autor.ano_falecimento, autor.pais_origem, autor.url_imagem)
    if sucesso:
        return {'Mensagem': 'Estilo inserido com sucesso.'}
    else: 
        raise HTTPException(400, detail='Erro: nome do Autor deve ser único.')

@app.post('/v1/obra', status_code=HTTPStatus.CREATED)
async def post_obra(obra: Obra):
    sucesso = repositorio.inserir_obra(obra.titulo, obra.autor, obra.ano, obra.estilo, obra.material, obra.url_imagem)
    if sucesso:
        return {'Mensagem': 'Obra inserida com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: ids de Autor e Estilo devem existir.')

@app.put('/v1/estilo/{id}')
async def put_estilo_id(id: int, estilo: Estilo):
    if not repositorio.obter_estilo_por_id(id):
        raise HTTPException(404, detail='Erro: estilo não encontrado.')
    sucesso = repositorio.editar_estilo_por_id(id, estilo.nome)
    if sucesso:
        return {'Mensagem': 'Estilo editado com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: nome do Estilo deve ser único.')

@app.put('/v1/estilo/{nome}')
async def put_estilo_nome(nome: str, estilo: Estilo):
    if not repositorio.obter_estilo_por_nome(nome):
        raise HTTPException(404, detail='Erro: estilo não encontrado.')
    sucesso = repositorio.editar_estilo_por_nome(nome, estilo.nome)
    if sucesso:
        return {'Mensagem': 'Estilo editado com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: nome do Estilo deve ser único.')

@app.put('/v1/autor/{id}')
async def put_autor_id(id: int, autor: Autor):
    if not repositorio.obter_autor_por_id(id):
        raise HTTPException(404, detail='Erro: Autor não encontrado.')
    sucesso = repositorio.editar_autor_por_id(id, autor.nome, autor.ano_nascimento, autor.ano_falecimento, autor.pais_origem, autor.url_imagem)
    if sucesso:
        return {'Mensagem': 'Autor editado com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: nome do Autor deve ser único.')

@app.put('/v1/autor/{nome}')
async def put_autor_nome(nome: str, autor: Autor):
    if not repositorio.obter_autor_por_nome(nome):
        raise HTTPException(404, detail='Erro: Autor não encontrado.')
    sucesso = repositorio.editar_autor_por_nome(nome, autor.nome, autor.ano_nascimento, autor.ano_falecimento, autor.pais_origem, autor.url_imagem)
    if sucesso:
        return {'Mensagem': 'Autor editado com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: nome do Autor deve ser único.')

@app.put('/v1/obra/{id}')
async def put_obra_id(id: int, obra: Obra):
    if not repositorio.obter_obra_por_id(id):
        raise HTTPException(404, detail='Erro: Obra não encontrada.')
    sucesso = repositorio.editar_obra_por_id(id, obra.titulo, obra.autor, obra.ano, obra.estilo, obra.material, obra.url_imagem)
    if sucesso:
        return {'Mensagem': 'Obra editada com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: ids de Autor e Estilo devem existir.')

@app.delete('/v1/estilo/{id}')
async def delete_estilo_id(id: int):
    if not repositorio.obter_estilo_por_id(id):
        raise HTTPException(404, detail='Erro: Estilo não encontrado.')
    sucesso = repositorio.remover_estilo_por_id(id)
    if sucesso:
        return {'Mensagem': 'Estilo removido com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: Estilo está sendo usado em obras.')

@app.delete('/v1/estilo/{nome}')
async def delete_estilo_nome(nome: str):
    if not repositorio.obter_estilo_por_nome(nome):
        raise HTTPException(404, detail='Erro: Estilo não encontrado.')
    sucesso = repositorio.remover_estilo_por_nome(nome)
    if sucesso:
        return {'Mensagem': 'Estilo removido com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: Estilo está sendo usado em obras.')

@app.delete('/v1/autor/{id}')
async def delete_autor_id(id: int):
    if not repositorio.obter_autor_por_id(id):
        raise HTTPException(404, detail='Erro: Autor não encontrado.')
    sucesso = repositorio.remover_autor_por_id(id)
    if sucesso:
        return {'Mensagem': 'Autor removido com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: Autor está sendo usado em obras.')

@app.delete('/v1/autor/{nome}')
async def delete_autor_nome(nome: str):
    if not repositorio.obter_autor_por_nome(nome):
        raise HTTPException(404, detail='Erro: Autor não encontrado.')
    sucesso = repositorio.remover_autor_por_nome(nome)
    if sucesso:
        return {'Mensagem': 'Autor removido com sucesso.'}
    else:
        raise HTTPException(400, detail='Erro: Autor está sendo usado em obras.')

@app.delete('/v1/obra/{id}')
async def delete_obra_id(id: int):
    sucesso = repositorio.remover_obra_por_id(id)
    if sucesso:
        return {'Mensagem': 'Obra removida com sucesso.'}
    else:
        raise HTTPException(404, detail='Erro: Obra não encontrada.')

@app.patch('/v1/autor/{id}')
async def patch_autor_url_id(id: int, url_imagem: URLImagem):
    sucesso = repositorio.alterar_imagem_autor_por_id(id, url_imagem.url_imagem)
    if sucesso:
        return {'Mensagem': 'URL de imagem do Autor alterada com sucesso.'}
    else:
        raise HTTPException(404, detail='Erro: Autor não encontrado.')

@app.patch('/v1/autor/{nome}')
async def patch_autor_url_nome(nome: str, url_imagem: URLImagem):
    sucesso = repositorio.alterar_imagem_autor_por_nome(nome, url_imagem.url_imagem)
    if sucesso:
        return {'Mensagem': 'URL de imagem do Autor alterada com sucesso.'}
    else:
        raise HTTPException(404, detail='Erro: Autor não encontrado.')

@app.patch('/v1/obra/{id}')
async def patch_obra_url_id(id: int, url_imagem: URLImagem):
    sucesso = repositorio.alterar_imagem_obra_por_id(id, url_imagem.url_imagem)
    if sucesso:
        return {'Mensagem': 'URL de imagem da Obra alterada com sucesso.'}
    else:
        raise HTTPException(404, detail='Erro: Obra não encontrada.')