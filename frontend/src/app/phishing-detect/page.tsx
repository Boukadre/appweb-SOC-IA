"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  Mail, 
  Search, 
  AlertTriangle, 
  CheckCircle2, 
  XCircle, 
  ShieldAlert,
  User,
  FileText,
  MessageSquare
} from "lucide-react";
import { getThreatColor, getThreatBgColor } from "@/lib/utils";
import api from "@/services/api";
import { toast } from "sonner";

interface DetectionResult {
  detection_id: string;
  is_phishing: boolean;
  confidence: number;
  threat_category: string;
  indicators: string[];
  threat_level: string;
  recommendations: string[];
  ai_model_used: string;
  timestamp: string;
}

export default function PhishingDetectPage() {
  // Form fields
  const [sender, setSender] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [detectionResult, setDetectionResult] = useState<DetectionResult | null>(null);

  const handleAnalyze = async () => {
    // Validation
    if (!sender && !subject && !body) {
      toast.error("Veuillez remplir au moins un champ");
      return;
    }

    setIsAnalyzing(true);
    setDetectionResult(null);

    const analyzeToast = toast.loading("🤖 Analyse IA en cours...");

    try {
      const result = await api.detectPhishing({
        sender: sender || undefined,
        subject: subject || undefined,
        body: body || undefined,
      });
      
      setDetectionResult(result);
      
      // Toast de succès avec couleur selon la menace
      if (result.threat_category === "phishing") {
        toast.error("🚨 PHISHING DÉTECTÉ !", {
          id: analyzeToast,
          description: `Confiance: ${Math.round(result.confidence * 100)}% • Ne cliquez sur rien !`,
          duration: 8000,
        });
      } else if (result.threat_category === "suspicious") {
        toast.warning("⚠️ Email suspect", {
          id: analyzeToast,
          description: `Confiance: ${Math.round(result.confidence * 100)}% • Soyez prudent`,
          duration: 6000,
        });
      } else {
        toast.success("✅ Email légitime", {
          id: analyzeToast,
          description: `Confiance: ${Math.round(result.confidence * 100)}%`,
          duration: 5000,
        });
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Erreur lors de l'analyse";
      toast.error("❌ Échec de l'analyse", {
        id: analyzeToast,
        description: errorMessage,
        duration: 6000,
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const clearForm = () => {
    setSender("");
    setSubject("");
    setBody("");
    setDetectionResult(null);
  };

  const loadExample = (type: "safe" | "phishing") => {
    if (type === "safe") {
      setSender("noreply@github.com");
      setSubject("Your pull request was merged");
      setBody("Hello! Your pull request #1234 has been successfully merged into the main branch. Thank you for your contribution!");
    } else {
      setSender("support@paypa1-secure.com");
      setSubject("URGENT: Your Account Will Be Suspended");
      setBody("Dear Customer, We have detected unusual activity on your account. Click here immediately to verify your identity or your account will be permanently suspended within 24 hours. Click here: http://paypal-verify.com/secure");
    }
  };

  // Fonction pour obtenir la couleur de la catégorie
  const getCategoryColor = (category: string) => {
    switch (category) {
      case "phishing":
        return "text-cyber-danger";
      case "suspicious":
        return "text-cyber-warning";
      case "safe":
        return "text-cyber-success";
      default:
        return "text-muted-foreground";
    }
  };

  const getCategoryBg = (category: string) => {
    switch (category) {
      case "phishing":
        return "bg-cyber-danger/10 border-cyber-danger/30";
      case "suspicious":
        return "bg-cyber-warning/10 border-cyber-warning/30";
      case "safe":
        return "bg-cyber-success/10 border-cyber-success/30";
      default:
        return "bg-muted/10";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold gradient-text flex items-center gap-3">
          <Mail className="h-10 w-10" />
          Phishing Detection AI
        </h1>
        <p className="text-muted-foreground mt-2">
          Détection avancée de phishing avec modèle BERT fine-tuné
        </p>
      </div>

      {/* Formulaire d'analyse */}
      <Card className="cyber-border">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Analyser un Email</span>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => loadExample("safe")}
                disabled={isAnalyzing}
              >
                Exemple ✅
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => loadExample("phishing")}
                disabled={isAnalyzing}
              >
                Exemple 🚨
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={clearForm}
                disabled={isAnalyzing}
              >
                Effacer
              </Button>
            </div>
          </CardTitle>
          <CardDescription>
            Remplissez au moins un champ pour analyser un email suspect
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Sender */}
            <div>
              <label className="text-sm font-medium flex items-center gap-2">
                <User className="h-4 w-4 text-cyber-primary" />
                Expéditeur (Sender)
              </label>
              <input
                type="email"
                value={sender}
                onChange={(e) => setSender(e.target.value)}
                placeholder="support@example.com"
                className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                disabled={isAnalyzing}
              />
              <p className="text-xs text-muted-foreground mt-1">
                L'adresse email de l'expéditeur
              </p>
            </div>

            {/* Subject */}
            <div>
              <label className="text-sm font-medium flex items-center gap-2">
                <FileText className="h-4 w-4 text-cyber-primary" />
                Objet (Subject)
              </label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Urgent: Verify your account"
                className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                disabled={isAnalyzing}
              />
              <p className="text-xs text-muted-foreground mt-1">
                Le sujet de l'email
              </p>
            </div>

            {/* Body */}
            <div>
              <label className="text-sm font-medium flex items-center gap-2">
                <MessageSquare className="h-4 w-4 text-cyber-primary" />
                Corps du message (Body)
              </label>
              <textarea
                value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder="Collez le contenu de l'email ici..."
                rows={6}
                className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                disabled={isAnalyzing}
              />
              <p className="text-xs text-muted-foreground mt-1">
                Le contenu complet du message
              </p>
            </div>

            <Button
              variant="cyber"
              className="w-full"
              disabled={isAnalyzing}
              onClick={handleAnalyze}
            >
              {isAnalyzing ? (
                <>
                  <ShieldAlert className="mr-2 h-4 w-4 animate-pulse" />
                  Analyse IA en cours...
                </>
              ) : (
                <>
                  <Search className="mr-2 h-4 w-4" />
                  Analyser avec BERT
                </>
              )}
            </Button>

            <div className="text-xs text-muted-foreground flex items-center justify-center gap-2">
              🤖 Propulsé par le modèle BERT fine-tuné pour la détection de phishing
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Results */}
      {detectionResult && (
        <>
          {/* Main Result */}
          <Card className={`cyber-border ${getCategoryBg(detectionResult.threat_category)}`}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-3">
                  {detectionResult.threat_category === "phishing" ? (
                    <XCircle className="h-8 w-8 text-cyber-danger" />
                  ) : detectionResult.threat_category === "suspicious" ? (
                    <AlertTriangle className="h-8 w-8 text-cyber-warning" />
                  ) : (
                    <CheckCircle2 className="h-8 w-8 text-cyber-success" />
                  )}
                  <div>
                    <div className="text-2xl">
                      {detectionResult.threat_category === "phishing" && "🚨 Phishing Détecté"}
                      {detectionResult.threat_category === "suspicious" && "⚠️ Email Suspect"}
                      {detectionResult.threat_category === "safe" && "✅ Email Légitime"}
                    </div>
                    <div className="text-sm font-normal text-muted-foreground mt-1">
                      Modèle: {detectionResult.ai_model_used}
                    </div>
                  </div>
                </span>
                <div className="text-right">
                  <div className={`text-4xl font-bold ${getCategoryColor(detectionResult.threat_category)}`}>
                    {Math.round(detectionResult.confidence * 100)}%
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    Confiance
                  </div>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">Catégorie: </span>
                  <span className={`font-semibold ${getCategoryColor(detectionResult.threat_category)}`}>
                    {detectionResult.threat_category.toUpperCase()}
                  </span>
                </div>
                <div>•</div>
                <div>
                  <span className="text-muted-foreground">Menace: </span>
                  <span className={`font-semibold ${getThreatColor(detectionResult.threat_level)}`}>
                    {detectionResult.threat_level.toUpperCase()}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="grid gap-6 md:grid-cols-2">
            {/* Indicators */}
            <Card className="cyber-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-cyber-warning" />
                  Indicateurs Détectés
                </CardTitle>
                <CardDescription>
                  {detectionResult.indicators.length} élément(s) analysé(s)
                </CardDescription>
              </CardHeader>
              <CardContent>
                {detectionResult.indicators.length > 0 ? (
                  <ul className="space-y-2 max-h-96 overflow-y-auto">
                    {detectionResult.indicators.map((indicator, idx) => (
                      <li
                        key={idx}
                        className="flex items-start gap-3 text-sm rounded-lg border border-border p-3 hover:bg-accent/50 transition-colors"
                      >
                        <span className="mt-0.5">{indicator.startsWith("🤖") || indicator.startsWith("✅") || indicator.startsWith("⚠️") || indicator.startsWith("🔴") ? "" : "•"}</span>
                        <span className="flex-1">{indicator}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-muted-foreground">Aucun indicateur détecté</p>
                )}
              </CardContent>
            </Card>

            {/* Recommendations */}
            <Card className="cyber-border bg-cyber-primary/5">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <ShieldAlert className="h-5 w-5 text-cyber-primary" />
                  Recommandations
                </CardTitle>
                <CardDescription>
                  Actions à prendre
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {detectionResult.recommendations.map((recommendation, idx) => (
                    <li
                      key={idx}
                      className={`flex items-start gap-3 text-sm rounded-lg border p-3 ${
                        recommendation.startsWith("🚫") 
                          ? "border-cyber-danger/30 bg-cyber-danger/5"
                          : recommendation.startsWith("⚠️")
                          ? "border-cyber-warning/30 bg-cyber-warning/5"
                          : "border-border"
                      }`}
                    >
                      <span className="flex-1">{recommendation}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>

          {/* Info Card */}
          <Card className="cyber-border bg-muted/20">
            <CardHeader>
              <CardTitle className="text-sm flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4" />
                Comment fonctionne la détection ?
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-2">
              <p>
                • <strong>Modèle BERT :</strong> Un modèle d'IA de pointe (State Of The Art) spécialement entraîné sur des millions d'emails de phishing
              </p>
              <p>
                • <strong>Analyse contextuelle :</strong> Le modèle analyse l'expéditeur, le sujet et le contenu ensemble pour détecter les patterns suspects
              </p>
              <p>
                • <strong>3 catégories :</strong> Safe (&lt;50%), Suspicious (50-80%), Phishing (&gt;80%)
              </p>
              <p>
                • <strong>Heuristiques complémentaires :</strong> Détection de typosquatting, mots-clés d'urgence, domaines suspects
              </p>
            </CardContent>
          </Card>
        </>
      )}

      {/* Warning */}
      <Card className="cyber-border bg-cyber-warning/5 border-cyber-warning/30">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-cyber-warning">
            <AlertTriangle className="h-5 w-5" />
            Conseils de Sécurité
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="text-sm text-muted-foreground space-y-2">
            <li>✓ En cas de doute, ne cliquez jamais sur les liens</li>
            <li>✓ Vérifiez toujours l'adresse de l'expéditeur</li>
            <li>✓ Les vraies entreprises ne demandent jamais vos mots de passe par email</li>
            <li>✓ Méfiez-vous des messages avec langage d'urgence ou de menace</li>
            <li>✓ Contactez l'entreprise par ses canaux officiels en cas de doute</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
