/**
 * Sidebar navigation component
 */
import { NavLink, useLocation } from 'react-router-dom';
import { clsx } from 'clsx';
import {
  HomeIcon,
  CubeIcon,
  TagIcon,
  TruckIcon,
  ExclamationTriangleIcon,
  ChartBarIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline';
import { useToast } from '../ui';

const navigation = [
  { name: '儀表板', href: '/', icon: HomeIcon },
  { name: '產品管理', href: '/products', icon: CubeIcon },
  { name: '分類/供應商/倉位', href: '/categories-suppliers-locations', icon: TagIcon },
  { name: '進貨/銷貨', href: '/stock', icon: TruckIcon },
  { name: '補貨提醒', href: '/alerts', icon: ExclamationTriangleIcon },
  { name: '業績報表', href: '/reports', icon: ChartBarIcon },
];

export function Sidebar() {
  const location = useLocation();
  const { success } = useToast();

  const handlePrint = () => {
    window.print();
    success('列印功能已觸發');
  };

  return (
    <aside className="fixed inset-y-0 left-0 z-40 w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Logo */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200">
        <h1 className="text-xl font-bold text-primary-600">Inventory</h1>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto" aria-label="Main navigation">
        {navigation.map(item => {
          const isActive = location.pathname === item.href || 
            (item.href !== '/' && location.pathname.startsWith(item.href));
          
          const Icon = item.icon;
          
          return (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive: active }) => clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                active
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              )}
              aria-current={isActive ? 'page' : undefined}
            >
              <Icon className={clsx('h-5 w-5 flex-shrink-0', isActive ? 'text-primary-600' : 'text-gray-400')} aria-hidden="true" />
              {item.name}
            </NavLink>
          );
        })}
      </nav>

      {/* Bottom actions */}
      <div className="p-3 border-t border-gray-200">
        <button
          onClick={handlePrint}
          className="w-full flex items-center gap-3 px-3 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
        >
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2h2m-2 2h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2h2" />
          </svg>
          列印報表
        </button>
      </div>
    </aside>
  );
}