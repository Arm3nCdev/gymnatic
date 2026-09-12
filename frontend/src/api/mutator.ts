const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export const customInstance = async <T>(
  url: string,
  options?: RequestInit,
): Promise<T> => {
  const response = await fetch(`${API_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  const data = response.status === 204 ? null : await response.json();

  if (!response.ok) {
    throw data;
  }

  return data;
};