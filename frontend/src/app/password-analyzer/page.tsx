"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Key, Eye, EyeOff, AlertCircle, CheckCircle2, Clock, Shield, Loader2 } from "lucide-react";
import api from "@/services/api";
import { toast } from "sonner";

interface PasswordAnalysis {
  score: number;
  strength: string;
  crack_time_seconds: number;
  crack_time_display: string;
  entropy: number;
  suggestions: string[];
  warning: string | null;
  feedback: any;
  timestamp: string;
}

// Configuration des couleurs selon le score (style cyber cohérent)
const strengthColors = {
  0: { bg: "bg-destructive", text: "text-destructive", label: "Très Faible", barColor: "bg-destructive" },
  1: { bg: "bg-cyber-danger", text: "text-cyber-danger", label: "Faible", barColor: "bg-cyber-danger" },
  2: { bg: "bg-cyber-warning", text: "text-cyber-warning", label: "Moyen", barColor: "bg-cyber-warning" },
  3: { bg: "bg-cyber-success", text: "text-cyber-success", label: "Fort", barColor: "bg-cyber-success" },
  4: { bg: "bg-cyber-primary", text: "text-cyber-primary", label: "Très Fort", barColor: "bg-cyber-primary" },
};

export default function PasswordAnalyzerPage() {
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<PasswordAnalysis | null>(null);

  // Fonction d'analyse
  const handleAnalyze = async () => {
    if (!password || password.trim() === "") {
      toast.error("Veuillez entrer un mot de passe");
      return;
    }

    setIsAnalyzing(true);
    setAnalysis(null);

    const analyzeToast = toast.loading("🔍 Analyse en cours...");

    try {
      const result = await api.analyzePassword(password);
      setAnalysis(result);
      
      toast.success("✅ Analyse terminée", {
        id: analyzeToast,
        description: `Force: ${strengthColors[result.score as keyof typeof strengthColors].label}`,
        duration: 3000,
      });
      
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || "Erreur lors de l'analyse";
      toast.error("❌ Échec de l'analyse", {
        id: analyzeToast,
        description: errorMessage,
        duration: 6000,
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getStrengthConfig = (score: number) => {
    return strengthColors[score as keyof typeof strengthColors] || strengthColors[0];
  };

  const strengthConfig = analysis ? getStrengthConfig(analysis.score) : null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold gradient-text flex items-center gap-3">
          <Key className="h-10 w-10" />
          Password Strength Analyzer
        </h1>
        <p className="text-muted-foreground mt-2">
          Analysez la robustesse de vos mots de passe avec IA
        </p>
      </div>

      {/* Formulaire Principal */}
      <Card className="cyber-border">
        <CardHeader>
          <CardTitle>Testez votre mot de passe</CardTitle>
          <CardDescription>
            Entrez un mot de passe pour analyser sa force et obtenir des conseils
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Input Password */}
            <div>
              <label className="text-sm font-medium mb-2 block">Mot de passe</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleAnalyze()}
                  placeholder="Entrez un mot de passe..."
                  className="w-full rounded-md border border-input bg-background px-4 py-3 pr-12 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring font-mono"
                  disabled={isAnalyzing}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                ℹ️ Votre mot de passe n'est jamais enregistré
              </p>
            </div>

            {/* Bouton Analyser */}
            <Button
              onClick={handleAnalyze}
              disabled={isAnalyzing || !password}
              variant="cyber"
              className="w-full"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyse en cours...
                </>
              ) : (
                <>
                  <Shield className="mr-2 h-4 w-4" />
                  Analyser le mot de passe
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Résultats de l'analyse */}
      {analysis && strengthConfig && (
        <>
          {/* Carte Score avec Jauge Animée */}
          <Card className={`cyber-border ${strengthConfig.bg}/10`}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Force du mot de passe</span>
                <span className={`text-3xl font-bold ${strengthConfig.text}`}>
                  {strengthConfig.label}
                </span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Barre de progression COLORÉE avec animation */}
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Score: {analysis.score}/4</span>
                  <span>{Math.round((analysis.score / 4) * 100)}%</span>
                </div>
                <div className="h-4 rounded-full bg-muted overflow-hidden">
                  <div
                    className={`h-full ${strengthConfig.barColor} transition-all duration-500 ease-out`}
                    style={{ width: `${(analysis.score / 4) * 100}%` }}
                  />
                </div>
                
                {/* Indicateurs visuels */}
                <div className="flex justify-between">
                  {[0, 1, 2, 3, 4].map((score) => (
                    <div
                      key={score}
                      className={`h-2 w-2 rounded-full transition-colors ${
                        analysis.score >= score
                          ? getStrengthConfig(score).barColor
                          : "bg-muted"
                      }`}
                    />
                  ))}
                </div>
              </div>

              {/* Warning */}
              {analysis.warning && (
                <div className={`rounded-md border p-3 ${
                  analysis.score <= 1 
                    ? "bg-cyber-danger/10 border-cyber-danger/30" 
                    : "bg-cyber-warning/10 border-cyber-warning/30"
                }`}>
                  <p className={`text-sm flex items-center gap-2 ${
                    analysis.score <= 1 ? "text-cyber-danger" : "text-cyber-warning"
                  }`}>
                    <AlertCircle className="h-4 w-4" />
                    {analysis.warning}
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Statistiques détaillées */}
          <div className="grid gap-4 md:grid-cols-3">
            {/* Temps de crackage - GROS ET EN GRAS */}
            <Card className="cyber-border">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                  <Clock className="h-4 w-4 text-cyber-primary" />
                  Temps de crackage
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold gradient-text">
                  {analysis.crack_time_display}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Attaque par force brute
                </p>
              </CardContent>
            </Card>

            {/* Entropie */}
            <Card className="cyber-border">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                  <Shield className="h-4 w-4 text-cyber-primary" />
                  Entropie
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold gradient-text">
                  {analysis.entropy.toFixed(1)}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  bits d'imprévisibilité
                </p>
              </CardContent>
            </Card>

            {/* Tentatives */}
            <Card className="cyber-border">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-cyber-primary" />
                  Tentatives
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold gradient-text">
                  {analysis.feedback.guesses.toLocaleString()}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Estimées pour cracker
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Conseils d'amélioration */}
          {analysis.suggestions.length > 0 && (
            <Card className="cyber-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertCircle className="h-5 w-5 text-cyber-warning" />
                  Conseils d'amélioration
                </CardTitle>
                <CardDescription>
                  Comment rendre votre mot de passe plus sûr
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {analysis.suggestions.map((suggestion, idx) => (
                    <li
                      key={idx}
                      className="flex items-start gap-3 text-sm rounded-lg border border-border p-3 hover:bg-accent/50 transition-colors"
                    >
                      <span className="text-cyber-warning mt-0.5">•</span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Bonnes pratiques */}
          <Card className="cyber-border bg-cyber-primary/5">
            <CardHeader>
              <CardTitle className="text-sm">💡 Bonnes pratiques de sécurité</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="text-sm text-muted-foreground space-y-2">
                <li>✓ Utilisez au moins 12-16 caractères</li>
                <li>✓ Mélangez majuscules, minuscules, chiffres et symboles</li>
                <li>✓ Évitez les mots du dictionnaire et les informations personnelles</li>
                <li>✓ Utilisez un gestionnaire de mots de passe</li>
                <li>✓ Activez l'authentification à deux facteurs (2FA)</li>
              </ul>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
