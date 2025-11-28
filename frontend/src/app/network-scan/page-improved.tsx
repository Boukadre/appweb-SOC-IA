"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Network, Play, AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
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

export default function NetworkScanPage() {
  const [target, setTarget] = useState("");
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);

  const handleScan = async () => {
    if (!target) {
      toast.error("Veuillez entrer une cible (IP ou domaine)");
      return;
    }

    setIsScanning(true);
    setScanResult(null);

    // Toast de début
    const scanToast = toast.loading("🔍 Scan réseau en cours...");

    try {
      const result = await api.quickScan(target);
      setScanResult(result);
      
      // Toast de succès avec niveau de menace
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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold gradient-text flex items-center gap-3">
          <Network className="h-10 w-10" />
          Network Scan
        </h1>
        <p className="text-muted-foreground mt-2">
          Analysez votre réseau pour détecter les vulnérabilités et les ports ouverts
        </p>
      </div>

      <Card className="cyber-border">
        <CardHeader>
          <CardTitle>Nouveau Scan</CardTitle>
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

      {/* Results */}
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
            Le scan non autorisé peut être illégal.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}



