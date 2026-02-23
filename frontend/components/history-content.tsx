"use client"

import { useState, useMemo } from "react"
import Link from "next/link"
import {
  FileText,
  Upload,
  Trash2,
  Search,
  Calendar,
  Scale,
  ChevronRight,
  ClipboardList,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { getHistory, clearHistory } from "@/lib/analysis-store"
import type { HistoryItem } from "@/lib/types"

function getConstitutionBadgeClass(constitution?: string) {
  switch (constitution) {
    case "India":
      return "bg-orange-500/15 text-orange-400 border-orange-500/30"
    case "China":
      return "bg-red-500/15 text-red-400 border-red-500/30"
    case "Japan":
      return "bg-pink-500/15 text-pink-400 border-pink-500/30"
    case "Russia":
      return "bg-sky-500/15 text-sky-400 border-sky-500/30"
    default:
      return "bg-secondary text-muted-foreground"
  }
}

function formatDate(dateStr: string) {
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  } catch {
    return dateStr
  }
}

export function HistoryContent() {
  const [history, setHistory] = useState<HistoryItem[]>(() => getHistory())
  const [searchQuery, setSearchQuery] = useState("")
  const [filterConstitution, setFilterConstitution] = useState<string | null>(null)

  const filteredHistory = useMemo(() => {
    return history.filter((item) => {
      const matchesSearch =
        !searchQuery ||
        item.filename.toLowerCase().includes(searchQuery.toLowerCase())
      const matchesFilter =
        !filterConstitution || item.constitution === filterConstitution
      return matchesSearch && matchesFilter
    })
  }, [history, searchQuery, filterConstitution])

  const constitutionCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    history.forEach((item) => {
      if (item.constitution) {
        counts[item.constitution] = (counts[item.constitution] || 0) + 1
      }
    })
    return counts
  }, [history])

  function handleClearHistory() {
    clearHistory()
    setHistory([])
  }

  // Empty state
  if (history.length === 0) {
    return (
      <div className="flex flex-col gap-8 p-8">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Document History</h1>
          <p className="mt-1 text-muted-foreground">
            View and manage your previously analyzed documents.
          </p>
        </div>

        <div className="flex flex-col items-center justify-center gap-6 py-20">
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-secondary">
            <ClipboardList className="h-10 w-10 text-muted-foreground" />
          </div>
          <div className="text-center">
            <h2 className="text-xl font-semibold text-foreground">No Analysis History</h2>
            <p className="mt-2 text-sm text-muted-foreground max-w-md">
              Your analyzed documents will appear here. Upload a legal document to get started.
            </p>
          </div>
          <Button asChild>
            <Link href="/upload" className="gap-2">
              <Upload className="h-4 w-4" />
              Upload Document
            </Link>
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-8 p-8">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Document History</h1>
          <p className="mt-1 text-muted-foreground">
            {history.length} document{history.length !== 1 ? "s" : ""} analyzed
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-2 text-destructive hover:text-destructive"
            onClick={handleClearHistory}
          >
            <Trash2 className="h-4 w-4" />
            Clear History
          </Button>
          <Button size="sm" asChild>
            <Link href="/upload" className="gap-2">
              <Upload className="h-4 w-4" />
              New Upload
            </Link>
          </Button>
        </div>
      </div>

      {/* Summary stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="flex items-center gap-3 p-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <FileText className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-xl font-bold text-foreground">{history.length}</p>
              <p className="text-xs text-muted-foreground">Total Documents</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-3 p-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-chart-2/10">
              <Scale className="h-5 w-5 text-chart-2" />
            </div>
            <div>
              <p className="text-xl font-bold text-foreground">
                {Object.keys(constitutionCounts).length}
              </p>
              <p className="text-xs text-muted-foreground">Constitutions</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-3 p-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-chart-3/10">
              <ClipboardList className="h-5 w-5 text-chart-3" />
            </div>
            <div>
              <p className="text-xl font-bold text-foreground">
                {history.reduce((sum, h) => sum + h.total_clauses, 0)}
              </p>
              <p className="text-xs text-muted-foreground">Total Clauses</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-3 p-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-chart-4/10">
              <Calendar className="h-5 w-5 text-chart-4" />
            </div>
            <div>
              <p className="text-xl font-bold text-foreground">
                {history.length > 0
                  ? formatDate(history[0].created_at).split(",")[0]
                  : "--"}
              </p>
              <p className="text-xs text-muted-foreground">Latest Analysis</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search documents..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <button
            className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
              !filterConstitution
                ? "bg-primary text-primary-foreground"
                : "bg-secondary text-muted-foreground hover:text-foreground"
            }`}
            onClick={() => setFilterConstitution(null)}
          >
            All
          </button>
          {Object.entries(constitutionCounts).map(([constitution, count]) => (
            <button
              key={constitution}
              className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                filterConstitution === constitution
                  ? "bg-primary text-primary-foreground"
                  : "bg-secondary text-muted-foreground hover:text-foreground"
              }`}
              onClick={() =>
                setFilterConstitution(
                  filterConstitution === constitution ? null : constitution
                )
              }
            >
              {constitution} ({count})
            </button>
          ))}
        </div>
      </div>

      <Separator />

      {/* History List */}
      {filteredHistory.length === 0 ? (
        <div className="py-12 text-center">
          <Search className="mx-auto h-8 w-8 text-muted-foreground" />
          <p className="mt-3 text-sm text-muted-foreground">
            No documents match your search criteria.
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {filteredHistory.map((item) => (
            <Card
              key={item.id}
              className="group transition-colors hover:border-primary/30"
            >
              <CardContent className="flex items-center gap-4 p-4">
                {/* Document icon */}
                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-secondary">
                  <FileText className="h-5 w-5 text-muted-foreground" />
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-medium text-foreground truncate">
                      {item.filename}
                    </p>
                    {item.constitution && (
                      <Badge
                        className={`shrink-0 text-[10px] ${getConstitutionBadgeClass(item.constitution)}`}
                      >
                        {item.constitution}
                      </Badge>
                    )}
                  </div>
                  <div className="mt-1 flex items-center gap-3 text-xs text-muted-foreground">
                    <span>{item.total_clauses} clauses</span>
                    <span>{item.total_characters.toLocaleString()} characters</span>
                    <span>{formatDate(item.created_at)}</span>
                  </div>
                </div>

                {/* Action */}
                <ChevronRight className="h-4 w-4 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
