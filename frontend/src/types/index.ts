/**
 * TypeScript interfaces matching the backend API responses
 * Keep in sync with backend schemas
 */

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pages: number;
  limit: number;
}

export interface ApiError {
  error: string;
  message: string;
  details?: Record<string, string>;
}

export interface Category {
  id: number;
  name: string;
  description: string | null;
  parent_id: number | null;
  path: string;
  level: number;
  is_active: boolean;
  full_path: string;
  created_at: string;
  updated_at: string;
  children?: Category[];
}

export interface Supplier {
  id: number;
  name: string;
  contact_name: string | null;
  email: string | null;
  phone: string | null;
  address: string | null;
  lead_time_days: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductSupplierLink {
  id: number;
  product_id: number;
  supplier_id: number;
  supplier_sku: string | null;
  supplier_price: number | null;
  min_order_qty: number;
  is_preferred: boolean;
  supplier?: Supplier;
}

export interface Product {
  id: number;
  name: string;
  sku: string;
  barcode: string | null;
  description: string | null;
  category_id: number | null;
  category?: Category | null;
  unit_price: number;
  cost_price: number;
  reorder_threshold: number;
  reorder_quantity: number;
  current_stock: number;
  reserved_stock: number;
  available_stock: number;
  track_serial: boolean;
  track_batch: boolean;
  is_active: boolean;
  is_low_stock: boolean;
  margin_percent: number;
  created_at: string;
  updated_at: string;
  suppliers?: ProductSupplierLink[];
}

export interface Location {
  id: number;
  name: string;
  description: string | null;
  parent_id: number | null;
  path: string;
  level: number;
  is_active: boolean;
  full_path: string;
  created_at: string;
  updated_at: string;
  children?: Location[];
}

export interface StockItem {
  id: number;
  product_id: number;
  location_id: number;
  product?: Product;
  location?: Location;
  quantity: number;
  reserved: number;
  available: number;
  batch_number: string | null;
  serial_numbers: string[] | null;
  created_at: string;
  updated_at: string;
}

export interface Salesperson {
  id: number;
  name: string;
  email: string | null;
  phone: string | null;
  employee_id: string | null;
  hire_date: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export type MovementType = 'in' | 'out' | 'adjustment' | 'transfer' | 'return';
export type ReferenceType = 'sale' | 'purchase' | 'adjustment' | 'transfer' | 'return';

export interface StockMovement {
  id: number;
  product_id: number;
  location_id: number | null;
  salesperson_id: number | null;
  supplier_id: number | null;
  type: MovementType;
  reference_type: ReferenceType | null;
  reference_id: number | null;
  quantity: number;
  unit_price_at_time: number;
  total_amount: number | null;
  reason: string | null;
  notes: string | null;
  changed_by: string | null;
  product?: Product;
  location?: Location;
  salesperson?: Salesperson;
  supplier?: Supplier;
  created_at: string;
}

export interface LowStockItem {
  id: number;
  sku: string;
  name: string;
  category: string | null;
  current_stock: number;
  available_stock: number;
  reorder_threshold: number;
  reorder_quantity: number;
  unit_price: number;
  urgency_ratio: number;
  status: 'OUT_OF_STOCK' | 'LOW_STOCK';
}

export interface ReorderSuggestionGroup {
  supplier_id: number;
  supplier_name: string;
  supplier_email: string | null;
  lead_time_days: number;
  items: ReorderSuggestionItem[];
  total_estimated_cost: number;
}

export interface ReorderSuggestionItem {
  product_id: number;
  sku: string;
  name: string;
  current_stock: number;
  threshold: number;
  suggested_qty: number;
  supplier_sku: string | null;
  unit_cost: number;
  estimated_cost: number;
}

export interface SalespersonPerformance {
  salesperson: {
    id: number;
    name: string;
    employee_id: string | null;
  };
  period: {
    from: string | null;
    to: string | null;
  };
  summary: {
    total_revenue: number;
    transaction_count: number;
    avg_order_value: number;
  };
  top_products: TopProduct[];
  daily_breakdown: DailyBreakdown[];
}

export interface TopProduct {
  product_id: number;
  name: string;
  qty_sold: number;
  revenue: number;
}

export interface DailyBreakdown {
  period: string;
  revenue: number;
  transactions: number;
}

export interface LeaderboardEntry {
  rank: number;
  salesperson_id: number;
  name: string;
  employee_id: string | null;
  total_revenue: number;
  transaction_count: number;
  avg_order_value: number;
}

export interface DashboardSummary {
  kpis: {
    total_products: number;
    low_stock_count: number;
    total_stock_value: number;
    today_sales: number;
    today_transactions: number;
    week_sales: number;
  };
  top_salespeople: Array<{
    id: number;
    name: string;
    revenue: number;
    transactions: number;
  }>;
}

export interface AlertSummary {
  low_stock_count: number;
  out_of_stock_count: number;
  message: string;
}