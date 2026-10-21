import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import type { Supplier, PaginatedResponse } from '../types';

interface SuppliersParams {
  page?: number;
  limit?: number;
  is_active?: boolean;
}

export const useSuppliers = (params: SuppliersParams = {}) => {
  return useQuery({
    queryKey: ['suppliers', params],
    queryFn: async () => {
      const response = await apiClient.get<PaginatedResponse<Supplier>>(API_ENDPOINTS.suppliers.list, { params });
      return response.data.items;
    },
    staleTime: 60000,
  });
};

export const useCreateSupplier = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<Supplier>) => {
      const response = await apiClient.post<Supplier>(API_ENDPOINTS.suppliers.create, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suppliers'] });
    },
  });
};

export const useUpdateSupplier = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<Supplier> }) => {
      const response = await apiClient.put<Supplier>(API_ENDPOINTS.suppliers.update(id), data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suppliers'] });
    },
  });
};

export const useDeleteSupplier = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(API_ENDPOINTS.suppliers.delete(id));
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suppliers'] });
    },
  });
};