"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  Network, 
  Play, 
  AlertCircle, 
  CheckCircle2, 
  Loader2, 
  Shield,
  Upload,
  TrendingDown,
  Globe,
  Target
} from "lucide-react";
import { getThreatColor, getThreatBgColor } from "@/lib/utils";
import api from "@/services/api";
import { toast } from "sonner";

interface ScanResult {
  scan_id: string;
  status: string;
  target: string;
  open_ports: number[];
  vulnerabilities: Array<{
    port: number;
    service: string;
    description: string;
    severity: string;
  }>;
  threat_level: string;
  timestamp: string;
}

interface SSHAuditResult {
  analysis_id: string;
  total_attacks: number;
  unique_attackers: number;
  top_attackers: Array<{
    ip: string;
    attempts: number;
    percentage: number;
    abuse_score?: number;
    country?: string;
  }>;
  attack_patterns: Array<{
    type: string;
    description: string;
    severity: string;
  }>;
  recommendations: string[];
  threat_level: string;
  timestamp: string;
}

type TabType = "port-scan" | "ssh-audit";

export default function NetworkScanPage() {
  const [activeTab, setActiveTab] = useState<TabType>("port-scan");
  
  // Port Scan State
  const [target, setTarget] = useState("");
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);

  // SSH Audit State
  const [sshLogs, setSSHLogs] = useState("");
  const [isAnalyzingSSH, setIsAnalyzingSSH] = useState(false);
  const [sshResult, setSSHResult] = useState<SSHAuditResult | null>(null);

  // Port Scan Handler
  const handleScan = async () => {
    if (!target) {
      toast.error("Veuillez entrer une cible (IP ou domaine)");
      return;
    }

    setIsScanning(true);
    setScanResult(null);

    const scanToast = toast.loading("🔍 Scan réseau en cours...");

    try {
      const result = await api.quickScan(target);
      setScanResult(result);
      
      toast.success("✅ Scan terminé avec succès", {
        id: scanToast,
        description: `Niveau de menace: ${result.threat_level.toUpperCase()} • ${result.open_ports.length} port(s) ouvert(s)`,
        duration: 5000,
      });
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Erreur lors du scan réseau";
      toast.error("❌ Échec du scan", {
        id: scanToast,
        description: errorMessage,
        duration: 6000,
      });
    } finally {
      setIsScanning(false);
    }
  };

  // SSH Audit Handler
  const handleSSHAnalysis = async () => {
    if (!sshLogs.trim()) {
      toast.error("Veuillez coller le contenu de vos logs SSH");
      return;
    }

    setIsAnalyzingSSH(true);
    setSSHResult(null);

    const auditToast = toast.loading("🔍 Analyse des logs SSH en cours...");

    try {
      const result = await api.analyzeSSHLogs(sshLogs);
      setSSHResult(result);
      
      toast.success("✅ Analyse terminée", {
        id: auditToast,
        description: `${result.total_attacks} tentatives détectées • Niveau: ${result.threat_level.toUpperCase()}`,
        duration: 5000,
      });
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Erreur lors de l'analyse";
      toast.error("❌ Échec de l'analyse", {
        id: auditToast,
        description: errorMessage,
        duration: 6000,
      });
    } finally {
      setIsAnalyzingSSH(false);
    }
  };

  // File Upload Handler (for SSH logs)
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      setSSHLogs(content);
      toast.success(`📄 Fichier chargé: ${file.name}`);
    };
    reader.readAsText(file);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold gradient-text flex items-center gap-3">
          <Network className="h-10 w-10" />
          Network Security Scanner
        </h1>
        <p className="text-muted-foreground mt-2">
          Analysez votre réseau et détectez les tentatives d'intrusion SSH
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-border">
        <button
          onClick={() => setActiveTab("port-scan")}
          className={`px-6 py-3 font-medium transition-colors border-b-2 ${
            activeTab === "port-scan"
              ? "border-cyber-primary text-cyber-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          }`}
        >
          <Target className="inline-block h-4 w-4 mr-2" />
          Port Scan
        </button>
        <button
          onClick={() => setActiveTab("ssh-audit")}
          className={`px-6 py-3 font-medium transition-colors border-b-2 ${
            activeTab === "ssh-audit"
              ? "border-cyber-primary text-cyber-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          }`}
        >
          <Shield className="inline-block h-4 w-4 mr-2" />
          SSH Log Audit
        </button>
      </div>

      {/* PORT SCAN TAB */}
      {activeTab === "port-scan" && (
        <>
          <Card className="cyber-border">
            <CardHeader>
              <CardTitle>Scan de Ports</CardTitle>
              <CardDescription>
                Entrez l'adresse IP ou le domaine à scanner
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Cible</label>
                  <input
                    type="text"
                    value={target}
                    onChange={(e) => setTarget(e.target.value)}
                    placeholder="192.168.1.1 ou example.com"
                    className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                    disabled={isScanning}
                    onKeyPress={(e) => e.key === "Enter" && handleScan()}
                  />
                </div>

                <Button 
                  variant="cyber" 
                  className="w-full" 
                  disabled={isScanning}
                  onClick={handleScan}
                >
                  {isScanning ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Scan en cours...
                    </>
                  ) : (
                    <>
                      <Play className="mr-2 h-4 w-4" />
                      Démarrer le scan
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Port Scan Results */}
          {scanResult && (
            <>
              <Card className={`cyber-border ${getThreatBgColor(scanResult.threat_level)}`}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>Résultat du scan</span>
                    <span className={`text-2xl font-bold ${getThreatColor(scanResult.threat_level)}`}>
                      {scanResult.threat_level.toUpperCase()}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Cible: <span className="font-mono">{scanResult.target}</span> • 
                    {scanResult.open_ports.length} port(s) ouvert(s) • 
                    {scanResult.vulnerabilities.length} vulnérabilité(s)
                  </p>
                </CardContent>
              </Card>

              <div className="grid gap-6 md:grid-cols-2">
                {/* Open Ports */}
                <Card className="cyber-border">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <CheckCircle2 className="h-5 w-5 text-cyber-primary" />
                      Ports Ouverts
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {scanResult.open_ports.length > 0 ? (
                      <div className="flex flex-wrap gap-2">
                        {scanResult.open_ports.map((port) => (
                          <span
                            key={port}
                            className="inline-flex items-center rounded-md bg-cyber-primary/10 px-3 py-1 text-sm font-mono text-cyber-primary border border-cyber-primary/30"
                          >
                            {port}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-muted-foreground">Aucun port ouvert détecté</p>
                    )}
                  </CardContent>
                </Card>

                {/* Vulnerabilities */}
                <Card className="cyber-border">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <AlertCircle className="h-5 w-5 text-cyber-danger" />
                      Vulnérabilités
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {scanResult.vulnerabilities.length > 0 ? (
                      <div className="space-y-2">
                        {scanResult.vulnerabilities.map((vuln, idx) => (
                          <div
                            key={idx}
                            className={`rounded-lg border p-3 ${getThreatBgColor(vuln.severity)}`}
                          >
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-mono text-sm">Port {vuln.port}</span>
                              <span className={`text-xs font-semibold ${getThreatColor(vuln.severity)}`}>
                                {vuln.severity.toUpperCase()}
                              </span>
                            </div>
                            <p className="text-xs text-muted-foreground">{vuln.service}</p>
                            <p className="text-sm mt-1">{vuln.description}</p>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-muted-foreground">Aucune vulnérabilité détectée</p>
                    )}
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </>
      )}

      {/* SSH AUDIT TAB */}
      {activeTab === "ssh-audit" && (
        <>
          <Card className="cyber-border">
            <CardHeader>
              <CardTitle>Analyse des Logs SSH</CardTitle>
              <CardDescription>
                Analysez les tentatives d'intrusion dans vos logs SSH (auth.log, secure)
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Contenu des logs SSH</label>
                  <textarea
                    value={sshLogs}
                    onChange={(e) => setSSHLogs(e.target.value)}
                    placeholder="Collez le contenu de votre fichier /var/log/auth.log ou /var/log/secure ici..."
                    className="mt-1 w-full h-48 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring font-mono"
                    disabled={isAnalyzingSSH}
                  />
                  <p className="text-xs text-muted-foreground mt-1">
                    💡 Exemple de commande: <code className="bg-muted px-1 rounded">sudo cat /var/log/auth.log</code>
                  </p>
                </div>

                <div className="flex gap-2">
                  <Button 
                    variant="cyber" 
                    className="flex-1" 
                    disabled={isAnalyzingSSH}
                    onClick={handleSSHAnalysis}
                  >
                    {isAnalyzingSSH ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Analyse en cours...
                      </>
                    ) : (
                      <>
                        <Shield className="mr-2 h-4 w-4" />
                        Analyser les logs
                      </>
                    )}
                  </Button>
                  
                  <label className="cursor-pointer">
                    <Button 
                      variant="outline" 
                      disabled={isAnalyzingSSH}
                      asChild
                    >
                      <span>
                        <Upload className="mr-2 h-4 w-4" />
                        Charger un fichier
                      </span>
                    </Button>
                    <input
                      type="file"
                      accept=".log,.txt"
                      onChange={handleFileUpload}
                      className="hidden"
                      disabled={isAnalyzingSSH}
                    />
                  </label>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* SSH Audit Results */}
          {sshResult && (
            <>
              {/* Threat Overview */}
              <Card className={`cyber-border ${getThreatBgColor(sshResult.threat_level)}`}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>Analyse des Tentatives d'Intrusion</span>
                    <span className={`text-2xl font-bold ${getThreatColor(sshResult.threat_level)}`}>
                      {sshResult.threat_level.toUpperCase()}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-muted-foreground">Total d'attaques</p>
                      <p className="text-3xl font-bold gradient-text">{sshResult.total_attacks}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Attaquants uniques</p>
                      <p className="text-3xl font-bold gradient-text">{sshResult.unique_attackers}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="grid gap-6 md:grid-cols-2">
                {/* Top Attackers */}
                <Card className="cyber-border">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingDown className="h-5 w-5 text-cyber-danger" />
                      Top Attaquants
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {sshResult.top_attackers.slice(0, 10).map((attacker, idx) => (
                        <div
                          key={idx}
                          className="rounded-lg border border-border p-3 hover:bg-accent/50 transition-colors"
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-mono text-sm font-bold">{attacker.ip}</span>
                            <div className="flex items-center gap-2">
                              {attacker.country && (
                                <span className="text-xs bg-muted px-2 py-0.5 rounded">
                                  <Globe className="inline h-3 w-3 mr-1" />
                                  {attacker.country}
                                </span>
                              )}
                              <span className="text-xs font-semibold text-cyber-danger">
                                {attacker.attempts} tentatives
                              </span>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
                              <div
                                className="h-full bg-cyber-danger"
                                style={{ width: `${attacker.percentage}%` }}
                              />
                            </div>
                            <span className="text-xs text-muted-foreground">
                              {attacker.percentage}%
                            </span>
                          </div>
                          {attacker.abuse_score !== undefined && attacker.abuse_score > 0 && (
                            <p className="text-xs text-cyber-warning mt-1">
                              ⚠️ Score d'abus: {attacker.abuse_score}%
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Attack Patterns */}
                <Card className="cyber-border">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <AlertCircle className="h-5 w-5 text-cyber-warning" />
                      Patterns d'Attaque
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {sshResult.attack_patterns.map((pattern, idx) => (
                        <div
                          key={idx}
                          className={`rounded-lg border p-3 ${getThreatBgColor(pattern.severity)}`}
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm font-semibold">{pattern.type.toUpperCase()}</span>
                            <span className={`text-xs font-bold ${getThreatColor(pattern.severity)}`}>
                              {pattern.severity.toUpperCase()}
                            </span>
                          </div>
                          <p className="text-sm text-muted-foreground">{pattern.description}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Recommendations */}
              <Card className="cyber-border bg-cyber-primary/5">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Shield className="h-5 w-5 text-cyber-primary" />
                    Recommandations de Sécurité
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {sshResult.recommendations.map((rec, idx) => (
                      <li
                        key={idx}
                        className="text-sm border border-border rounded-lg p-3 hover:bg-accent/50 transition-colors"
                      >
                        {rec}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </>
          )}
        </>
      )}

      {/* Warning Note */}
      <Card className="cyber-border bg-cyber-warning/5 border-cyber-warning/30">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-cyber-warning">
            <AlertCircle className="h-5 w-5" />
            Note importante
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Assurez-vous d'avoir l'autorisation nécessaire avant de scanner un réseau.
            Le scan non autorisé peut être illégal. Les logs SSH peuvent contenir des informations sensibles.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
