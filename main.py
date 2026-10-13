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

@app.get("/", response_class=HTMLResponse)
async def pagina_explorar(request: Request):
    
    republicas_mock = [
        {
            "id": 1,
            "nome": "República Teste 1",
            "descricao": "Ambiente tranquilo, ideal para quem quer focar nos estudos.",
            "fotos": [
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            ],
            "vagas": 2,
            "facilidades": ["Wi-Fi", "Mobiliado", "Lavanderia"],
            "whatsapp": "5512982588993", # SEU WHATSAPP AQUI
            "bairro": "BPS",
            "cidade": "Itajubá",
            "faculdade": "UNIFEI",
            "valor_medio": 650
        },
        {
            "id": 2,
            "nome": "República Teste 2",
            "descricao": "Casa grande, galera animada e bem perto do portão principal.",
            "fotos": [
                "https://images.unsplash.com/photo-1502672260266-1c1de2d9d0cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            ],
            "vagas": 0,
            "facilidades": ["Garagem", "Cozinha equipada", "Quintal"],
            "whatsapp": "5512982588993", # SEU WHATSAPP AQUI TAMBÉM
            "bairro": "Centro",
            "cidade": "Lavras",
            "faculdade": "UFLA",
            "valor_medio": 800
        }
    ]
    
    return templates.TemplateResponse(
        request=request, 
        name="explorar.html", 
        context={"request": request, "republicas": republicas_mock}
    )
