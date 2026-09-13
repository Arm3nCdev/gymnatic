const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export const customInstance = async <T>(
  url: string,
  options?: RequestInit,
): Promise<T> => {
  const token = localStorage.getItem("access_token") || sessionStorage.getItem("access_token");

  const response = await fetch(`${API_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...options?.headers,
    },
  });

  const body = response.status === 204 ? null : await response.json();

  if (!response.ok) {
    throw body;
  }

  return {
    data: body,
    status: response.status,
    headers: response.headers,
  } as T;
};