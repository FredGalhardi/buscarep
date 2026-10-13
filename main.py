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
        resposta = supabase.table('republicas').select('*, faculdades(sigla), fotos(url)').eq('status', 'publicada').execute()
        for rep in resposta.data:
            fotos_urls = [foto['url'] for foto in rep.get('fotos', [])]
            if not fotos_urls:
                fotos_urls = ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3"]
                
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
            })
            
    return templates.TemplateResponse(request=request, name="explorar.html", context={"request": request, "republicas": republicas_formatadas})

# NOVA ROTA: O One-Pager da República
@app.get("/republica/{rep_id}", response_class=HTMLResponse)
async def pagina_republica(request: Request, rep_id: str):
    if supabase:
        resposta = supabase.table('republicas').select('*, faculdades(sigla, nome), fotos(url)').eq('id', rep_id).execute()
        if resposta.data:
            rep = resposta.data[0]
            fotos_urls = [foto['url'] for foto in rep.get('fotos', [])]
            if not fotos_urls:
                fotos_urls = ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3"]
            
            faculdade_sigla = rep.get('faculdades', {}).get('sigla', 'N/A') if rep.get('faculdades') else 'N/A'
            faculdade_nome = rep.get('faculdades', {}).get('nome', 'N/A') if rep.get('faculdades') else 'N/A'
            
            rep_formatada = {
                "id": rep["id"],
                "nome": rep["nome"],
                "fotos": fotos_urls,
                "vagas": rep["vagas_disponiveis"],
                "facilidades": rep.get("facilidades", []),
                "whatsapp": rep["whatsapp"],
                "bairro": rep["bairro"],
                "cidade": rep["cidade"],
                "endereco": rep["endereco"],
                "faculdade_sigla": faculdade_sigla,
                "faculdade_nome": faculdade_nome,
                "valor_medio": rep["valor_medio_aluguel"],
                "descricao": rep.get("descricao", "Sem descrição disponível.")
            }
            return templates.TemplateResponse(request=request, name="republica.html", context={"request": request, "rep": rep_formatada})
            
    return HTMLResponse(content="República não encontrada", status_code=404)
