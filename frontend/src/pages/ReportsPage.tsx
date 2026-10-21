/**
 * Reports Page - MVP version
 */
import { useState } from 'react';
import { useSalespeople, useSalespersonPerformance, useLeaderboard } from '../hooks';
import { formatCurrency, formatNumber } from '../utils/formatters';
import { ChartBarIcon, ArrowDownTrayIcon, UserGroupIcon, TrophyIcon } from '@heroicons/react/24/outline';

export function ReportsPage() {
  const [selectedSalesperson, setSelectedSalesperson] = useState<string | null>(null);
  const [dateFrom, setDateFrom] = useState(() => {
    const d = new Date();
    d.setMonth(d.getMonth() - 1);
    return d.toISOString().split('T')[0];
  });
  const [dateTo, setDateTo] = useState(() => new Date().toISOString().split('T')[0]);
  const [groupBy, setGroupBy] = useState<'day' | 'week' | 'month'>('day');

  const { data: salespeopleData } = useSalespeople();
  const { data: performance } = useSalespersonPerformance(selectedSalesperson ? parseInt(selectedSalesperson) : 0, { from: dateFrom, to: dateTo, group_by: groupBy });
  const { data: leaderboard } = useLeaderboard({ from: dateFrom, to: dateTo });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">業績報表</h1>
          <p className="text-gray-500 mt-1">銷貨員業績分析與排行榜</p>
        </div>
        <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700" disabled={!selectedSalesperson}>
          匯出 CSV
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">銷貨員</label>
          <select value={selectedSalesperson || ''} onChange={e => setSelectedSalesperson(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
            <option value="">全部銷貨員</option>
            {salespeopleData?.filter((s: any) => s.is_active).map((s: any) => (<option key={s.id} value={s.id}>{s.name} ({s.employee_id})</option>))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">起始日期</label>
          <input type="date" value={dateFrom} onChange={e => setDateFrom(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">結束日期</label>
          <input type="date" value={dateTo} onChange={e => setDateTo(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">群組方式</label>
          <select value={groupBy} onChange={e => setGroupBy(e.target.value as 'day' | 'week' | 'month')} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
            <option value="day">按日</option>
            <option value="week">按週</option>
            <option value="month">按月</option>
          </select>
        </div>
      </div>

      {selectedSalesperson && performance && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <p className="text-sm text-gray-500">總銷售額</p>
            <p className="text-2xl font-bold text-gray-900">${(performance.summary.total_revenue || 0).toLocaleString()}</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <p className="text-sm text-gray-500">交易筆數</p>
            <p className="text-2xl font-bold text-gray-900">{(performance.summary.transaction_count || 0).toLocaleString()}</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <p className="text-sm text-gray-500">平均客單價</p>
            <p className="text-2xl font-bold text-gray-900">${(performance.summary.avg_order_value || 0).toLocaleString()}</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <p className="text-sm text-gray-500">銷貨員</p>
            <p className="text-lg font-semibold text-gray-900">{performance.salesperson?.name || ''}</p>
          </div>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
        <h3 className="text-lg font-semibold mb-4">{selectedSalesperson && performance ? performance.salesperson?.name : '業績趨勢'}</h3>
        <div className="h-64">
          <canvas id="performanceChart" width="800" height="300"></canvas>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100">
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h3 className="text-lg font-semibold">業績排行榜</h3>
          <span className="text-sm text-gray-500">期間: {dateFrom} ~ {dateTo}</span>
        </div>
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">排名</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">銷貨員</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">總銷售額</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">交易筆數</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">平均客單價</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {leaderboard?.map((row: any, index: number) => (
              <tr key={row.salesperson_id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-gray-900">#{index + 1}</td>
                <td className="px-4 py-3 text-sm text-gray-700">{row.name} ({row.employee_id})</td>
                <td className="px-4 py-3 text-sm text-gray-700">${(row.total_revenue || 0).toLocaleString()}</td>
                <td className="px-4 py-3 text-sm text-gray-700">{row.transactions?.toLocaleString()}</td>
                <td className="px-4 py-3 text-sm text-gray-700">${(row.avg_order_value || 0).toLocaleString()}</td>
              </tr>
            )) || (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-gray-500">此期間無銷售數據</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}