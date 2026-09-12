"use client";

export function TenantSwitcher() {
  return (
    <div className="flex items-center space-x-2 border p-2 rounded-md bg-muted/50 w-full cursor-pointer hover:bg-muted transition-colors">
      <div className="w-6 h-6 rounded bg-primary text-primary-foreground flex items-center justify-center font-bold text-xs">
        B
      </div>
      <div className="flex-1 text-sm font-medium leading-none">
        Demo Business
      </div>
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-muted-foreground"><path d="m6 9 6 6 6-6"/></svg>
    </div>
  );
}
