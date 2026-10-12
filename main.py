from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client
import os

app = FastAPI(title="BuscaRep")

# Configuração da pasta de templates (HTML)
templates = Jinja2Templates(directory="templates")

# Chaves do Supabase (serão configuradas no alojamento)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

@app.get("/", response_class=HTMLResponse)
async def pagina_explorar(request: Request):
    # Dados fictícios para testar o ecrã inicial antes de ligar a base de dados
    republicas_teste = [
        {"nome": "República Teste 1", "bairro": "BPS", "preco_minimo": 600, "vagas": 2},
        {"nome": "República Teste 2", "bairro": "Centro", "preco_minimo": 850, "vagas": 0}
    ]
    
    return templates.TemplateResponse("explorar.html", {"request": request, "republicas": republicas_teste})
