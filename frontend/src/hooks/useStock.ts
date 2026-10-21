/**
 * Custom hooks for stock API
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import type { StockMovement, PaginatedResponse, LowStockItem, ReorderSuggestionGroup, AlertSummary } from '../types';

export const useLowStock = (includeZero = false) => {
  return useQuery({
    queryKey: ['alerts', 'low-stock', { includeZero }],
    queryFn: async () => {
      const response = await apiClient.get<LowStockItem[]>(API_ENDPOINTS.alerts.lowStock, {
        params: { include_zero: includeZero },
      });
      return response.data;
    },
    staleTime: 15000,
    refetchInterval: 30000,
  });
};

export const useReorderSuggestions = () => {
  return useQuery({
    queryKey: ['alerts', 'reorder-suggestions'],
    queryFn: async () => {
      const response = await apiClient.get<ReorderSuggestionGroup[]>(API_ENDPOINTS.alerts.reorderSuggestions);
      return response.data;
    },
    staleTime: 60000,
  });
};

export const useAlertSummary = () => {
  return useQuery({
    queryKey: ['alerts', 'summary'],
    queryFn: async () => {
      const response = await apiClient.get<AlertSummary>(API_ENDPOINTS.alerts.summary);
      return response.data;
    },
    staleTime: 15000,
    refetchInterval: 30000,
  });
};

export const useProductMovements = (productId: number, params?: {
  page?: number;
  limit?: number;
  type?: string;
  from?: string;
  to?: string;
}) => {
  return useQuery({
    queryKey: ['movements', productId, params],
    queryFn: async () => {
      const response = await apiClient.get<PaginatedResponse<any>>(API_ENDPOINTS.stock.movements(productId), { params });
      return response.data;
    },
    enabled: !!productId,
    staleTime: 30000,
  });
};

export const useStockIn = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: {
      product_id: number;
      location_id: number;
      quantity: number;
      unit_price: number;
      reason?: string;
      supplier_id?: number;
      reference_id?: number;
    }) => {
      const response = await apiClient.post(API_ENDPOINTS.stock.in, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
      queryClient.invalidateQueries({ queryKey: ['movements'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
};

export const useStockOut = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: {
      product_id: number;
      location_id: number;
      quantity: number;
      unit_price: number;
      salesperson_id: number;
      reason?: string;
      reference_id?: number;
    }) => {
      const response = await apiClient.post(API_ENDPOINTS.stock.out, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
      queryClient.invalidateQueries({ queryKey: ['movements'] });
      queryClient.invalidateQueries({ queryKey: ['reports'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
};

export const useStockTransfer = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: {
      product_id: number;
      from_location_id: number;
      to_location_id: number;
      quantity: number;
      reason?: string;
      reference_id?: number;
    }) => {
      const response = await apiClient.post(API_ENDPOINTS.stock.transfer, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
      queryClient.invalidateQueries({ queryKey: ['movements'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
};