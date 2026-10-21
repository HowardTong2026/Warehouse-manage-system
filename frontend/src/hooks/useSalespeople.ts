/**
 * Custom hooks for salespeople API
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import type { Salesperson, PaginatedResponse } from '../types';

interface SalespeopleParams {
  page?: number;
  limit?: number;
  is_active?: boolean;
}

export const useSalespeople = (params: SalespeopleParams = {}) => {
  return useQuery({
    queryKey: ['salespeople', params],
    queryFn: async () => {
      const response = await apiClient.get<PaginatedResponse<Salesperson>>(API_ENDPOINTS.salespeople.list, {
        params,
      });
      return response.data.items;
    },
    staleTime: 60000,
  });
};

export const useCreateSalesperson = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<Salesperson>) => {
      const response = await apiClient.post<Salesperson>(API_ENDPOINTS.salespeople.create, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['salespeople'] });
    },
  });
};

export const useUpdateSalesperson = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<Salesperson> }) => {
      const response = await apiClient.put<Salesperson>(API_ENDPOINTS.salespeople.update(id), data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['salespeople'] });
    },
  });
};

export const useDeleteSalesperson = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(API_ENDPOINTS.salespeople.delete(id));
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['salespeople'] });
    },
  });
};