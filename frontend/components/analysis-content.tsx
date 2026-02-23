"use client"

import { useState, useCallback, useRef } from "react"
import Link from "next/link"
import { Download, Upload, FileText, BarChart3 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { getCurrentAnalysis } from "@/lib/analysis-store"
import { DocumentViewer } from "@/components/document-viewer"
import { ClausePanel } from "@/components/clause-panel"

export function AnalysisContent() {
  const analysis = getCurrentAnalysis()
  const [selectedClause, setSelectedClause] = useState<string | null>(null)
  const downloadLinkRef = useRef<HTMLAnchorElement>(null)

  const handleClauseSelect = useCallback((id: string) => {
    setSelectedClause((prev) => (prev === id ? null : id))
  }, [])

  const handleDownload = useCallback(() => {
    if (!analysis) return

    // Create a text report for download
    const report = [
      "LEXAI Legal Document Analysis Report",
      "=".repeat(50),
      "",
      `Document: ${analysis.filename}`,
      `Constitution: ${analysis.constitution}`,
      `Analysis Date: ${new Date().toLocaleDateString()}`,
      `Total Clauses: ${analysis.document_stats.total_clauses}`,
      "",
      "Summary",
      "-".repeat(30),
      `High Priority Clauses: ${analysis.summary.high_priority_count}`,
      `Medium Priority Clauses: ${analysis.summary.medium_priority_count}`,
      `Low Priority Clauses: ${analysis.summary.low_priority_count}`,
      `Clause Types: ${analysis.summary.clause_types.join(", ")}`,
      "",
      "Detailed Clause Analysis",
      "-".repeat(30),
      "",
      ...analysis.clauses.map((clause) => [
        `[${clause.clause_id}] Rank #${clause.rank} - ${clause.type.toUpperCase()}`,
        `Priority: ${clause.color === "red" ? "CRITICAL" : clause.color === "yellow" ? "MODERATE" : "LOW"} (${(clause.priority_score * 100).toFixed(0)}%)`,
        `Text: ${clause.text}`,
        `AI Analysis: This ${clause.type} clause carries ${clause.color === "red" ? "significant legal risk" : clause.color === "yellow" ? "moderate importance" : "standard standing"} under the ${analysis.constitution} Constitution.`,
        "",
      ]).flat(),
    ].join("\n")

    const blob = new Blob([report], { type: "text/plain" })
    const url = URL.createObjectURL(blob)

    if (downloadLinkRef.current) {
      downloadLinkRef.current.href = url
      downloadLinkRef.current.download = `LEXAI_Analysis_${analysis.filename.replace(/\.[^/.]+$/, "")}.txt`
      downloadLinkRef.current.click()
    }

    URL.revokeObjectURL(url)
  }, [analysis])

  // No analysis available
  if (!analysis) {
    return (
      <div className="flex flex-col items-center justify-center gap-6 p-8 min-h-[60vh]">
        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-secondary">
          <FileText className="h-10 w-10 text-muted-foreground" />
        </div>
        <div className="text-center">
          <h2 className="text-xl font-semibold text-foreground">No Analysis Available</h2>
          <p className="mt-2 text-sm text-muted-foreground max-w-md">
            Upload a legal document and run analysis to view results here.
          </p>
        </div>
        <Button asChild>
          <Link href="/upload" className="gap-2">
            <Upload className="h-4 w-4" />
            Upload Document
          </Link>
        </Button>
      </div>
    )
  }

  return (
    <div className="flex h-screen flex-col">
      {/* Top bar */}
      <div className="flex items-center justify-between border-b border-border px-6 py-3">
        <div className="flex items-center gap-3">
          <FileText className="h-5 w-5 text-primary" />
          <div>
            <h1 className="text-sm font-semibold text-foreground">{analysis.filename}</h1>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="text-[10px]">
                {analysis.constitution}
              </Badge>
              <span className="text-xs text-muted-foreground">
                {analysis.document_stats.total_clauses} clauses
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Stats badges */}
          <div className="hidden md:flex items-center gap-2 mr-4">
            <div className="flex items-center gap-1.5 rounded-md bg-destructive/10 px-2 py-1">
              <div className="h-2 w-2 rounded-full bg-destructive" />
              <span className="text-xs font-medium text-destructive">
                {analysis.summary.high_priority_count}
              </span>
            </div>
            <div className="flex items-center gap-1.5 rounded-md bg-chart-3/10 px-2 py-1">
              <div className="h-2 w-2 rounded-full bg-chart-3" />
              <span className="text-xs font-medium text-chart-3">
                {analysis.summary.medium_priority_count}
              </span>
            </div>
            <div className="flex items-center gap-1.5 rounded-md bg-chart-2/10 px-2 py-1">
              <div className="h-2 w-2 rounded-full bg-chart-2" />
              <span className="text-xs font-medium text-chart-2">
                {analysis.summary.low_priority_count}
              </span>
            </div>
          </div>

          <Button variant="outline" size="sm" className="gap-2" onClick={handleDownload}>
            <Download className="h-4 w-4" />
            <span className="hidden sm:inline">Download Report</span>
          </Button>
          <Button size="sm" asChild>
            <Link href="/upload" className="gap-2">
              <Upload className="h-4 w-4" />
              <span className="hidden sm:inline">New Analysis</span>
            </Link>
          </Button>
        </div>
      </div>

      {/* Hidden download link */}
      <a ref={downloadLinkRef} className="hidden" aria-hidden="true" />

      {/* Main content: split view */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: Document Viewer */}
        <div className="flex-1 p-4 overflow-hidden">
          {analysis.imageUrl ? (
            <DocumentViewer
              imageUrl={analysis.imageUrl}
              clauses={analysis.clauses}
              selectedClause={selectedClause}
              onClauseClick={handleClauseSelect}
            />
          ) : (
            <Card className="flex h-full items-center justify-center">
              <CardContent className="text-center">
                <BarChart3 className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                <CardTitle className="text-lg mb-2">Document Preview</CardTitle>
                <CardDescription>
                  Document image not available. View clause analysis in the right panel.
                </CardDescription>

                {/* Summary stats */}
                <div className="mt-6 grid grid-cols-3 gap-4">
                  <div className="rounded-lg bg-destructive/10 p-3">
                    <p className="text-2xl font-bold text-destructive">
                      {analysis.summary.high_priority_count}
                    </p>
                    <p className="text-xs text-muted-foreground">Critical</p>
                  </div>
                  <div className="rounded-lg bg-chart-3/10 p-3">
                    <p className="text-2xl font-bold text-chart-3">
                      {analysis.summary.medium_priority_count}
                    </p>
                    <p className="text-xs text-muted-foreground">Moderate</p>
                  </div>
                  <div className="rounded-lg bg-chart-2/10 p-3">
                    <p className="text-2xl font-bold text-chart-2">
                      {analysis.summary.low_priority_count}
                    </p>
                    <p className="text-xs text-muted-foreground">Info</p>
                  </div>
                </div>

                <div className="mt-4 flex flex-wrap justify-center gap-2">
                  {analysis.summary.clause_types.map((type) => (
                    <Badge key={type} variant="outline" className="capitalize">
                      {type}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Right: Clause Panel */}
        <div className="w-96 border-l border-border overflow-hidden">
          <ClausePanel
            clauses={analysis.clauses}
            selectedClause={selectedClause}
            onClauseSelect={handleClauseSelect}
            constitution={analysis.constitution}
          />
        </div>
      </div>
    </div>
  )
}
