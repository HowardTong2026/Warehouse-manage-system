/**
 * Categories / Suppliers / Locations Page - MVP version (simplified)
 */
import { useState } from 'react';
import { useCategories, useCreateCategory, useUpdateCategory, useDeleteCategory } from '../hooks/useCategories';
import { useSuppliers, useCreateSupplier, useUpdateSupplier, useDeleteSupplier } from '../hooks/useSuppliers';
import { useLocations, useCreateLocation, useUpdateLocation, useDeleteLocation } from '../hooks/useLocations';
import { Card, Button, Modal, Input, Select, Table } from '../components/ui';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';

type MasterTab = 'categories' | 'suppliers' | 'locations';

export function CategoriesSuppliersLocationsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">分類 / 供應商 / 倉位</h1>
          <p className="text-gray-500 mt-1">管理基礎主檔資料 (建構中...)</p>
        </div>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <p className="text-gray-500">此頁面建構中。核心功能請使用其他頁面：</p>
        <ul className="list-disc list-inside mt-4 space-y-2 text-gray-600">
          <li>產品管理 - 完整 CRUD</li>
          <li>進貨/銷貨 - 完整進銷存</li>
          <li>補貨提醒 - 即時低庫存監控</li>
          <li>業績報表 - 銷貨員業績分析</li>
        </ul>
      </div>
    </div>
  );
}