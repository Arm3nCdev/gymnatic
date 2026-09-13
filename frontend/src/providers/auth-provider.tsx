"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { setAccessToken } from "@/api/mutator";

type AuthContextType = {
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  function login(token: string) {
    setAccessToken(token);
    setIsAuthenticated(true);
  }

  function logout() {
    setAccessToken(null);
    setIsAuthenticated(false);
  }

  useEffect(() => {
    async function restoreSession() {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`,
          {
            method: "POST",
            credentials: "include",
          },
        );

        if (!response.ok) {
          setAccessToken(null);
          setIsAuthenticated(false);
          return;
        }

        const data = await response.json();

        setAccessToken(data.access_token);
        setIsAuthenticated(true);
      } catch {
        setAccessToken(null);
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    }

    restoreSession();
  }, []);


  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth debe utilizarse dentro de AuthProvider");
  }

  return context;
}
