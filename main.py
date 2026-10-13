from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client
import os

app = FastAPI(title="BuscaRep")
templates = Jinja2Templates(directory="templates")

# 👉 ATENÇÃO AQUI 1: Quando formos ligar o banco real, estas chaves vão conectar ao Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

@app.get("/", response_class=HTMLResponse)
async def pagina_explorar(request: Request):
    
    # 👉 ATENÇÃO AQUI 2: No futuro, vamos apagar este bloco e fazer: 
    # republicas = supabase.table('republicas').select('*').execute()
    
    republicas_mock = [
        {
            "id": 1,
            "nome": "República Teste 1",             # 1. Nome
            "descricao": "Ambiente tranquilo, ideal para quem quer focar nos estudos.", # 2. Descrição pequena
            "fotos": [                               # 3. Fotos (a primeira é a capa)
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            ],
            "vagas": 2,                              # 4. Qtde vagas
            "facilidades": ["Wi-Fi", "Mobiliado", "Lavanderia"], # 5. Facilidades
            "whatsapp": "5535999999999",             # 6. Contato (número limpo para o link wa.me)
            "bairro": "BPS",                         # 7. Endereço (bairro público)
            "cidade": "Itajubá",
            "faculdade": "UNIFEI",                   # 8. Faculdade
            "valor_medio": 650                       # 9. Valor médio
        },
        {
            "id": 2,
            "nome": "República Teste 2",
            "descricao": "Casa grande, galera animada e bem perto do portão principal.",
            "fotos": [
                "https://images.unsplash.com/photo-1502672260266-1c1de2d9d0cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            ],
            "vagas": 0, # Sem vagas para testarmos o visual
            "facilidades": ["Garagem", "Cozinha equipada", "Quintal"],
            "whatsapp": "5535888888888",
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
