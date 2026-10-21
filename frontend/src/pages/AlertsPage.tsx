/**
 * Alerts Page - MVP version
 */
import { useLowStock, useReorderSuggestions, useAlertSummary } from '../hooks/useStock';
import { formatCurrency } from '../utils/formatters';
import { Card, CardHeader, Button, Table, Badge, Modal, Input, Select } from '../components/ui';
import { ExclamationTriangleIcon, ShoppingCartIcon } from '@heroicons/react/24/outline';

export function AlertsPage() {
  const { data: lowStock } = useLowStock();
  const { data: reorderSuggestions } = useReorderSuggestions();
  const { data: alertSummary } = useAlertSummary();

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <ExclamationTriangleIcon className="h-6 w-6 text-yellow-600" />
            補貨提醒
          </h1>
          <p className="text-gray-500 mt-1">即時低庫存監控與採購建議</p>
        </div>
      </div>

      {alertSummary && alertSummary.low_stock_count > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
          <div className="flex items-center gap-2 text-yellow-800">
            <span className="font-medium">{alertSummary.message}</span>
          </div>
        </div>
      )}

      <Card>
        <CardHeader title="低庫存清單" subtitle={`共 ${lowStock?.length || 0} 項需補貨`} />
        <Table
          columns={[
            { key: 'sku', header: 'SKU', render: (row: any) => <code className="px-2 py-0.5 bg-gray-100 rounded">{row.sku}</code> },
            { key: 'name', header: '產品名稱' },
            { key: 'category', header: '分類' },
            { key: 'current_stock', header: '目前庫存', render: (row: any) => row.current_stock.toLocaleString() },
            { key: 'reorder_threshold', header: '補貨點', render: (row: any) => row.reorder_threshold.toLocaleString() },
            { key: 'status', header: '狀態', render: (row: any) => <span className={row.status === 'OUT_OF_STOCK' ? 'text-red-600 font-medium' : 'text-yellow-600 font-medium'}>{row.status === 'OUT_OF_STOCK' ? '缺貨' : '需補貨'}</span> },
          ]}
          data={lowStock || []}
          keyExtractor={row => row.id}
          isLoading={false}
          emptyMessage="目前無低庫存商品"
        />
      </Card>
    </div>
  );
}