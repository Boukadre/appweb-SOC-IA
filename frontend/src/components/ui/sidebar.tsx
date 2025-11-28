"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  Network,
  Shield,
  Mail,
  FileText,
  Home,
  Activity,
  Settings,
  AlertTriangle,
  Bug,
  Key,
} from "lucide-react";

interface NavItem {
  title: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

const navItems: NavItem[] = [
  {
    title: "Dashboard",
    href: "/",
    icon: Home,
  },
  {
    title: "Network Scan",
    href: "/network-scan",
    icon: Network,
  },
  {
    title: "CVE Scanner",
    href: "/cve-scanner",
    icon: Bug,
  },
  {
    title: "Malware Analysis",
    href: "/malware-analysis",
    icon: Shield,
  },
  {
    title: "Phishing Detection",
    href: "/phishing-detect",
    icon: Mail,
  },
  {
    title: "Password Analyzer",
    href: "/password-analyzer",
    icon: Key,
  },
  {
    title: "Report Generation",
    href: "/report-gen",
    icon: FileText,
  },
];

const secondaryNavItems: NavItem[] = [
  {
    title: "Activity Log",
    href: "/activity",
    icon: Activity,
  },
  {
    title: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-full w-64 flex-col border-r border-border bg-card">
      {/* Logo & Brand */}
      <div className="flex h-16 items-center border-b border-border px-6">
        <AlertTriangle className="h-8 w-8 text-cyber-primary animate-pulse-glow" />
        <span className="ml-3 text-xl font-bold gradient-text font-mono">
          CYBER IA
        </span>
      </div>

      {/* Navigation principale */}
      <nav className="flex-1 space-y-1 p-4">
        <div className="space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all",
                  isActive
                    ? "bg-primary/10 text-primary cyber-glow"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                )}
              >
                <Icon className={cn("h-5 w-5", isActive && "text-cyber-primary")} />
                <span>{item.title}</span>
                {item.badge && (
                  <span className="ml-auto rounded-full bg-cyber-primary/20 px-2 py-0.5 text-xs font-semibold text-cyber-primary">
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </div>

        {/* Divider */}
        <div className="my-4 h-px bg-border" />

        {/* Navigation secondaire */}
        <div className="space-y-1">
          {secondaryNavItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all",
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                )}
              >
                <Icon className="h-5 w-5" />
                <span>{item.title}</span>
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Status Footer */}
      <div className="border-t border-border p-4">
        <div className="rounded-lg bg-muted/50 p-3">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-cyber-success animate-pulse-glow" />
            <span className="text-xs font-medium text-muted-foreground">
              System Operational
            </span>
          </div>
          <p className="mt-1 text-xs text-muted-foreground font-mono">
            API: Connected
          </p>
        </div>
      </div>
    </div>
  );
}

