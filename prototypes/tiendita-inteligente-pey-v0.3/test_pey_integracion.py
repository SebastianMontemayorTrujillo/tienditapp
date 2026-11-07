"""Integracion con PEY 100% simulada: ninguna red ni llave verdadera."""
import base64
import hashlib
import hmac
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from fastapi.testclient import TestClient

TOKEN='operador-test-token-1234567890-abc'
SECRET='whsec_'+base64.b64encode(b'secreto-sintetico-solo-pruebas-32').decode()


def make_real(tmp_path, monkeypatch):
    monkeypatch.setenv('TIENDITA_DB',str(tmp_path/'simulado.db'))
    monkeypatch.setenv('PEY_ENABLE_LIVE','1')
    monkeypatch.setenv('PEY_API_KEY','sk_test_FICTICIO_NO_EXISTE')
    monkeypatch.setenv('PEY_WEBHOOK_SECRET',SECRET)
    monkeypatch.setenv('TIENDITA_OPERATOR_TOKEN',TOKEN)
    monkeypatch.setenv('PEY_CONFIRM_REAL_MONEY','YES_I_AUTHORIZE')
    monkeypatch.setenv('TIENDITA_PUBLIC_URL','https://hackathon.invalid')
    name='tiendita_test_pay_'+tmp_path.name
    spec=importlib.util.spec_from_file_location(name,Path(__file__).parent/'app.py')
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    assert module.LIVE
    # Previene toda llamada externa aun si el endpoint se invoca por error.
    def qr(body):
        assert body['metadata']['orderId'].isdigit()
        assert isinstance(body['amount'],float)
        return {'id':'QR-FAKE-'+body['metadata']['kind']+'-'+body['numRef'],
                'qrString':'SIMULACION-COdi-QR-'+body['numRef']}
    def push(body):
        assert len(body['phoneNumber'])==10
        return {'transactionId':'TX-FAKE-'+body['metadata']['kind']+'-'+body['numRef'],
                'codiId':'12345678901234567890'}
    module.pey.create_qr=qr
    module.pey.create_push=push
    client=TestClient(module.app)
    auth={'x-tiendita-operator-key':TOKEN}
    return client, auth, module


def signed(payload, webhook_id):
    raw=json.dumps(payload,separators=(',',':')).encode()
    timestamp=str(int(time.time()))
    string=webhook_id+'.'+timestamp+'.'
    signature=base64.b64encode(hmac.new(base64.b64decode(SECRET[6:]),
                                             string.encode()+raw,hashlib.sha256).digest()).decode()
    return raw,{'webhook-id':webhook_id,'webhook-timestamp':timestamp,'webhook-signature':'v1,'+signature,'Content-Type':'application/json'}


def pay(client,payload,webhook_id):
    raw,headers=signed(payload,webhook_id)
    return client.post('/webhooks/pey',data=raw,headers=headers)


def stock(client,auth,id):
    return next(p['qty'] for p in client.get('/api/bootstrap',headers=auth).json()['products'] if p['id']==id)


def test_qr_real_mock_y_eventos_repetidos(tmp_path,monkeypatch):
    cl,auth,mod=make_real(tmp_path,monkeypatch)
    assert cl.get('/api/bootstrap').status_code==401
    original=stock(cl,auth,'agua')
    sale=cl.post('/api/sales',headers=auth,json={'employee':'Ana','items':[{'id':'agua','qty':2}]}).json()
    qr=cl.post(f'/api/sales/{sale["id"]}/qr',headers=auth)
    assert qr.status_code==200,qr.text
    assert qr.json()['mode']=='REAL'
    assert stock(cl,auth,'agua')==original
    assert cl.post(f'/api/sales/{sale["id"]}/qr',headers=auth).status_code==409
    payload={'type':'codi.qr.payment_received','codiQrId':qr.json()['qr_id'],
             'amount':30,'numRef':str(sale['id']),'transactionId':'REAL-TX-123',
             'metadata':{'externalMetadata':{'orderId':str(sale['id'])}}}
    bad_payload=dict(payload,amount=29.99)
    assert pay(cl,bad_payload,'wh_001').status_code==409
    assert stock(cl,auth,'agua')==original
    raw,headers=signed(payload,'wh_002')
    headers['webhook-signature']='v1,INVALID'
    assert cl.post('/webhooks/pey',data=raw,headers=headers).status_code==401
    assert stock(cl,auth,'agua')==original
    ok=pay(cl,payload,'wh_003')
    assert ok.status_code==200,ok.text
    assert stock(cl,auth,'agua')==original-2
    assert pay(cl,payload,'wh_003').json()['duplicate']
    assert pay(cl,payload,'wh_004').json()['duplicate']
    assert stock(cl,auth,'agua')==original-2


def test_push_venta_mock(tmp_path,monkeypatch):
    cl,auth,mod=make_real(tmp_path,monkeypatch)
    original=stock(cl,auth,'pan')
    sale=cl.post('/api/sales',headers=auth,json={'employee':'Luis','items':[{'id':'pan','qty':1}]}).json()
    assert cl.post(f'/api/sales/{sale["id"]}/push',headers=auth,json={'phone':'55123'}).status_code==422
    response=cl.post(f'/api/sales/{sale["id"]}/push',headers=auth,json={'phone':'5512345678'})
    assert response.status_code==200
    p={'type':'codi.pn.payment_received','amount':45,'numRef':str(sale['id']),
       'transactionId':'TX-FAKE-sale-'+str(sale['id']),
       'metadata':{'externalMetadata':{'orderId':str(sale['id'])}}}
    assert pay(cl,p,'wh_101').status_code==200
    assert stock(cl,auth,'pan')==original-1


def test_abono_fiado_qr_real_mock(tmp_path,monkeypatch):
    cl,auth,mod=make_real(tmp_path,monkeypatch)
    cid=cl.get('/api/bootstrap',headers=auth).json()['clients'][0]['id']
    sale=cl.post('/api/sales',headers=auth,json={'employee':'María','items':[{'id':'leche','qty':2}]}).json()
    assert cl.post(f'/api/sales/{sale["id"]}/credit',headers=auth,json={'client_id':cid}).status_code==200
    req=cl.post(f'/api/clients/{cid}/payment-requests',headers=auth,json={'amount_cents':2500,'method':'QR'})
    assert req.status_code==200,req.text
    r=req.json();assert r['mode']=='REAL' and r['qr_image']
    assert cl.get('/p/'+r['link'].split('/p/')[1]).status_code==200
    state=cl.get('/api/bootstrap',headers=auth).json()
    assert state['totals']['credit_outstanding_cents']==5600
    pr=next(x for x in state['payment_requests'] if x['id']==r['id'])
    p={'type':'codi.qr.payment_received','amount':25,'codiQrId':pr['pey_qr_id'],
       'numRef':str(r['id']),'transactionId':'QR-CREDIT-PAID-00001',
       'metadata':{'externalMetadata':{'orderId':str(r['id'])}}}
    assert pay(cl,p,'wh_301').status_code==200
    assert cl.get('/api/bootstrap',headers=auth).json()['totals']['credit_outstanding_cents']==3100
    assert pay(cl,p,'wh_302').json()['duplicate']
    assert cl.get('/api/bootstrap',headers=auth).json()['totals']['credit_outstanding_cents']==3100


def test_abono_fiado_push_mock(tmp_path,monkeypatch):
    cl,auth,mod=make_real(tmp_path,monkeypatch)
    user=cl.post('/api/clients',headers=auth,json={'name':'Cliente Simulado','phone':'5512345678','credit_limit_cents':50000}).json()
    sale=cl.post('/api/sales',headers=auth,json={'employee':'Ana','items':[{'id':'cafe','qty':1}]}).json()
    assert cl.post(f'/api/sales/{sale["id"]}/credit',headers=auth,json={'client_id':user['id']}).status_code==200
    r=cl.post(f'/api/clients/{user["id"]}/payment-requests',headers=auth,
              json={'amount_cents':5000,'method':'PUSH'}).json()
    assert r['method']=='PUSH' and r['mode']=='REAL'
    p={'type':'codi.pn.payment_received','amount':50,'numRef':str(r['id']),
       'transactionId':'TX-FAKE-credit-'+str(r['id']),
       'metadata':{'externalMetadata':{'orderId':str(r['id'])}}}
    assert pay(cl,p,'wh_401').status_code==200
    assert cl.get('/api/bootstrap',headers=auth).json()['totals']['credit_outstanding_cents']==3500


def test_webhook_firma_y_monto_exactos():
    from pey_gateway import verify_standard_webhook,money_to_cents
    assert money_to_cents('19.99')==1999
    assert money_to_cents(0.01)==1
    for x in (float('nan'),float('inf'),-1,1.001,None,True):
        try:money_to_cents(x);assert False,'debio fallar'
        except ValueError:pass
    raw,head=signed({'type':'prueba'},'whtest')
    assert verify_standard_webhook(head,raw,SECRET)
    assert not verify_standard_webhook(head,raw+b' ',SECRET)
    h=dict(head);h['webhook-timestamp']='1'
    assert not verify_standard_webhook(h,raw,SECRET)


def test_modo_real_no_activa_sin_confirmacion(tmp_path,monkeypatch):
    cl,auth,mod=make_real(tmp_path,monkeypatch)
    monkeypatch.delenv('PEY_CONFIRM_REAL_MONEY')
    spec=importlib.util.spec_from_file_location('blocked_app',Path(__file__).parent/'app.py')
    m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    assert not m.LIVE and m.CONFIG_BLOCKED
    c=TestClient(m.app)
    assert c.get('/api/health').json()['mode']=='BLOQUEADO'
    sale=c.post('/api/sales',json={'employee':'Ana','items':[{'id':'agua','qty':1}]}).json()
    assert c.post(f'/api/sales/{sale["id"]}/qr').status_code==503
