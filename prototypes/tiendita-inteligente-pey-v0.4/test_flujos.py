"""Pruebas de los flujos de hackathon; siempre usa una base temporal y sin PEY LIVE."""
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def make_client(tmp_path):
    os.environ['TIENDITA_DB'] = str(tmp_path/'test.db')
    os.environ.pop('PEY_ENABLE_LIVE',None)
    os.environ.pop('PEY_API_KEY',None)
    os.environ.pop('PEY_WEBHOOK_SECRET',None)
    spec=importlib.util.spec_from_file_location('tiendita_test_'+tmp_path.name,Path(__file__).parent/'app.py')
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return TestClient(module.app)


def test_fiado_y_abono_sin_duplicados(tmp_path):
    cl=make_client(tmp_path)
    state=cl.get('/api/bootstrap').json()
    base=next(p['qty'] for p in state['products'] if p['id']=='leche')
    cid=state['clients'][0]['id']
    sale=cl.post('/api/sales',json={'employee':'Ana','items':[{'id':'leche','qty':2}]}).json()
    assert sale['status']=='PENDIENTE'
    assert next(p['qty'] for p in cl.get('/api/bootstrap').json()['products'] if p['id']=='leche')==base
    credit=cl.post(f'/api/sales/{sale["id"]}/credit',json={'client_id':cid})
    assert credit.status_code==200,credit.text
    assert credit.json()['status']=='FIADA'
    assert cl.post(f'/api/sales/{sale["id"]}/credit',json={'client_id':cid}).status_code==409
    state=cl.get('/api/bootstrap').json()
    assert next(p['qty'] for p in state['products'] if p['id']=='leche')==base-2
    assert state['totals']['credit_outstanding_cents']==5600
    assert state['totals']['sales_cents']==0  # Fiado no equivale a ingreso cobrado
    request=cl.post(f'/api/clients/{cid}/payment-requests',json={'amount_cents':3000})
    assert request.status_code==200,request.text
    r=request.json();assert r['mode']=='DEMO'
    assert cl.get('/p/'+r['link'].split('/p/')[1]).status_code==200
    confirm=cl.post(f'/api/payment-requests/{r["id"]}/demo-confirm')
    assert confirm.status_code==200,confirm.text
    assert confirm.json()['balance_cents']==2600
    assert cl.post(f'/api/payment-requests/{r["id"]}/demo-confirm').status_code==409
    assert cl.get('/api/bootstrap').json()['totals']['credit_outstanding_cents']==2600
    assert next(p['qty'] for p in cl.get('/api/bootstrap').json()['products'] if p['id']=='leche')==base-2


def test_limite_de_credito_y_datos_cliente(tmp_path):
    cl=make_client(tmp_path)
    bad=cl.post('/api/clients',json={'name':'Cliente Demo','phone':'123','credit_limit_cents':5000})
    assert bad.status_code==400
    new=cl.post('/api/clients',json={'name':'Cliente de prueba','phone':'','credit_limit_cents':100})
    assert new.status_code==200
    sale=cl.post('/api/sales',json={'employee':'Luis','items':[{'id':'agua','qty':1}]}).json()
    out=cl.post(f'/api/sales/{sale["id"]}/credit',json={'client_id':new.json()['id']})
    assert out.status_code==409
    assert cl.get('/api/bootstrap').json()['totals']['credit_outstanding_cents']==0


def test_venta_qr_demo_no_descontar_antes_de_pago(tmp_path):
    cl=make_client(tmp_path)
    base=next(p['qty'] for p in cl.get('/api/bootstrap').json()['products'] if p['id']=='agua')
    s=cl.post('/api/sales',json={'employee':'María','items':[{'id':'agua','qty':2}]}).json()
    qr=cl.post(f'/api/sales/{s["id"]}/qr')
    assert qr.status_code==200,qr.text
    assert qr.json()['mode']=='DEMO'
    assert next(p['qty'] for p in cl.get('/api/bootstrap').json()['products'] if p['id']=='agua')==base
    paid=cl.post(f'/api/sales/{s["id"]}/demo-confirm')
    assert paid.status_code==200,paid.text
    assert cl.post(f'/api/sales/{s["id"]}/demo-confirm').status_code==409
    st=cl.get('/api/bootstrap').json()
    assert next(p['qty'] for p in st['products'] if p['id']=='agua')==base-2
    assert st['totals']['sales_cents']==0  # simulaciones NO son ingresos bancarios
    assert st['totals']['demo_sales_count']==1


def test_recepcion_y_notificacion(tmp_path):
    cl=make_client(tmp_path)
    po=cl.post('/api/purchases',json={'product_id':'pan','quantity':10,'supplier':'Demo'}).json()
    rec=cl.post(f'/api/purchases/{po["id"]}/receive',json={'quantity':9,'employee':'Ana','expiry':None})
    assert rec.status_code==200
    assert cl.post(f'/api/purchases/{po["id"]}/receive',json={'quantity':9,'employee':'Ana'}).status_code==409
    snapshot=cl.get('/api/bootstrap').json()
    assert any('recibió 9 piezas' in x['message'] for x in snapshot['notifications'])
