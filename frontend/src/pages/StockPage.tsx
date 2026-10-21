/**
 * Stock Page - MVP version
 */
import { useState } from 'react';
import { useProducts, useLocations, useSalespeople, useSuppliers, useStockIn, useStockOut, useStockTransfer } from '../hooks';
import { Card, Button, Modal } from '../components/ui';

type StockActionType = 'in' | 'out' | 'transfer';

interface StockFormData {
  type: 'in' | 'out' | 'transfer';
  product_id: string;
  location_id: string;
  to_location_id: string;
  quantity: string;
  unit_price: string;
  salesperson_id: string;
  supplier_id: string;
  reason: string;
}

export function StockPage() {
  const [activeTab, setActiveTab] = useState<'in' | 'out' | 'transfer'>('in');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    type: 'in', product_id: '', location_id: '', to_location_id: '',
    quantity: '', unit_price: '', salesperson_id: '', supplier_id: '', reason: '',
  });

  const { data: productsData } = useProducts();
  const { data: locationsData } = useLocations();
  const { data: salespeopleData } = useSalespeople();
  const { data: suppliersData } = useSuppliers();

  const stockInMutation = useStockIn();
  const stockOutMutation = useStockOut();
  const transferMutation = useStockTransfer();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      product_id: parseInt(formData.product_id),
      location_id: parseInt(formData.location_id),
      quantity: parseInt(formData.quantity),
      unit_price: parseFloat(formData.unit_price),
      reason: formData.reason,
    };

    if (activeTab === 'in') {
      stockInMutation.mutate({ ...payload, supplier_id: formData.supplier_id ? parseInt(formData.supplier_id) : undefined }, { onSuccess: () => { setShowModal(false); } });
    } else if (activeTab === 'out') {
      stockOutMutation.mutate({ ...payload, salesperson_id: parseInt(formData.salesperson_id) }, { onSuccess: () => { setShowModal(false); } });
    } else {
      transferMutation.mutate({ ...payload, from_location_id: parseInt(formData.location_id), to_location_id: parseInt(formData.to_location_id) }, { onSuccess: () => { setShowModal(false); } });
    }
  };

  const tabs = [
    { type: 'in' as const, label: '進貨', icon: '⬇️', desc: '採購入庫、退貨入庫' },
    { type: 'out' as const, label: '銷貨', icon: '⬆️', desc: '銷售出貨、銷貨員記錄' },
    { type: 'transfer' as const, label: '調撥', icon: '↔️', desc: '倉位間調撥移動' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">進貨/銷貨</h1>
          <p className="text-gray-500 mt-1">庫存進銷存管理、調撥移動</p>
        </div>
        <button onClick={() => { setActiveTab('in'); }} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-2">新增記錄</button>
      </div>

      <div className="border-b border-gray-200">
        <nav className="flex gap-8" aria-label="Stock actions">
          {tabs.map(tab => (
            <button key={tab.type} onClick={() => { setActiveTab(tab.type); }} className={`flex items-center gap-2 px-4 py-4 text-sm font-medium border-b-2 transition-colors ${activeTab === tab.type ? 'border-primary-600 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}>
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>
      </div>

      <div className="text-center py-12 text-gray-500">
        <p className="text-lg font-medium">{tabs.find(t => t.type === activeTab)?.label} 功能</p>
        <p className="text-gray-400 mt-1">點擊上方按鈕新增記錄</p>
      </div>

      <div className="fixed inset-0 z-50" style={{display: showModal ? 'block' : 'none'}}>
        <div className="fixed inset-0 bg-black/25" onClick={() => setShowModal(false)} />
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-lg w-full p-6">
            <h2 className="text-xl font-semibold mb-4">{tabs.find(t => t.type === activeTab)?.label} 記錄</h2>
            <form onSubmit={e => { e.preventDefault(); handleSubmit(e); }} className="space-y-4">
              <select value={formData.product_id} onChange={e => setFormData({...formData, product_id: e.target.value})} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option value="">選擇產品</option>
                {productsData?.map((p: any) => (<option key={p.id} value={p.id}>{p.sku} - {p.name} (可用 {p.available_stock})</option>))}
              </select>
              <select value={formData.location_id} onChange={e => setFormData({...formData, location_id: e.target.value})} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option value="">選擇倉位</option>
                {locationsData?.map((l: any) => (<option key={l.id} value={l.id}>{l.name}</option>))}
              </select>
              <div className="grid grid-cols-2 gap-4">
                <input type="number" min="1" placeholder="數量 *" value={formData.quantity} onChange={e => setFormData({...formData, quantity: e.target.value})} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
                <input type="number" step="0.01" min="0" placeholder="單價 *" value={formData.unit_price} onChange={e => setFormData({...formData, unit_price: e.target.value})} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
              </div>
              <textarea placeholder="原因/備註" value={formData.reason} onChange={e => setFormData({...formData, reason: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
              <div className="flex justify-end gap-3 pt-4 border-t">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">取消</button>
                <button type="submit" className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">確認</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}