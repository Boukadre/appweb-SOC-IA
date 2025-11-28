"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { StatsCard } from "@/components/dashboard/stats-card";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Activity,
  Shield,
  Network,
  Mail,
  AlertTriangle,
  CheckCircle2,
  TrendingUp,
  Clock,
  Key,
  FileSearch,
} from "lucide-react";
import api from "@/services/api";

export default function DashboardPage() {
  const [systemStatus, setSystemStatus] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch system health on mount
    const checkHealth = async () => {
      try {
        const health = await api.healthCheck();
        setSystemStatus(health);
      } catch (error) {
        console.error("Failed to fetch health:", error);
      } finally {
        setIsLoading(false);
      }
    };

    checkHealth();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold gradient-text">
            Security Operations Center
          </h1>
          <p className="text-muted-foreground mt-2">
            Vue d'ensemble des menaces et analyses en temps réel
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            <Clock className="mr-2 h-4 w-4" />
            Dernières 24h
          </Button>
          <Button variant="cyber" size="sm" asChild>
            <Link href="/network-scan">
              <Activity className="mr-2 h-4 w-4" />
              Nouvelle Analyse
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Analyses"
          value="2,847"
          description="Analyses effectuées ce mois"
          icon={Activity}
          trend={{ value: 12.5, isPositive: true }}
        />
        <StatsCard
          title="Menaces Détectées"
          value="143"
          description="Nécessitent une attention"
          icon={AlertTriangle}
          trend={{ value: -8.2, isPositive: true }}
          className="border-cyber-danger/30"
        />
        <StatsCard
          title="Scans Réseau"
          value="1,024"
          description="Ports analysés aujourd'hui"
          icon={Network}
          trend={{ value: 18.1, isPositive: true }}
        />
        <StatsCard
          title="Taux de Sécurité"
          value="94.7%"
          description="Score global du système"
          icon={Shield}
          trend={{ value: 2.4, isPositive: true }}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Recent Activities */}
        <Card className="col-span-2 cyber-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-cyber-primary" />
              Activités Récentes
            </CardTitle>
            <CardDescription>
              Dernières analyses et détections de menaces
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                {
                  type: "network",
                  title: "Scan réseau terminé",
                  target: "192.168.1.0/24",
                  status: "success",
                  time: "Il y a 2 minutes",
                },
                {
                  type: "malware",
                  title: "Fichier suspect détecté",
                  target: "suspicious_file.exe",
                  status: "warning",
                  time: "Il y a 15 minutes",
                },
                {
                  type: "phishing",
                  title: "URL malveillante bloquée",
                  target: "hxxp://phishing-site[.]com",
                  status: "danger",
                  time: "Il y a 1 heure",
                },
                {
                  type: "report",
                  title: "Rapport mensuel généré",
                  target: "Report_November_2025.pdf",
                  status: "success",
                  time: "Il y a 3 heures",
                },
              ].map((activity, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-4 rounded-lg border border-border p-4 transition-colors hover:bg-accent/50"
                >
                  <div
                    className={`mt-0.5 rounded-full p-2 ${
                      activity.status === "success"
                        ? "bg-cyber-success/10"
                        : activity.status === "warning"
                        ? "bg-cyber-warning/10"
                        : "bg-cyber-danger/10"
                    }`}
                  >
                    {activity.type === "network" && (
                      <Network className="h-4 w-4 text-cyber-primary" />
                    )}
                    {activity.type === "malware" && (
                      <Shield className="h-4 w-4 text-cyber-warning" />
                    )}
                    {activity.type === "phishing" && (
                      <Mail className="h-4 w-4 text-cyber-danger" />
                    )}
                    {activity.type === "report" && (
                      <CheckCircle2 className="h-4 w-4 text-cyber-success" />
                    )}
                  </div>
                  <div className="flex-1 space-y-1">
                    <p className="text-sm font-medium leading-none">
                      {activity.title}
                    </p>
                    <p className="text-sm text-muted-foreground font-mono">
                      {activity.target}
                    </p>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {activity.time}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Threat Distribution */}
        <Card className="cyber-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-cyber-primary" />
              Distribution des Menaces
            </CardTitle>
            <CardDescription>Par niveau de sévérité</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { level: "Critical", count: 12, color: "bg-destructive", percent: 8 },
                { level: "High", count: 38, color: "bg-cyber-danger", percent: 27 },
                { level: "Medium", count: 61, color: "bg-cyber-warning", percent: 43 },
                { level: "Low", count: 32, color: "bg-cyber-success", percent: 22 },
              ].map((threat) => (
                <div key={threat.level} className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">{threat.level}</span>
                    <span className="text-muted-foreground">
                      {threat.count} ({threat.percent}%)
                    </span>
                  </div>
                  <div className="h-2 rounded-full bg-muted overflow-hidden">
                    <div
                      className={`h-full ${threat.color} transition-all duration-500`}
                      style={{ width: `${threat.percent}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions - CÂBLÉES avec les vrais liens */}
      <Card className="cyber-border bg-gradient-to-br from-cyber-primary/5 to-cyber-secondary/5">
        <CardHeader>
          <CardTitle>Actions Rapides</CardTitle>
          <CardDescription>
            Lancez rapidement une analyse de sécurité
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
            {/* Network Scan */}
            <Button
              variant="outline"
              className="h-auto flex-col items-start gap-2 p-4 hover:bg-cyber-primary/10 hover:border-cyber-primary/50 transition-all"
              asChild
            >
              <Link href="/network-scan">
                <Network className="h-6 w-6 text-cyber-primary" />
                <div className="text-left w-full">
                  <div className="font-semibold">Network Scan</div>
                  <div className="text-xs text-muted-foreground">
                    Analyser le réseau
                  </div>
                </div>
              </Link>
            </Button>

            {/* Malware Analysis */}
            <Button
              variant="outline"
              className="h-auto flex-col items-start gap-2 p-4 hover:bg-cyber-primary/10 hover:border-cyber-primary/50 transition-all"
              asChild
            >
              <Link href="/malware-analysis">
                <Shield className="h-6 w-6 text-cyber-primary" />
                <div className="text-left w-full">
                  <div className="font-semibold">Malware Scan</div>
                  <div className="text-xs text-muted-foreground">
                    Analyser un fichier
                  </div>
                </div>
              </Link>
            </Button>

            {/* Password Analyzer */}
            <Button
              variant="outline"
              className="h-auto flex-col items-start gap-2 p-4 hover:bg-cyber-primary/10 hover:border-cyber-primary/50 transition-all"
              asChild
            >
              <Link href="/password-analyzer">
                <Key className="h-6 w-6 text-cyber-primary" />
                <div className="text-left w-full">
                  <div className="font-semibold">Password Test</div>
                  <div className="text-xs text-muted-foreground">
                    Test de force
                  </div>
                </div>
              </Link>
            </Button>

            {/* Phishing Detection */}
            <Button
              variant="outline"
              className="h-auto flex-col items-start gap-2 p-4 hover:bg-cyber-primary/10 hover:border-cyber-primary/50 transition-all"
              asChild
            >
              <Link href="/phishing-detect">
                <Mail className="h-6 w-6 text-cyber-primary" />
                <div className="text-left w-full">
                  <div className="font-semibold">Phishing Check</div>
                  <div className="text-xs text-muted-foreground">
                    Vérifier un email
                  </div>
                </div>
              </Link>
            </Button>

            {/* CVE Scanner */}
            <Button
              variant="outline"
              className="h-auto flex-col items-start gap-2 p-4 hover:bg-cyber-primary/10 hover:border-cyber-primary/50 transition-all"
              asChild
            >
              <Link href="/cve-scanner">
                <FileSearch className="h-6 w-6 text-cyber-primary" />
                <div className="text-left w-full">
                  <div className="font-semibold">CVE Scanner</div>
                  <div className="text-xs text-muted-foreground">
                    Scan vulnérabilités
                  </div>
                </div>
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
