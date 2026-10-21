/**
 * Badge component for status indicators
 */
import { clsx } from 'clsx';
import type { ReactNode } from 'react';

interface BadgeProps {
  children: ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info' | 'gray';
  size?: 'sm' | 'md';
  className?: string;
}

export function Badge({ children, variant = 'default', size = 'md', className }: { children: ReactNode; variant?: 'default' | 'success' | 'warning' | 'danger' | 'info' | 'gray'; size?: 'sm' | 'md'; className?: string }) {
  const variantClasses = {
    default: 'bg-gray-100 text-gray-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    danger: 'bg-red-100 text-red-800',
    info: 'bg-blue-100 text-blue-800',
    gray: 'bg-gray-100 text-gray-600',
  };

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center font-medium rounded-full',
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
    >
      {children}
    </span>
  );
}

export function StatusBadge({ status }: { status: 'OK' | 'LOW_STOCK' | 'OUT_OF_STOCK' }) {
  const config = {
    OK: { label: '正常', variant: 'success' as const },
    LOW_STOCK: { label: '需補貨', variant: 'warning' as const },
    OUT_OF_STOCK: { label: '缺貨', variant: 'danger' as const },
  };

  const { label, variant } = config[status];
  return <Badge variant={variant}>{label}</Badge>;
}