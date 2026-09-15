import { ReactNode } from "react";
import { Sidebar } from "../../components/layout/sidebar";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen w-full flex-col md:flex-row bg-background">
      {/* Mobile Header */}
      <header className="flex md:hidden h-14 items-center gap-4 border-b bg-muted/40 px-4 shrink-0">
        <div className="font-semibold text-lg">AI Receptionist</div>
        {/* Placeholder for a mobile hamburger menu to toggle sidebar */}
        <div className="ml-auto text-sm text-muted-foreground">Menu (WIP)</div>
      </header>

      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-64 border-r shrink-0">
        <Sidebar />
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-4 md:p-6 lg:p-8 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
