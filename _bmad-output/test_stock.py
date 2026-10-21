from app import create_app

app = create_app()
with app.test_client() as client:
    # Test stock in
    r = client.post('/api/stock/in', json={
        'product_id': 1,  # MacBook Pro
        'location_id': 3,  # Zone 1
        'quantity': 5,
        'unit_price': 1650.00,
        'reason': 'Test purchase'
    })
    print('POST /api/stock/in:', r.status_code, r.get_json())
    
    # Test stock out
    r = client.post('/api/stock/out', json={
        'product_id': 2,  # Dell XPS
        'location_id': 3,
        'quantity': 1,
        'unit_price': 1599.00,
        'salesperson_id': 1,  # Alice
        'reason': 'Test sale'
    })
    print('POST /api/stock/out:', r.status_code, r.get_json())
    
    # Test low stock now
    r = client.get('/api/alerts/low-stock')
    items = r.get_json()
    print('Low stock after test:', len(items), 'items')
    for item in items:
        print('  {}: available={}, threshold={}'.format(item['sku'], item['available_stock'], item['reorder_threshold']))