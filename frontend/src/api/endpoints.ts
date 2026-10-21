/**
 * API endpoint constants
 * Centralized for easy maintenance
 */
export const API_ENDPOINTS = {
  // Products
  products: {
    list: '/products',
    get: (id: number) => `/products/${id}`,
    create: '/products',
    update: (id: number) => `/products/${id}`,
    delete: (id: number) => `/products/${id}`,
  },

  // Categories
  categories: {
    list: '/categories',
    create: '/categories',
    update: (id: number) => `/categories/${id}`,
    delete: (id: number) => `/categories/${id}`,
  },

  // Suppliers
  suppliers: {
    list: '/suppliers',
    create: '/suppliers',
    update: (id: number) => `/suppliers/${id}`,
    delete: (id: number) => `/suppliers/${id}`,
  },

  // Locations
  locations: {
    list: '/locations',
    create: '/locations',
    update: (id: number) => `/locations/${id}`,
    delete: (id: number) => `/locations/${id}`,
  },

  // Stock
  stock: {
    in: '/stock/in',
    out: '/stock/out',
    transfer: '/stock/transfer',
    movements: (productId: number) => `/products/${productId}/movements`,
  },

  // Alerts
  alerts: {
    lowStock: '/alerts/low-stock',
    reorderSuggestions: '/alerts/reorder-suggestions',
    summary: '/alerts/summary',
  },

  // Salespeople
  salespeople: {
    list: '/salespeople',
    get: (id: number) => `/salespeople/${id}`,
    create: '/salespeople',
    update: (id: number) => `/salespeople/${id}`,
    delete: (id: number) => `/salespeople/${id}`,
  },

  // Reports
  reports: {
    salesperson: (id: number) => `/reports/salesperson/${id}`,
    leaderboard: '/reports/salespeople/leaderboard',
    export: (id: number) => `/reports/salesperson/${id}/export`,
  },

  // Dashboard
  dashboard: {
    summary: '/dashboard/summary',
  },

  // Health
  health: '/health',
} as const;