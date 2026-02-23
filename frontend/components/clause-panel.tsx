"use client"

import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import {
  AlertTriangle,
  AlertCircle,
  Info,
  ChevronDown,
  ChevronUp,
} from "lucide-react"
import { useState } from "react"
import type { Clause } from "@/lib/types"

interface ClausePanelProps {
  clauses: Clause[]
  selectedClause: string | null
  onClauseSelect: (id: string) => void
  constitution: string
}

function getPriorityIcon(color: string) {
  switch (color) {
    case "red":
      return <AlertTriangle className="h-4 w-4 text-destructive" />
    case "yellow":
      return <AlertCircle className="h-4 w-4 text-chart-3" />
    default:
      return <Info className="h-4 w-4 text-chart-2" />
  }
}

function getPriorityLabel(color: string) {
  switch (color) {
    case "red":
      return "Critical Risk"
    case "yellow":
      return "Moderate"
    default:
      return "Informational"
  }
}

function getPriorityBadgeClasses(color: string) {
  switch (color) {
    case "red":
      return "bg-destructive/15 text-destructive border-destructive/30"
    case "yellow":
      return "bg-chart-3/15 text-chart-3 border-chart-3/30"
    default:
      return "bg-chart-2/15 text-chart-2 border-chart-2/30"
  }
}

export function ClausePanel({ clauses, selectedClause, onClauseSelect, constitution }: ClausePanelProps) {
  const [expandedClauses, setExpandedClauses] = useState<Set<string>>(new Set())
  const sortedClauses = [...clauses].sort((a, b) => a.rank - b.rank)

  function toggleExpand(id: string) {
    setExpandedClauses((prev) => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border px-4 py-3">
        <div>
          <h3 className="text-sm font-semibold text-foreground">Clause Analysis</h3>
          <p className="text-xs text-muted-foreground">
            {clauses.length} clauses &middot; {constitution} Constitution
          </p>
        </div>
        <div className="flex gap-1.5">
          <Badge className={cn("text-[10px]", getPriorityBadgeClasses("red"))}>
            {clauses.filter((c) => c.color === "red").length}
          </Badge>
          <Badge className={cn("text-[10px]", getPriorityBadgeClasses("yellow"))}>
            {clauses.filter((c) => c.color === "yellow").length}
          </Badge>
          <Badge className={cn("text-[10px]", getPriorityBadgeClasses("green"))}>
            {clauses.filter((c) => c.color === "green").length}
          </Badge>
        </div>
      </div>

      {/* Clause List */}
      <ScrollArea className="flex-1">
        <div className="flex flex-col gap-1 p-2">
          {sortedClauses.map((clause) => {
            const isSelected = clause.clause_id === selectedClause
            const isExpanded = expandedClauses.has(clause.clause_id)

            return (
              <div
                key={clause.clause_id}
                className={cn(
                  "rounded-lg border transition-all cursor-pointer",
                  isSelected
                    ? "border-primary bg-primary/5"
                    : "border-transparent hover:border-border hover:bg-accent/50"
                )}
              >
                {/* Clause header */}
                <button
                  className="flex w-full items-start gap-3 p-3 text-left"
                  onClick={() => {
                    onClauseSelect(clause.clause_id)
                    toggleExpand(clause.clause_id)
                  }}
                >
                  <div className="mt-0.5">{getPriorityIcon(clause.color)}</div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-xs font-mono text-muted-foreground">
                        #{clause.rank}
                      </span>
                      <Badge variant="secondary" className="text-[10px] capitalize">
                        {clause.type}
                      </Badge>
                      <Badge className={cn("text-[10px]", getPriorityBadgeClasses(clause.color))}>
                        {getPriorityLabel(clause.color)}
                      </Badge>
                    </div>
                    <p className="mt-1.5 text-sm text-foreground leading-relaxed line-clamp-2">
                      {clause.text}
                    </p>
                    <div className="mt-1.5 flex items-center gap-3 text-xs text-muted-foreground">
                      <span>Score: {(clause.priority_score * 100).toFixed(0)}%</span>
                      <span>Confidence: {(clause.confidence * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                  <div className="mt-0.5">
                    {isExpanded ? (
                      <ChevronUp className="h-4 w-4 text-muted-foreground" />
                    ) : (
                      <ChevronDown className="h-4 w-4 text-muted-foreground" />
                    )}
                  </div>
                </button>

                {/* Expanded content - AI explanation */}
                {isExpanded && (
                  <div className="px-3 pb-3">
                    <Separator className="mb-3" />
                    <div className="rounded-md bg-secondary/80 p-3">
                      <p className="text-xs font-medium text-foreground mb-1">
                        AI Legal Analysis
                      </p>
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        {clause.explanation ||
                          `This ${clause.type} clause has been identified with a priority score of ${(clause.priority_score * 100).toFixed(0)}%. Under the ${constitution} Constitution, this clause type carries ${clause.color === "red" ? "significant legal weight and requires careful attention" : clause.color === "yellow" ? "moderate legal importance and should be reviewed" : "standard legal standing as an informational provision"}. The clause pertains to ${clause.type} provisions and has been ranked #${clause.rank} in order of legal significance.`}
                      </p>
                      <div className="mt-2 flex items-center gap-2">
                        <Badge variant="outline" className="text-[10px]">
                          {constitution} Constitution
                        </Badge>
                        <Badge variant="outline" className="text-[10px]">
                          {clause.color === "red" ? "High Risk" : clause.color === "yellow" ? "Review Required" : "Standard"}
                        </Badge>
                      </div>
                    </div>

                    {/* Full clause text */}
                    <div className="mt-2 rounded-md border border-border p-3">
                      <p className="text-xs font-medium text-foreground mb-1">
                        Full Clause Text
                      </p>
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        {clause.text}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </ScrollArea>
    </div>
  )
}
