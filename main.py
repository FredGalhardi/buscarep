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
async def pagina_explorar(request: Request, filtro_cidade: str = "", filtro_faculdade: str = ""):
    republicas_formatadas = []
    cidades_unicas = []
    faculdades_unicas = []
    
    if supabase:
        # Puxa todas as repúblicas publicadas
        resposta = supabase.table('republicas').select('*, faculdades(sigla), fotos(url)').eq('status', 'publicada').execute()
        dados = resposta.data
        
        # Filtra via Python para evitar erros de SQL complexos
        if filtro_cidade:
            dados = [r for r in dados if r.get('cidade') == filtro_cidade]
        if filtro_faculdade:
            dados = [r for r in dados if r.get('faculdades', {}).get('sigla') == filtro_faculdade]
            
        for rep in dados:
            fotos_urls = [foto['url'] for foto in rep.get('fotos', [])]
            if not fotos_urls:
                fotos_urls = ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3"]
                
            republicas_formatadas.append({
                "id": rep["id"],
                "nome": rep["nome"],
                "fotos": fotos_urls,
                "vagas": rep["vagas_disponiveis"],
                "facilidades": rep.get("facilidades", []),
                "whatsapp": rep["whatsapp"],
                "bairro": rep["bairro"],
                "cidade": rep["cidade"],
                "faculdade": rep.get('faculdades', {}).get('sigla', 'N/A') if rep.get('faculdades') else 'N/A',
                "valor_medio": rep["valor_medio_aluguel"],
            })
            
        # Extrai listas únicas para popular os menus (Dropdowns) do HTML
        todas_reps = resposta.data
        cidades_unicas = sorted(list(set(r.get('cidade') for r in todas_reps if r.get('cidade'))))
        faculdades_unicas = sorted(list(set(r.get('faculdades', {}).get('sigla') for r in todas_reps if r.get('faculdades'))))
            
    return templates.TemplateResponse(request=request, name="explorar.html", context={
        "request": request, 
        "republicas": republicas_formatadas,
        "cidades": cidades_unicas,
        "faculdades": faculdades_unicas,
        "filtro_cidade": filtro_cidade,
        "filtro_faculdade": filtro_faculdade
    })

@app.get("/republica/{rep_id}", response_class=HTMLResponse)
async def pagina_republica(request: Request, rep_id: str):
    if supabase:
        resposta = supabase.table('republicas').select('*, faculdades(sigla, nome), fotos(url)').eq('id', rep_id).execute()
        if resposta.data:
            rep = resposta.data[0]
            fotos_urls = [foto['url'] for foto in rep.get('fotos', [])]
            if not fotos_urls:
                fotos_urls = ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3"]
            
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
                "faculdade_sigla": rep.get('faculdades', {}).get('sigla', 'N/A') if rep.get('faculdades') else 'N/A',
                "faculdade_nome": rep.get('faculdades', {}).get('nome', 'N/A') if rep.get('faculdades') else 'N/A',
                "valor_medio": rep["valor_medio_aluguel"],
                "descricao": rep.get("descricao", "Sem descrição disponível.")
            }
            return templates.TemplateResponse(request=request, name="republica.html", context={"request": request, "rep": rep_formatada})
            
    return HTMLResponse(content="República não encontrada", status_code=404)
