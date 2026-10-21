
/**
 * Custom hooks for categories API
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import type { Category, PaginatedResponse } from '../types';

export const useCategories = (tree = false) => {
  return useQuery<Category[]>({
    queryKey: ['categories', { tree }],
    queryFn: async (): Promise<Category[]> => {
      const response = await apiClient.get<any>(API_ENDPOINTS.categories.list, {
        params: { tree },
      });
      return tree ? response.data : response.data.items;
    },
    staleTime: 60000,
  });
};

export const useCreateCategory = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<Category>) => {
      const response = await apiClient.post<Category>(API_ENDPOINTS.categories.create, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
    },
  });
};

export const useUpdateCategory = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<Category> }) => {
      const response = await apiClient.put<Category>(API_ENDPOINTS.categories.update(id), data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
    },
  });
};

export const useDeleteCategory = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(API_ENDPOINTS.categories.delete(id));
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
    },
  });
};
