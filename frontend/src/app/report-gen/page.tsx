"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Download } from "lucide-react";

export default function ReportGenPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold gradient-text flex items-center gap-3">
          <FileText className="h-10 w-10" />
          Report Generation
        </h1>
        <p className="text-muted-foreground mt-2">
          Générez des rapports détaillés de vos analyses de sécurité
        </p>
      </div>

      <Card className="cyber-border">
        <CardHeader>
          <CardTitle>Nouveau Rapport</CardTitle>
          <CardDescription>
            Sélectionnez les analyses à inclure dans le rapport
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium">Type de rapport</label>
              <select className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
                <option>Rapport Complet</option>
                <option>Network Scan uniquement</option>
                <option>Malware Analysis uniquement</option>
                <option>Phishing Detection uniquement</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Format</label>
              <select className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
                <option>PDF</option>
                <option>HTML</option>
                <option>JSON</option>
              </select>
            </div>
            <Button variant="cyber" className="w-full">
              <Download className="mr-2 h-4 w-4" />
              Générer le rapport
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

