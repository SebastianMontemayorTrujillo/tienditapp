"""Converts Spanish point-of-sale dictation to a *proposal* for a cart.
Never computes or invents prices. AI is optional and validated against the catalog.
"""
from __future__ import annotations
import json, os, re, unicodedata, urllib.request

WORDS = {'un':1,'uno':1,'una':1,'dos':2,'tres':3,'cuatro':4,'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9,'diez':10}
ALIASES = {
 'leche': ['leche','leches','litro de leche'],
 'pan': ['pan','panes','pan de caja'],
 'huevo': ['huevo','huevos','docena de huevos','docenas'],
 'agua': ['agua','aguas','botella de agua'],
 'refresco': ['refresco','refrescos','coca','cocas','coca cola','coca-cola'],
 'arroz': ['arroz','kilo de arroz'],
 'cafe': ['cafe','café','café molido'],
 'yogur': ['yogur','yogurt','yogures'],
}

def norm(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(text).lower()) if not unicodedata.combining(c)).replace('-', ' ')

def verified_cart_items(candidates, catalog):
    by_id = {p['id']:p for p in catalog}
    selected = {}
    unmatched = []
    for item in candidates:
        id_ = item.get('id')
        try: qty = int(item.get('qty', 0))
        except (ValueError, TypeError): qty = 0
        if id_ not in by_id or qty < 1 or qty > 100:
            unmatched.append(str(item.get('label') or id_ or 'Producto desconocido')[:120]); continue
        selected[id_] = selected.get(id_, 0) + qty
    return [{'id':id_,'name':by_id[id_]['name'],'qty':qty,
             'price_cents':by_id[id_]['price_cents'], 'available':by_id[id_]['available']}
            for id_, qty in selected.items()], unmatched

def rule_parse(text, catalog):
    text=norm(text).strip()
    # Boundaries protect e.g. "pan" from matching a longer product identifier.
    phrases=[]
    for p in catalog:
        names=ALIASES.get(p['id'], [])+[p['name']]
        for name in names:
            phrase=norm(name)
            if len(phrase)>=3: phrases.append((phrase,p['id']))
    phrases.sort(key=lambda x:len(x[0]),reverse=True)
    candidates=[]; left=text
    found=[]
    for name,id_ in phrases:
        pat=r'(?<!\w)(?:(?P<qty>\d{1,3}|'+ '|'.join(WORDS)+r')\s+)?(?P<name>'+re.escape(name)+r')(?!\w)'
        for m in list(re.finditer(pat,left)):
            if any(not(m.end()<=start or m.start()>=end) for start,end in found):continue
            q=m.group('qty') or '1'
            candidates.append({'id':id_,'qty':WORDS.get(q,q),'label':name})
            found.append((m.start(),m.end()))
    residual=list(left)
    for start,end in found:
        for i in range(start,end):residual[i]=' '
    remainder=re.sub(r'\b(y|con|mas|por|favor|quiero|dame|me|das|de|la|el|los|las|unas|unos|al|una|un|para|llevar|porfa)\b', ' ', ''.join(residual))
    remainder=' '.join(remainder.split()).strip(' ,.;')
    items,unmatched=verified_cart_items(candidates,catalog)
    if remainder: unmatched.append(remainder[:120])
    return {'items':items,'unmatched':unmatched,'source':'REGLAS','text':text}

def openai_parse(text, catalog):
    key=os.getenv('OPENAI_API_KEY','')
    if not key: return None
    model=os.getenv('OPENAI_CART_MODEL','gpt-4o-mini')
    allowed=[{'id':p['id'],'name':p['name'],'aliases':ALIASES.get(p['id'],[])} for p in catalog]
    task=('Eres un parser de pedidos de tienda en español de México. Devuelve SOLO JSON '
          'con la forma {"items":[{"id":"id_catalogo","qty":2}],"unmatched":["texto"]}. '
          'Usa únicamente ID del catálogo. NO inventes productos o precios. '
          'Si hay ambigüedad pon el texto en unmatched. Cantidades de 1 a 100. '
          'El empleado revisará la propuesta antes de cobrar.')
    payload={'model':model,'instructions':task,'input':json.dumps({'dictado':text,'catalogo':allowed},ensure_ascii=False),
             'text':{'format':{'type':'json_object'}},'store':False}
    req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(payload).encode('utf-8'),
                               headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=12) as resp:
        answer=json.load(resp)
    output=''.join(e.get('text','') for block in answer.get('output',[]) for e in block.get('content',[]) if e.get('type')=='output_text')
    parsed=json.loads(output)
    if not isinstance(parsed,dict) or not isinstance(parsed.get('items'),list) or not isinstance(parsed.get('unmatched'),list):
        raise ValueError('Respuesta IA sin estructura válida')
    items,unknown=verified_cart_items(parsed['items'],catalog)
    return {'items':items,'unmatched':(unknown+[str(x)[:120] for x in parsed['unmatched']])[:15],
            'source':'OPENAI','text':text}

def parse_cart(text,catalog):
    if not isinstance(text,str) or not (1 <= len(text.strip()) <= 500):
        raise ValueError('Escribe entre 1 y 500 caracteres')
    if os.getenv('OPENAI_API_KEY'):
        return openai_parse(text,catalog)
    return rule_parse(text,catalog)
