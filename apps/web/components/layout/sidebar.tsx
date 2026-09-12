"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { TenantSwitcher } from "./tenant-switcher";

const navigation = [
  { name: "Dashboard", href: "/dashboard" },
  { name: "Conversations", href: "/dashboard/conversations" },
  { name: "Appointments", href: "/dashboard/appointments" },
  { name: "Settings", href: "/dashboard/settings" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-full w-full flex-col border-r bg-background">
      <div className="p-4 border-b">
        <TenantSwitcher />
      </div>
      <div className="flex-1 overflow-auto py-4">
        <nav className="grid gap-1 px-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all ${
                  isActive ? "bg-secondary text-secondary-foreground" : "text-muted-foreground hover:bg-secondary/50 hover:text-foreground"
                }`}
              >
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>
      <div className="p-4 border-t mt-auto text-xs text-muted-foreground">
        AI Receptionist v1.0
      </div>
    </div>
  );
}
