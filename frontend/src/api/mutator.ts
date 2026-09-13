const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
}

async function refreshAccessToken(): Promise<string | null> {
  try {
    const response = await fetch(`${API_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      setAccessToken(null);
      return null;
    }

    const data = await response.json();

    setAccessToken(data.access_token);

    return data.access_token;
  } catch {
    setAccessToken(null);
    return null;
  }
}

export const customInstance = async <T>(
  url: string,
  options?: RequestInit,
): Promise<T> => {
  const token = accessToken;

  const headers = new Headers(options?.headers);

  headers.set("Content-Type", "application/json");

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  let response = await fetch(`${API_URL}${url}`, {
    ...options,
    headers,
    credentials: "include",
  });

  if (response.status === 401 && url !== "/auth/refresh") {
    const newToken = await refreshAccessToken();

    if (newToken) {
      headers.set("Authorization", `Bearer ${newToken}`);

      response = await fetch(`${API_URL}${url}`, {
        ...options,
        headers,
        credentials: "include",
      });
    }
  }

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
