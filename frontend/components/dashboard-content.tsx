"use client"

import Link from "next/link"
import {
  Upload,
  FileSearch,
  History,
  FileText,
  Shield,
  Zap,
  ArrowRight,
} from "lucide-react"
import { useAuth } from "@/lib/auth-context"
import { getHistory } from "@/lib/analysis-store"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export function DashboardContent() {
  const { user } = useAuth()
  const history = getHistory()

  const stats = [
    {
      label: "Documents Analyzed",
      value: history.length.toString(),
      icon: FileText,
      color: "text-primary",
    },
    {
      label: "Constitutions Used",
      value: [...new Set(history.map((h) => h.constitution).filter(Boolean))].length.toString(),
      icon: Shield,
      color: "text-chart-2",
    },
    {
      label: "Total Clauses Found",
      value: history.reduce((sum, h) => sum + h.total_clauses, 0).toString(),
      icon: Zap,
      color: "text-chart-3",
    },
  ]

  return (
    <div className="flex flex-col gap-8 p-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">
          Welcome back, {user?.name}
        </h1>
        <p className="mt-1 text-muted-foreground">
          Upload and analyze legal documents with AI-powered constitution-aware intelligence.
        </p>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        {stats.map((stat) => (
          <Card key={stat.label}>
            <CardContent className="flex items-center gap-4 p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-secondary">
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stat.value}</p>
                <p className="text-sm text-muted-foreground">{stat.label}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card className="group cursor-pointer transition-colors hover:border-primary/40">
          <Link href="/upload">
            <CardHeader>
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 mb-2">
                <Upload className="h-5 w-5 text-primary" />
              </div>
              <CardTitle className="text-lg">Upload Document</CardTitle>
              <CardDescription>
                Upload a legal document image or capture with camera for AI analysis.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="ghost" size="sm" className="gap-2 text-primary p-0">
                Get Started <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Link>
        </Card>

        <Card className="group cursor-pointer transition-colors hover:border-primary/40">
          <Link href="/analysis">
            <CardHeader>
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-chart-2/10 mb-2">
                <FileSearch className="h-5 w-5 text-chart-2" />
              </div>
              <CardTitle className="text-lg">View Analysis</CardTitle>
              <CardDescription>
                Review AI-generated legal analysis with highlighted clauses and explanations.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="ghost" size="sm" className="gap-2 text-chart-2 p-0">
                View Results <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Link>
        </Card>

        <Card className="group cursor-pointer transition-colors hover:border-primary/40">
          <Link href="/history">
            <CardHeader>
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-chart-3/10 mb-2">
                <History className="h-5 w-5 text-chart-3" />
              </div>
              <CardTitle className="text-lg">Document History</CardTitle>
              <CardDescription>
                Access previous analyses, download annotated documents, and review history.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="ghost" size="sm" className="gap-2 text-chart-3 p-0">
                View History <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Link>
        </Card>
      </div>

      {/* Recent Activity */}
      {history.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Recent Analyses</CardTitle>
            <CardDescription>Your most recent document analyses</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-3">
              {history.slice(0, 5).map((item) => (
                <div
                  key={item.id}
                  className="flex items-center justify-between rounded-md border border-border p-3"
                >
                  <div className="flex items-center gap-3">
                    <FileText className="h-4 w-4 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium text-foreground">{item.filename}</p>
                      <p className="text-xs text-muted-foreground">
                        {item.total_clauses} clauses &middot;{" "}
                        {new Date(item.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  {item.constitution && (
                    <Badge variant="secondary" className="text-xs">
                      {item.constitution}
                    </Badge>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
