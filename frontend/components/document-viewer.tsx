"use client"

import { useRef, useEffect, useState, useCallback } from "react"
import { ZoomIn, ZoomOut, RotateCcw } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { Clause } from "@/lib/types"

interface DocumentViewerProps {
  imageUrl: string
  clauses: Clause[]
  selectedClause: string | null
  onClauseClick: (id: string) => void
}

interface HighlightBox {
  clause_id: string
  x: number
  y: number
  width: number
  height: number
  color: string
}

function generateHighlightPositions(clauses: Clause[], imgWidth: number, imgHeight: number): HighlightBox[] {
  const boxes: HighlightBox[] = []
  const margin = 20
  const lineHeight = Math.max(30, imgHeight / (clauses.length + 2))
  const sortedClauses = [...clauses].sort((a, b) => a.rank - b.rank)

  sortedClauses.forEach((clause, index) => {
    const y = margin + index * lineHeight
    if (y + lineHeight > imgHeight - margin) return

    const colorMap: Record<string, string> = {
      red: "rgba(239, 68, 68, 0.25)",
      yellow: "rgba(234, 179, 8, 0.25)",
      green: "rgba(34, 197, 94, 0.25)",
    }

    boxes.push({
      clause_id: clause.clause_id,
      x: margin,
      y,
      width: imgWidth - margin * 2,
      height: lineHeight - 4,
      color: colorMap[clause.color] || colorMap.green,
    })
  })

  return boxes
}

export function DocumentViewer({ imageUrl, clauses, selectedClause, onClauseClick }: DocumentViewerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [zoom, setZoom] = useState(1)
  const [imgLoaded, setImgLoaded] = useState(false)
  const imgRef = useRef<HTMLImageElement | null>(null)
  const highlightsRef = useRef<HighlightBox[]>([])

  const drawCanvas = useCallback(() => {
    const canvas = canvasRef.current
    const img = imgRef.current
    if (!canvas || !img || !imgLoaded) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    canvas.width = img.naturalWidth
    canvas.height = img.naturalHeight

    // Draw image
    ctx.drawImage(img, 0, 0)

    // Generate and draw highlights
    const highlights = generateHighlightPositions(clauses, img.naturalWidth, img.naturalHeight)
    highlightsRef.current = highlights

    highlights.forEach((box) => {
      const isSelected = box.clause_id === selectedClause

      // Fill
      ctx.fillStyle = box.color
      ctx.fillRect(box.x, box.y, box.width, box.height)

      // Border
      if (isSelected) {
        ctx.strokeStyle = "hsl(210, 100%, 52%)"
        ctx.lineWidth = 3
        ctx.setLineDash([])
      } else {
        const borderColor = box.color.replace("0.25", "0.6")
        ctx.strokeStyle = borderColor
        ctx.lineWidth = 1
        ctx.setLineDash([4, 2])
      }
      ctx.strokeRect(box.x, box.y, box.width, box.height)
      ctx.setLineDash([])
    })
  }, [clauses, selectedClause, imgLoaded])

  useEffect(() => {
    const img = new Image()
    img.crossOrigin = "anonymous"
    img.onload = () => {
      imgRef.current = img
      setImgLoaded(true)
    }
    img.src = imageUrl
  }, [imageUrl])

  useEffect(() => {
    drawCanvas()
  }, [drawCanvas])

  const handleCanvasClick = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      const canvas = canvasRef.current
      if (!canvas) return

      const rect = canvas.getBoundingClientRect()
      const scaleX = canvas.width / rect.width
      const scaleY = canvas.height / rect.height
      const x = (e.clientX - rect.left) * scaleX
      const y = (e.clientY - rect.top) * scaleY

      const clicked = highlightsRef.current.find(
        (box) =>
          x >= box.x &&
          x <= box.x + box.width &&
          y >= box.y &&
          y <= box.y + box.height
      )

      if (clicked) {
        onClauseClick(clicked.clause_id)
      }
    },
    [onClauseClick]
  )

  return (
    <div className="flex flex-col gap-3 h-full">
      {/* Controls */}
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="icon"
          onClick={() => setZoom((z) => Math.max(0.5, z - 0.25))}
          aria-label="Zoom out"
        >
          <ZoomOut className="h-4 w-4" />
        </Button>
        <span className="text-xs text-muted-foreground min-w-10 text-center">
          {Math.round(zoom * 100)}%
        </span>
        <Button
          variant="outline"
          size="icon"
          onClick={() => setZoom((z) => Math.min(3, z + 0.25))}
          aria-label="Zoom in"
        >
          <ZoomIn className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          size="icon"
          onClick={() => setZoom(1)}
          aria-label="Reset zoom"
        >
          <RotateCcw className="h-4 w-4" />
        </Button>

        {/* Legend */}
        <div className="ml-auto flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <div className="h-3 w-3 rounded-sm bg-red-500/40" />
            <span className="text-xs text-muted-foreground">Critical</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="h-3 w-3 rounded-sm bg-yellow-500/40" />
            <span className="text-xs text-muted-foreground">Moderate</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="h-3 w-3 rounded-sm bg-green-500/40" />
            <span className="text-xs text-muted-foreground">Info</span>
          </div>
        </div>
      </div>

      {/* Canvas */}
      <div className="flex-1 overflow-auto rounded-lg border border-border bg-secondary/50">
        <div
          style={{
            transform: `scale(${zoom})`,
            transformOrigin: "top left",
            transition: "transform 0.2s ease",
          }}
        >
          <canvas
            ref={canvasRef}
            className="max-w-full cursor-pointer"
            onClick={handleCanvasClick}
          />
        </div>
      </div>
    </div>
  )
}
