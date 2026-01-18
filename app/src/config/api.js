// API Configuration for Capacitor
// In development (web): uses Vite proxy → /api/...
// In production (native app): uses full URL → https://your-api.com/api/...

import { Capacitor } from '@capacitor/core';

// Set your production API URL here when you deploy your backend
const PRODUCTION_API_URL = import.meta.env.VITE_API_URL || '';

export function getApiBaseUrl() {
  // If running as native app (iOS/Android), use production URL
  if (Capacitor.isNativePlatform()) {
    return PRODUCTION_API_URL;
  }

  // In web/dev mode, use relative path (Vite proxy handles it)
  return '';
}

export function buildApiUrl(path) {
  const baseUrl = getApiBaseUrl();
  // Ensure path starts with /
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${baseUrl}${normalizedPath}`;
}

// Helper for common API calls
export const api = {
  analyzeBazi: (params) => buildApiUrl(`/api/analyze_bazi?${new URLSearchParams(params)}`),

  // Add more endpoints as needed
  // dongGong: (params) => buildApiUrl(`/api/dong_gong?${new URLSearchParams(params)}`),
};
