/**
 * Custom hooks for reports API
 */
import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import type { SalespersonPerformance, LeaderboardEntry } from '../types';

export const useSalespersonPerformance = (spId: number, params?: {
  from?: string;
  to?: string;
  group_by?: 'day' | 'week' | 'month';
}) => {
  return useQuery({
    queryKey: ['reports', 'salesperson', spId, params],
    queryFn: async () => {
      const response = await apiClient.get<SalespersonPerformance>(
        API_ENDPOINTS.reports.salesperson(spId),
        { params }
      );
      return response.data;
    },
    enabled: !!spId,
    staleTime: 60000,
  });
};

export const useLeaderboard = (params?: {
  from?: string;
  to?: string;
  metric?: 'revenue' | 'transactions' | 'avg_order';
}) => {
  return useQuery({
    queryKey: ['reports', 'leaderboard', params],
    queryFn: async () => {
      const response = await apiClient.get<LeaderboardEntry[]>(
        API_ENDPOINTS.reports.leaderboard,
        { params }
      );
      return response.data;
    },
    staleTime: 60000,
  });
};

export const useExportSalesperson = (spId: number, params?: { from?: string; to?: string }) => {
  const exportData = async () => {
    const response = await apiClient.get(API_ENDPOINTS.reports.export(spId), {
      params,
      responseType: 'blob',
    });
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `salesperson_${spId}_report.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };
  
  return { exportData };
};