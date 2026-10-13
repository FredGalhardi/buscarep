from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client
import os

app = FastAPI(title="BuscaRep")
templates = Jinja2Templates(directory="templates")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

# Base de dados fictícia enriquecida
republicas_teste = [
    {
        "id": 1,
        "nome": "República Teste 1", 
        "cidade": "Itajubá",
        "bairro": "BPS", 
        "preco_minimo": 600, 
        "vagas": 2,
        "foto_capa": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "descricao": "República tradicional, ambiente focado nos estudos durante a semana e descontraído no final de semana. Fica muito perto da Unifei.",
        "comodidades": ["Internet 500MB", "Faxineira 2x/semana", "Máquina de Lavar", "Garagem"],
        "quarto": "Quarto duplo partilhado, mobilado com cama, secretária e roupeiro."
    },
    {
        "id": 2,
        "nome": "República Teste 2", 
        "cidade": "Itajubá",
        "bairro": "Centro", 
        "preco_minimo": 850, 
        "vagas": 0,
        "foto_capa": "https://images.unsplash.com/photo-1502672260266-1c1de2d9d0cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "descricao": "República mista no centro da cidade, perto de supermercados e da paragem de autocarro para a faculdade.",
        "comodidades": ["Internet 300MB", "TV por Cabo", "Cozinha Completa", "Varanda"],
        "quarto": "Quarto individual amplo e bem arejado."
    }
]

@app.get("/", response_class=HTMLResponse)
async def pagina_explorar(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="explorar.html", 
        context={"request": request, "republicas": republicas_teste}
    )

# NOVA ROTA: Quando o utilizador clica numa república
@app.get("/republica/{rep_id}", response_class=HTMLResponse)
async def pagina_republica(request: Request, rep_id: int):
    # Procura a república pelo ID
    rep_encontrada = next((rep for rep in republicas_teste if rep["id"] == rep_id), None)
    
    if not rep_encontrada:
        return HTMLResponse(content="República não encontrada", status_code=404)
        
    return templates.TemplateResponse(
        request=request, 
        name="republica.html", 
        context={"request": request, "rep": rep_encontrada}
    )
