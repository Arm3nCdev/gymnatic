const Spinner = () => {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background text-foreground">
      <div className="flex flex-col items-center gap-4">
        <div className="flex size-12 items-center justify-center rounded-2xl bg-primary text-lg font-bold text-primary-foreground">
          G
        </div>

        <div className="size-5 animate-spin rounded-full border-2 border-muted-foreground/25 border-t-primary" />
      </div>
    </main>
  );
};

export default Spinner;
