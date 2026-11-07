"""v0.4 acceptance checks. All PEY and OpenAI external calls are mocked."""
from pathlib import Path
import importlib.util, sys, json, base64, hashlib, hmac, time
from fastapi.testclient import TestClient
from test_pey_integracion import make_real, signed, stock, SECRET
from cart_intelligence import parse_cart, verified_cart_items


def demo_client(tmp_path, monkeypatch, one_cent=False):
    monkeypatch.setenv('TIENDITA_DB',str(tmp_path/'demo.db'))
    monkeypatch.delenv('PEY_ENABLE_LIVE',raising=False)
    monkeypatch.delenv('OPENAI_API_KEY',raising=False)
    if one_cent:monkeypatch.setenv('TIENDITA_TEST_ONE_CENT','1')
    else:monkeypatch.delenv('TIENDITA_TEST_ONE_CENT',raising=False)
    name='demo_v04_'+tmp_path.name
    spec=importlib.util.spec_from_file_location(name,Path(__file__).parent/'app.py')
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return TestClient(module.app)


def test_empleado_movil_y_dictado_con_revision(tmp_path, monkeypatch):
    c=demo_client(tmp_path, monkeypatch)
    assert c.get('/empleado').status_code==200
    assert 'App del empleado' in c.get('/empleado').text
    assert c.post('/api/employee/login',json={'name':'Ana'}).status_code==200
    p=c.get('/api/employee/bootstrap').json()['products']
    assert len(p)==8 and all('credit_limit_cents' not in x for x in p)
    r=c.post('/api/cart/parse',json={'text':'dos cocas y una leche y tres chicles'})
    assert r.status_code==200,r.text
    data=r.json()
    assert data['source']=='REGLAS'
    assert {(i['id'],i['qty']) for i in data['items']}=={('refresco',2),('leche',1)}
    assert data['unmatched']
    assert next(i['price_cents'] for i in data['items'] if i['id']=='refresco')==1900
    # No mutación al dictar: sólo propuesta.
    assert c.get('/api/bootstrap').json()['sales']==[]


def test_venta_centavo_diferencia_importe_y_no_inflar_caja(tmp_path, monkeypatch):
    c=demo_client(tmp_path, monkeypatch, True)
    s=c.post('/api/sales',json={'employee':'Ana','items':[{'id':'refresco','qty':2}]}).json()
    assert s['amount_cents']==3800 and s['charged_cents']==1
    assert c.get('/api/sales/'+str(s['id'])+'/status').json()['charged_cents']==1
    qr=c.post('/api/sales/'+str(s['id'])+'/qr').json()
    assert qr['amount_cents']==1
    assert c.post('/api/sales/'+str(s['id'])+'/demo-confirm').status_code==200
    report=c.get('/api/bootstrap').json()['totals']
    assert report['sales_cents']==0 and report['demo_sales_count']==1


def test_real_centavo_bancario_es_prueba_y_verificacion_adicional(tmp_path, monkeypatch):
    monkeypatch.setenv('TIENDITA_TEST_ONE_CENT','1')
    c,auth,mod=make_real(tmp_path,monkeypatch)
    original=stock(c,auth,'agua')
    s=c.post('/api/sales',headers=auth,json={'employee':'Ana','items':[{'id':'agua','qty':2}]}).json()
    assert (s['amount_cents'],s['charged_cents'])==(3000,1)
    qr=c.post(f'/api/sales/{s["id"]}/qr',headers=auth)
    assert qr.status_code==200
    assert qr.json()['amount_cents']==1
    tx='fake-transaccion-ulid-12345'
    evt={'type':'codi.qr.payment_received','amount':0.01,'codiQrId':qr.json()['qr_id'],
         'numRef':str(s['id']),'transactionId':tx,
         'metadata':{'externalMetadata':{'orderId':str(s['id'])}}}
    detail={'id':tx,'status':'PENDING','amount':0.01,'currency':'MXN',
            'paymentMethod':'CODI','payableType':'API_CODI_QR'}
    mod.pey.transaction=lambda _:detail
    body,headers=signed(evt,'wh_v04a')
    assert c.post('/webhooks/pey',content=body,headers=headers).status_code==409
    assert stock(c,auth,'agua')==original
    detail['status']='PAID';detail['currency']='USD'
    assert c.post('/webhooks/pey',content=body,headers=headers).status_code==409
    assert stock(c,auth,'agua')==original
    detail['currency']='MXN'
    r=c.post('/webhooks/pey',content=body,headers=headers)
    assert r.status_code==200,r.text
    assert r.json()['status']=='PAGADA_PRUEBA'
    assert stock(c,auth,'agua')==original-2
    assert c.post('/webhooks/pey',content=body,headers=headers).json()['duplicate']
    assert stock(c,auth,'agua')==original-2
    report=c.get('/api/bootstrap',headers=auth).json()['totals']
    assert report['sales_cents']==0 and report['test_pey_receipts_cents']==1


def test_empleado_en_live_ve_solo_lo_permitido(tmp_path,monkeypatch):
    c,auth,mod=make_real(tmp_path,monkeypatch)
    assert c.get('/api/employee/bootstrap').status_code==401
    assert c.post('/api/employee/login',json={'name':'Ana','pin':'INCORRECTO'}).status_code==401
    c.post('/api/employee/login',json={'name':'Ana','pin':'123456'}).raise_for_status()
    assert c.get('/api/employee/bootstrap').status_code==200
    assert c.get('/api/bootstrap').status_code==403
    assert c.post('/api/purchases',json={'product_id':'agua','quantity':3}).status_code==403
    s=c.post('/api/sales',json={'employee':'Luis','items':[{'id':'agua','qty':1}]}).json()
    # El servidor ignora el nombre de empleado suplido por el navegador.
    assert c.get(f'/api/sales/{s["id"]}/status').status_code==200
    assert c.get('/api/bootstrap',headers=auth).json()['sales'][0]['employee']=='Ana'


def test_openai_datos_no_autorizados_no_pueden_agregarse(tmp_path,monkeypatch):
    catalog=[{'id':'pan','name':'Pan de caja','price_cents':4500,'available':6}]
    items,unknown=verified_cart_items([{'id':'pan','qty':2},{'id':'telefono','qty':1}],catalog)
    assert items==[{'id':'pan','name':'Pan de caja','qty':2,'price_cents':4500,'available':6}]
    assert unknown==['telefono']
