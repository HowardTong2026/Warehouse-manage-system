/**
 * Products Page - MVP version
 */
import { useState } from 'react';
import { useProducts, useCreateProduct, useUpdateProduct, useDeleteProduct, useCategories } from '../hooks';
import { formatCurrency } from '../utils/formatters';
import { Card, Button, Modal, Input, Select, Table } from '../components/ui';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';

interface ProductFormData {
  name: string;
  sku: string;
  barcode: string;
  description: string;
  category_id: number;
  unit_price: string;
  cost_price: string;
  reorder_threshold: string;
  reorder_quantity: string;
}

export function ProductsPage() {
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState<any>(null);
  const [formData, setFormData] = useState<ProductFormData>({
    name: '', sku: '', barcode: '', description: '',
    category_id: 0, unit_price: '', cost_price: '',
    reorder_threshold: '10', reorder_quantity: '50',
  });

  const { data: productsData, isLoading } = useProducts({ search });
  const { data: categoriesData } = useCategories();

  const createMutation = useCreateProduct();
  const updateMutation = useUpdateProduct();
  const deleteMutation = useDeleteProduct();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      name: formData.name,
      sku: formData.sku,
      barcode: formData.barcode || undefined,
      category_id: formData.category_id || undefined,
      unit_price: parseFloat(formData.unit_price),
      cost_price: parseFloat(formData.cost_price || '0'),
      reorder_threshold: parseInt(formData.reorder_threshold || '10'),
      reorder_quantity: parseInt(formData.reorder_quantity || '50'),
    };

    if (editingProduct) {
      updateMutation.mutate({ id: editingProduct.id, data: payload }, { onSuccess: () => { setShowModal(false); setEditingProduct(null); resetForm(); } });
    } else {
      createMutation.mutate(payload, { onSuccess: () => { setShowModal(false); resetForm(); } });
    }
  };

  const resetForm = () => {
    setFormData({ name: '', sku: '', barcode: '', description: '', category_id: 0, unit_price: '', cost_price: '', reorder_threshold: '10', reorder_quantity: '50' });
    setEditingProduct(null);
  };

  const openEdit = (product: any) => {
    setEditingProduct(product);
    setFormData({
      name: product.name,
      sku: product.sku,
      barcode: product.barcode || '',
      description: product.description || '',
      category_id: product.category_id || 0,
      unit_price: product.unit_price.toString(),
      cost_price: product.cost_price.toString(),
      reorder_threshold: product.reorder_threshold.toString(),
      reorder_quantity: product.reorder_quantity.toString(),
    });
    setShowModal(true);
  };

  const confirmDelete = (product: any) => {
    if (window.confirm(`確定要刪除 "${product.name}" (${product.sku}) 嗎？`)) {
      deleteMutation.mutate(product.id);
    }
  };

  const columns = [
    { key: 'sku', header: 'SKU', render: (row: any) => <code className="px-2 py-0.5 bg-gray-100 rounded">{row.sku}</code> },
    { key: 'name', header: '名稱' },
    { key: 'unit_price', header: '售價', render: (row: any) => formatCurrency(row.unit_price) },
    { key: 'current_stock', header: '庫存', render: (row: any) => row.current_stock.toLocaleString() },
    { key: 'available_stock', header: '可用', render: (row: any) => row.available_stock.toLocaleString() },
    { key: 'reorder_threshold', header: '補貨點', render: (row: any) => row.reorder_threshold.toLocaleString() },
    { key: 'status', header: '狀態', render: (row: any) => <span className={row.is_low_stock ? 'text-red-600 font-medium' : 'text-green-600 font-medium'}>{row.is_low_stock ? '需補貨' : '正常'}</span> },
    { key: 'actions', header: '操作', render: (row: any) => (
      <div className="flex items-center gap-2">
        <button onClick={() => openEdit(row)} className="p-1.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg">編輯</button>
        <button onClick={() => confirmDelete(row)} className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg">刪除</button>
      </div>
    )},
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">產品管理</h1>
          <p className="text-gray-500 mt-1">管理產品目錄、價格與庫存</p>
        </div>
        <button onClick={() => { resetForm(); setShowModal(true); }} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-2">
          <span className="h-5 w-5">➕</span>
          新增產品
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
        <form onSubmit={e => e.preventDefault()} className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1 max-w-md">
            <input
              type="search"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="搜尋名稱、SKU、條碼..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              autoComplete="off"
            />
          </div>
        </form>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SKU</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">名稱</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">售價</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">庫存</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">可用</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">補貨點</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">狀態</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {productsData?.map((row: any) => (
              <tr key={row.id} className="hover:bg-gray-50">
                <td className="px-4 py-3"><code className="px-2 py-0.5 bg-gray-100 rounded">{row.sku}</code></td>
                <td className="px-4 py-3">{row.name}</td>
                <td className="px-4 py-3">{formatCurrency(row.unit_price)}</td>
                <td className="px-4 py-3">{row.current_stock.toLocaleString()}</td>
                <td className="px-4 py-3">{row.available_stock.toLocaleString()}</td>
                <td className="px-4 py-3">{row.reorder_threshold.toLocaleString()}</td>
                <td className="px-4 py-3"><span className={row.is_low_stock ? 'text-red-600 font-medium' : 'text-green-600 font-medium'}>{row.is_low_stock ? '需補貨' : '正常'}</span></td>
                <td className="px-4 py-3">
                  <button onClick={() => openEdit(row)} className="p-1.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg">編輯</button>
                  <button onClick={() => confirmDelete(row)} className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg">刪除</button>
                </td>
              </tr>
            )) || (
              <tr>
                <td colSpan={8} className="px-4 py-8 text-center text-gray-500">沒有找到符合條件的產品</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="fixed inset-0 z-50" style={{display: showModal ? 'block' : 'none'}}>
        <div className="fixed inset-0 bg-black/25" onClick={() => setShowModal(false)} />
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-lg w-full p-6">
            <h2 className="text-xl font-semibold mb-4">{editingProduct ? '編輯產品' : '新增產品'}</h2>
            <form onSubmit={e => { e.preventDefault(); handleSubmit(e); }} className="space-y-4">
              <input type="text" placeholder="名稱 *" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
              <input type="text" placeholder="SKU *" value={formData.sku} onChange={e => setFormData({...formData, sku: e.target.value})} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
              <input type="text" placeholder="條碼" value={formData.barcode} onChange={e => setFormData({...formData, barcode: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
              <select value={formData.category_id} onChange={e => setFormData({...formData, category_id: Number(e.target.value)})} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option value={0}>選擇分類</option>
                {categoriesData?.map((c: any) => (<option key={c.id} value={c.id}>{c.name}</option>))}
              </select>
              <div className="grid grid-cols-2 gap-4">
                <input type="number" step="0.01" min="0" placeholder="售價 *" value={formData.unit_price} onChange={e => setFormData({...formData, unit_price: e.target.value})} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
                <input type="number" step="0.01" min="0" placeholder="成本" value={formData.cost_price} onChange={e => setFormData({...formData, cost_price: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <input type="number" min="0" placeholder="補貨點" value={formData.reorder_threshold} onChange={e => setFormData({...formData, reorder_threshold: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
                <input type="number" min="0" placeholder="補貨量" value={formData.reorder_quantity} onChange={e => setFormData({...formData, reorder_quantity: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
              </div>
              <textarea placeholder="描述" value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
              <div className="flex justify-end gap-3 pt-4 border-t">
                <button type="button" onClick={() => { setShowModal(false); setEditingProduct(null); }} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">取消</button>
                <button type="submit" className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">儲存</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}