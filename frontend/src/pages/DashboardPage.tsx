/**
 * Dashboard Page - MVP version
 */
import { useDashboard } from '../hooks/useDashboard';
import { formatCurrency, formatNumber } from '../utils/formatters';
import { CubeIcon, ExclamationTriangleIcon, CurrencyDollarIcon, ArrowTrendingUpIcon, UserGroupIcon } from '@heroicons/react/24/outline';

export function DashboardPage() {
  const { data: dashboard } = useDashboard();

  const kpis = [
    { label: '總產品數', value: dashboard?.kpis.total_products ?? 0, icon: CubeIcon, color: 'bg-blue-100 text-blue-600', formatter: formatNumber },
    { label: '需補貨項目', value: dashboard?.kpis.low_stock_count ?? 0, icon: ExclamationTriangleIcon, color: 'bg-yellow-100 text-yellow-600', formatter: formatNumber },
    { label: '總庫存價值', value: dashboard?.kpis.total_stock_value ?? 0, icon: CurrencyDollarIcon, color: 'bg-green-100 text-green-600', formatter: formatCurrency },
    { label: '今日銷售額', value: dashboard?.kpis.today_sales ?? 0, icon: ArrowTrendingUpIcon, color: 'bg-purple-100 text-purple-600', formatter: formatCurrency },
    { label: '今日交易數', value: dashboard?.kpis.today_transactions ?? 0, icon: UserGroupIcon, color: 'bg-pink-100 text-pink-600', formatter: formatNumber },
    { label: '本週銷售額', value: dashboard?.kpis.week_sales ?? 0, icon: ArrowTrendingUpIcon, color: 'bg-indigo-100 text-indigo-600', formatter: formatCurrency },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">儀表板</h1>
          <p className="text-gray-500 mt-1">庫存管理系統概覽</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {kpis.map((kpi, index) => {
          const Icon = kpi.icon;
          return (
            <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 font-medium">{kpi.label}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{kpi.formatter(kpi.value)}</p>
                </div>
                <div className={`p-3 rounded-xl ${kpi.color}`}>
                  <Icon className="h-6 w-6" />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}