"use client";

import { FormEvent, useState } from "react";
import { Eye, EyeOff, LockKeyhole, Mail } from "lucide-react";
import { useLoginAuthLoginPost } from "@/api/endpoints/default/default";

export default function Page() {
  const [showPassword, setShowPassword] = useState(false);

  const loginMutation = useLoginAuthLoginPost();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);

    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    loginMutation.mutate({
      data: {
        email,
        password,
      },
    });
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-5 py-8 text-foreground">
      <section className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-5 flex size-12 items-center justify-center rounded-2xl bg-primary text-lg font-bold text-primary-foreground">
            G
          </div>

          <h1 className="text-3xl font-semibold tracking-tight">
            gymnatic
          </h1>

          <p className="mt-2 text-sm text-muted-foreground">
            Inicia sesión para gestionar tu gimnasio.
          </p>
        </div>

        <div className="rounded-2xl border border-border bg-card p-6 shadow-xl shadow-black/10 sm:p-8">
          <form className="space-y-5" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">
                Correo
              </label>

              <div className="relative">
                <Mail
                  className="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
                  aria-hidden="true"
                />

                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  placeholder="nombre@ejemplo.com"
                  required
                  className="h-11 w-full rounded-lg border border-input bg-background pl-10 pr-3 text-sm outline-none transition placeholder:text-muted-foreground focus:border-primary focus:ring-4 focus:ring-primary/15"
                />
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="text-sm font-medium">
                  Contraseña
                </label>

                <button
                  type="button"
                  className="text-xs font-medium text-primary hover:underline"
                >
                  Olvidaste tu contraseña?
                </button>
              </div>

              <div className="relative">
                <LockKeyhole
                  className="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
                  aria-hidden="true"
                />

                <input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  placeholder="Ingresa tu contraseña"
                  required
                  className="h-11 w-full rounded-lg border border-input bg-background pl-10 pr-10 text-sm outline-none transition placeholder:text-muted-foreground focus:border-primary focus:ring-4 focus:ring-primary/15"
                />

                <button
                  type="button"
                  aria-label={
                    showPassword ? "Hide password" : "Show password"
                  }
                  onClick={() => setShowPassword((visible) => !visible)}
                  className="absolute right-2 top-1/2 flex size-7 -translate-y-1/2 items-center justify-center rounded text-muted-foreground hover:text-foreground"
                >
                  {showPassword ? (
                    <EyeOff className="size-4" />
                  ) : (
                    <Eye className="size-4" />
                  )}
                </button>
              </div>
            </div>

            <label className="flex items-center gap-2 text-sm text-muted-foreground">
              <input
                type="checkbox"
                className="size-4 rounded border-input accent-primary"
              />
              Recuerdame
            </label>

            <button
              type="submit"
              disabled={loginMutation.isPending}
              className="h-11 w-full rounded-lg bg-primary px-4 text-sm font-semibold text-primary-foreground transition hover:opacity-90 focus:outline-none focus:ring-4 focus:ring-primary/25 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loginMutation.isPending ? "Iniciando sesión..." : "Iniciar sesión"}
            </button>

            {loginMutation.isError && (
              <p className="text-center text-sm text-red-500">
                Correo o contraseña incorrectos.
              </p>
            )}

            {loginMutation.isSuccess && (
              <p className="text-center text-sm text-green-500">
                ¡Inicio de sesión exitoso!
              </p>
            )}
          </form>

          <p className="mt-6 text-center text-xs text-muted-foreground">
            Necesitas acceso?{" "}
            <button
              type="button"
              className="font-medium text-primary hover:underline"
            >
              Contacta a tu administrador
            </button>
          </p>
        </div>

        <p className="mt-6 text-center text-xs text-muted-foreground">
          © 2026 gymnatic
        </p>
      </section>
    </main>
  );
}