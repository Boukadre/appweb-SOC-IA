import axios, { AxiosInstance, AxiosError } from "axios";

/**
 * Configuration de l'API client
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Intercepteur pour les requêtes
    this.client.interceptors.request.use(
      (config) => {
        // Ajouter le token d'authentification si disponible
        const token = localStorage.getItem("auth_token");
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Intercepteur pour les réponses
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        // Gestion centralisée des erreurs
        if (error.response?.status === 401) {
          // Redirect to login or refresh token
          localStorage.removeItem("auth_token");
        }
        return Promise.reject(error);
      }
    );
  }

  // ============= NETWORK SCAN =============
  async startNetworkScan(data: {
    target: string;
    scan_type?: string;
    ports?: string;
  }) {
    const response = await this.client.post("/api/network-scan/start", data);
    return response.data;
  }

  async getScanStatus(scanId: string) {
    const response = await this.client.get(`/api/network-scan/status/${scanId}`);
    return response.data;
  }

  async getScanHistory(limit = 10, skip = 0) {
    const response = await this.client.get("/api/network-scan/history", {
      params: { limit, skip },
    });
    return response.data;
  }

  async quickScan(target: string) {
    const response = await this.client.post("/api/network-scan/quick-scan", null, {
      params: { target },
    });
    return response.data;
  }

  async analyzeSSHLogs(logContent: string) {
    const response = await this.client.post("/api/network-scan/ssh-audit", null, {
      params: { log_content: logContent },
    });
    return response.data;
  }

  // ============= MALWARE ANALYSIS =============
  async analyzeMalware(data: {
    file_name: string;
    file_hash?: string;
    analysis_depth?: string;
  }) {
    const response = await this.client.post("/api/malware-analysis/analyze", data);
    return response.data;
  }

  async uploadAndAnalyze(file: File) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await this.client.post("/api/malware-analysis/scan-file", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      timeout: 60000, // 60 secondes pour VirusTotal
    });
    return response.data;
  }

  async getMalwareHistory(limit = 10) {
    const response = await this.client.get("/api/malware-analysis/history", {
      params: { limit },
    });
    return response.data;
  }

  // ============= PHISHING DETECTION =============
  async detectPhishing(data: {
    sender?: string;
    subject?: string;
    body?: string;
    url?: string;
  }) {
    const response = await this.client.post("/api/phishing-detect/analyze", data);
    return response.data;
  }

  async analyzeUrl(url: string) {
    const response = await this.client.post("/api/phishing-detect/analyze-url", null, {
      params: { url },
    });
    return response.data;
  }

  async getPhishingHistory(limit = 10) {
    const response = await this.client.get("/api/phishing-detect/history", {
      params: { limit },
    });
    return response.data;
  }

  // ============= REPORT GENERATION =============
  async generateReport(data: {
    report_type: string;
    analysis_ids: string[];
    format?: string;
    include_recommendations?: boolean;
  }) {
    const response = await this.client.post("/api/report-gen/generate", data);
    return response.data;
  }

  async getReportStatus(reportId: string) {
    const response = await this.client.get(`/api/report-gen/status/${reportId}`);
    return response.data;
  }

  async getReportHistory(limit = 10) {
    const response = await this.client.get("/api/report-gen/history", {
      params: { limit },
    });
    return response.data;
  }

  async downloadReport(reportId: string) {
    const response = await this.client.get(`/api/report-gen/download/${reportId}`, {
      responseType: "blob",
    });
    return response.data;
  }

  // ============= CVE SCANNER =============
  async scanCVE(data: {
    url: string;
    deep_scan?: boolean;
  }) {
    const response = await this.client.post("/api/cve-scanner/scan", data);
    return response.data;
  }

  async getCVEHistory(limit = 10) {
    const response = await this.client.get("/api/cve-scanner/history", {
      params: { limit },
    });
    return response.data;
  }

  async getCVEScan(scanId: string) {
    const response = await this.client.get(`/api/cve-scanner/${scanId}`);
    return response.data;
  }

  // ============= PASSWORD ANALYZER =============
  async analyzePassword(password: string) {
    const response = await this.client.post("/api/password-analyzer/analyze", {
      password,
    });
    return response.data;
  }

  async batchAnalyzePasswords(passwords: string[]) {
    const response = await this.client.post("/api/password-analyzer/batch-analyze", passwords);
    return response.data;
  }

  // ============= HEALTH CHECK =============
  async healthCheck() {
    const response = await this.client.get("/health");
    return response.data;
  }
}

// Export de l'instance singleton
export const api = new ApiClient();
export default api;

