/**
 * Custom hooks for locations API
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import type { Location, PaginatedResponse } from '../types';

export const useLocations = (tree = false) => {
  return useQuery<Location[]>({
    queryKey: ['locations', { tree }],
    queryFn: async (): Promise<Location[]> => {
      const response = await apiClient.get<any>(API_ENDPOINTS.locations.list, {
        params: { tree },
      });
      return tree ? response.data : response.data.items;
    },
    staleTime: 60000,
  });
};

export const useCreateLocation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<Location>) => {
      const response = await apiClient.post<Location>(API_ENDPOINTS.locations.create, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['locations'] });
    },
  });
};

export const useUpdateLocation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<Location> }) => {
      const response = await apiClient.put<Location>(API_ENDPOINTS.locations.update(id), data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['locations'] });
    },
  });
};

export const useDeleteLocation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(API_ENDPOINTS.locations.delete(id));
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['locations'] });
    },
  });
}
