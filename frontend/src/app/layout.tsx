import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/ui/sidebar";
import { Toaster } from "sonner";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
});

export const metadata: Metadata = {
  title: "Cyber IA Platform - Professional Security Dashboard",
  description: "Plateforme professionnelle d'analyse de sécurité cyber avec Intelligence Artificielle",
  keywords: ["cybersecurity", "AI", "network scan", "malware analysis", "phishing detection"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" className="dark">
      <body
        className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased`}
      >
        <div className="flex h-screen overflow-hidden bg-background grid-background">
          {/* Sidebar Navigation */}
          <Sidebar />

          {/* Main Content Area */}
          <main className="flex-1 overflow-y-auto">
            <div className="container mx-auto p-6 space-y-6">
              {children}
            </div>
          </main>
        </div>
        
        {/* Toast Notifications */}
        <Toaster 
          position="top-right"
          expand={true}
          richColors
          closeButton
          theme="dark"
        />
      </body>
    </html>
  );
}

