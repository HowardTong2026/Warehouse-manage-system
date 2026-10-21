/**
 * Custom hook for dashboard API
 */
import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import type { DashboardSummary } from '../types';

export const useDashboard = () => {
  return useQuery({
    queryKey: ['dashboard', 'summary'],
    queryFn: async () => {
      const response = await apiClient.get<DashboardSummary>(API_ENDPOINTS.dashboard.summary);
      return response.data;
    },
    staleTime: 30000,
    refetchInterval: 60000,
  });
};