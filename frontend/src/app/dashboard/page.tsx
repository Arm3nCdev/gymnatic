"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/providers/auth-provider";
import { useLogoutAuthLogoutPost } from "@/api/endpoints/default/default";

export default function Page() {
  const router = useRouter();
  const { isAuthenticated, isLoading, logout } = useAuth();
  const logoutMutation = useLogoutAuthLogoutPost();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return <div>Cargando...</div>;
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-5 py-8 text-foreground">
      <section className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-5 flex size-12 items-center justify-center rounded-2xl bg-primary text-lg font-bold text-primary-foreground">
            G
          </div>

          <h1 className="text-3xl font-semibold tracking-tight">
            gymnatic - Dashboard
          </h1>

          <p className="mt-2 text-sm text-muted-foreground">Proximamente...</p>

          <button
            type="button"
            disabled={logoutMutation.isPending}
            className="mt-24 h-11 w-full rounded-lg bg-primary px-4 text-sm font-semibold text-primary-foreground transition hover:opacity-90 focus:outline-none focus:ring-4 focus:ring-primary/25 disabled:cursor-not-allowed disabled:opacity-60"
            onClick={() => {
              logoutMutation.mutate(undefined, {
                onSuccess: () => {
                  logout();
                  router.replace("/login");
                },
              });
            }}
          >
            {logoutMutation.isPending ? "Cerrando sesión..." : "Cerrar sesión"}
          </button>
        </div>

        <p className="mt-6 text-center text-xs text-muted-foreground">
          © 2026 gymnatic
        </p>
      </section>
    </main>
  );
}
