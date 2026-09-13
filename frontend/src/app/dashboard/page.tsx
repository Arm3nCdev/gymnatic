"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Page() {
  const router = useRouter();

  useEffect(() => {
    const token =
      localStorage.getItem("access_token") ||
      sessionStorage.getItem("access_token");

    if (!token) {
      router.replace("/login");
    }
  }, [router]);

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
            className="mt-24 h-11 w-full rounded-lg bg-primary px-4 text-sm font-semibold text-primary-foreground transition hover:opacity-90 focus:outline-none focus:ring-4 focus:ring-primary/25 disabled:cursor-not-allowed disabled:opacity-60"
            onClick={() => {
              localStorage.removeItem("access_token");
              localStorage.removeItem("token_type");

              sessionStorage.removeItem("access_token");
              sessionStorage.removeItem("token_type");

              router.replace("/login");
            }}
          >
            Cerrar sesión
          </button>
        </div>

        <p className="mt-6 text-center text-xs text-muted-foreground">
          © 2026 gymnatic
        </p>
      </section>
    </main>
  );
}
