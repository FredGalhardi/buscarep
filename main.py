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
    republicas_formatadas = []
    
    if supabase:
        # Puxa apenas repúblicas publicadas e traz as tabelas relacionadas (faculdades e fotos)
        resposta = supabase.table('republicas').select('*, faculdades(sigla), fotos(url)').eq('status', 'publicada').execute()
        
        for rep in resposta.data:
            # Organiza as fotos numa lista simples
            fotos_urls = [foto['url'] for foto in rep.get('fotos', [])]
            if not fotos_urls:
                fotos_urls = ["https://via.placeholder.com/800x400?text=Sem+Foto"]
                
            # Extrai a sigla da faculdade com segurança
            faculdade_sigla = rep.get('faculdades', {}).get('sigla', 'N/A') if rep.get('faculdades') else 'N/A'
            
            republicas_formatadas.append({
                "id": rep["id"],
                "nome": rep["nome"],
                "fotos": fotos_urls,
                "vagas": rep["vagas_disponiveis"],
                "facilidades": rep.get("facilidades", []),
                "whatsapp": rep["whatsapp"],
                "bairro": rep["bairro"],
                "cidade": rep["cidade"],
                "faculdade": faculdade_sigla,
                "valor_medio": rep["valor_medio_aluguel"],
                "descricao": "" # O novo plano técnico não inclui descrição, deixamos vazio para não quebrar o HTML
            })
            
    return templates.TemplateResponse(
        request=request, 
        name="explorar.html", 
        context={"request": request, "republicas": republicas_formatadas}
    )
