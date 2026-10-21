/**
 * Header component with user menu and alerts
 */
import { useState, Fragment } from 'react';
import { clsx } from 'clsx';
import { UserCircleIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { Menu, Transition } from '@headlessui/react';
import { useToast } from '../ui';
import { useAlertSummary } from '../../hooks/useStock';

export function Header() {
  const [searchQuery, setSearchQuery] = useState('');
  const { warning } = useToast();
  const { data: alertSummary } = useAlertSummary();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/products?search=${encodeURIComponent(searchQuery.trim())}`;
    }
  };

  return (
    <header className="fixed top-0 left-64 right-0 z-30 h-16 bg-white border-b border-gray-200 flex items-center px-6">
      {/* Search */}
      <form onSubmit={handleSearch} className="flex-1 max-w-xl mx-8 relative" role="search">
        <label htmlFor="global-search" className="sr-only">全域搜尋</label>
        <div className="relative">
          <input
            type="search"
            id="global-search"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="搜尋產品、SKU、條碼..."
            className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            autoComplete="off"
          />
        </div>
      </form>

      {/* Alerts & User Menu */}
      <div className="flex items-center gap-4">
        {/* Alert Bell */}
        {alertSummary && alertSummary.low_stock_count > 0 && (
          <button
            className={`relative p-2 rounded-lg hover:bg-gray-100 transition-colors ${alertSummary.out_of_stock_count > 0 ? 'text-red-600 animate-pulse' : ''}`}
            aria-label={`補貨提醒: ${alertSummary.low_stock_count} 項需補貨`}
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 5.165 6 6.879 6 8.828V11A2.032 2.032 0 013.595 13.842L2 15.258" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
            </svg>
            {alertSummary.low_stock_count > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
                {alertSummary.low_stock_count > 9 ? '9+' : alertSummary.low_stock_count}
              </span>
            )}
          </button>
        )}

        {/* User Menu */}
        <Menu as="div" className="relative">
          <Menu.Button className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500">
            <svg className="h-8 w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span className="hidden sm:block text-sm font-medium text-gray-700">Admin</span>
          </Menu.Button>

          <Transition
            as={Fragment}
            enter="transition ease-out duration-100"
            enterFrom="transform opacity-0 scale-95"
            enterTo="transform opacity-100 scale-100"
            leave="transition ease-in duration-75"
            leaveFrom="transform opacity-100 scale-100"
            leaveTo="transform opacity-0 scale-95"
          >
            <Menu.Items className="absolute right-0 mt-2 w-48 origin-top-right rounded-lg bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
              <Menu.Item>
                {({ active }) => (
                  <button className={`w-full px-4 py-2 text-sm text-left ${active ? 'bg-gray-50 text-blue-600' : 'text-gray-700 hover:bg-gray-50'}`}>
                    個人資料
                  </button>
                )}
              </Menu.Item>
              <Menu.Item>
                {({ active }) => (
                  <button className={`w-full px-4 py-2 text-sm text-left ${active ? 'bg-gray-50 text-blue-600' : 'text-gray-700 hover:bg-gray-50'}`}>
                    設定
                  </button>
                )}
              </Menu.Item>
              <Menu.Item>
                <hr className="my-1 border-gray-100" />
              </Menu.Item>
              <Menu.Item>
                {({ active }) => (
                  <button className={`w-full px-4 py-2 text-sm text-left text-red-600 ${active ? 'bg-red-50' : 'hover:bg-gray-50'}`}>
                    登出
                  </button>
                )}
              </Menu.Item>
            </Menu.Items>
          </Transition>
        </Menu>
      </div>
    </header>
  );
}