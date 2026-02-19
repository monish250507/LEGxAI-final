"use client"

import { useState, useRef, useCallback } from "react"
import { useRouter } from "next/navigation"
import {
  Upload,
  Camera,
  X,
  FileImage,
  ArrowRight,
  AlertCircle,
  CheckCircle2,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { cn } from "@/lib/utils"
import { uploadDocument } from "@/lib/api"
import { saveAnalysis } from "@/lib/analysis-store"
import type { Constitution, AnalysisResult } from "@/lib/types"

const constitutions: { value: Constitution; label: string; flag: string; description: string }[] = [
  { value: "India", label: "India", flag: "IN", description: "Constitution of India" },
  { value: "China", label: "China", flag: "CN", description: "Constitution of PRC (2018)" },
  { value: "Japan", label: "Japan", flag: "JP", description: "Constitution of Japan (1946)" },
  { value: "Russia", label: "Russia", flag: "RU", description: "Constitution of Russia (2014)" },
]

type UploadStep = "upload" | "constitution" | "processing" | "complete" | "error"

export function UploadContent() {
  const router = useRouter()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  const [step, setStep] = useState<UploadStep>("upload")
  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [selectedConstitution, setSelectedConstitution] = useState<Constitution | null>(null)
  const [dragActive, setDragActive] = useState(false)
  const [progress, setProgress] = useState(0)
  const [errorMessage, setErrorMessage] = useState("")
  const [showCamera, setShowCamera] = useState(false)

  const handleFile = useCallback((f: File) => {
    const validTypes = ["image/jpeg", "image/png", "image/jpg", "application/pdf", "application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation"]
    if (!validTypes.includes(f.type)) {
      setErrorMessage("Please upload a JPG, PNG, PDF, or PPT file.")
      setStep("error")
      return
    }
    setFile(f)
    
    // Set preview based on file type
    if (f.type.startsWith('image/')) {
      setPreviewUrl(URL.createObjectURL(f))
    } else if (f.type === 'application/pdf') {
      setPreviewUrl('/icons/file-pdf.svg')
    } else if (f.type.includes('powerpoint') || f.type.includes('presentationml')) {
      setPreviewUrl('/icons/file-ppt.svg')
    } else {
      setPreviewUrl('/icons/file-document.svg')
    }
    
    setStep("constitution")
    setErrorMessage("")
  }, [])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setDragActive(false)
      if (e.dataTransfer.files?.[0]) {
        handleFile(e.dataTransfer.files[0])
      }
    },
    [handleFile]
  )

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragActive(true)
  }, [])

  const handleDragLeave = useCallback(() => {
    setDragActive(false)
  }, [])

  const openCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
      setShowCamera(true)
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          videoRef.current.play()
        }
      }, 100)
    } catch {
      setErrorMessage("Camera access denied or not available.")
      setStep("error")
    }
  }, [])

  const capturePhoto = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return
    const video = videoRef.current
    const canvas = canvasRef.current
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext("2d")
    if (!ctx) return
    ctx.drawImage(video, 0, 0)
    canvas.toBlob(
      (blob) => {
        if (blob) {
          const capturedFile = new File([blob], "camera-capture.jpg", { type: "image/jpeg" })
          handleFile(capturedFile)
        }
        // Stop camera
        const stream = video.srcObject as MediaStream
        stream?.getTracks().forEach((t) => t.stop())
        setShowCamera(false)
      },
      "image/jpeg",
      0.9
    )
  }, [handleFile])

  const closeCamera = useCallback(() => {
    if (videoRef.current) {
      const stream = videoRef.current.srcObject as MediaStream
      stream?.getTracks().forEach((t) => t.stop())
    }
    setShowCamera(false)
  }, [])

  const handleAnalyze = useCallback(async () => {
    if (!file || !selectedConstitution) return
    setStep("processing")
    setProgress(0)

    // Simulate progress for UX
    const interval = setInterval(() => {
      setProgress((p) => {
        if (p >= 90) {
          clearInterval(interval)
          return 90
        }
        return p + Math.random() * 15
      })
    }, 500)

    try {
      const response = await uploadDocument(file, selectedConstitution)
      clearInterval(interval)

      if (!response.ok) {
        const errData = await response.json().catch(() => ({ detail: "Upload failed" }))
        throw new Error(errData.detail || "Upload failed")
      }

      const result: AnalysisResult = await response.json()
      setProgress(100)
      saveAnalysis(result, selectedConstitution, previewUrl || undefined)
      setStep("complete")

      setTimeout(() => {
        router.push("/analysis")
      }, 1500)
    } catch (err) {
      clearInterval(interval)
      setErrorMessage(err instanceof Error ? err.message : "Analysis failed. Make sure the backend is running.")
      setStep("error")
    }
  }, [file, selectedConstitution, previewUrl, router])

  const reset = useCallback(() => {
    setFile(null)
    setPreviewUrl(null)
    setSelectedConstitution(null)
    setStep("upload")
    setProgress(0)
    setErrorMessage("")
  }, [])

  return (
    <div className="flex flex-col gap-8 p-8">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Upload Document</h1>
        <p className="mt-1 text-muted-foreground">
          Upload a legal document image and select a governing constitution for analysis.
        </p>
      </div>

      {/* Step Indicator */}
      <div className="flex items-center gap-2">
        {["Upload", "Constitution", "Analysis"].map((label, i) => {
          const stepIndex =
            step === "upload" ? 0 : step === "constitution" ? 1 : 2
          const isActive = i <= stepIndex
          return (
            <div key={label} className="flex items-center gap-2">
              {i > 0 && (
                <div
                  className={cn(
                    "h-px w-8",
                    isActive ? "bg-primary" : "bg-border"
                  )}
                />
              )}
              <div className="flex items-center gap-2">
                <div
                  className={cn(
                    "flex h-7 w-7 items-center justify-center rounded-full text-xs font-medium",
                    isActive
                      ? "bg-primary text-primary-foreground"
                      : "bg-secondary text-muted-foreground"
                  )}
                >
                  {i + 1}
                </div>
                <span
                  className={cn(
                    "text-sm font-medium",
                    isActive ? "text-foreground" : "text-muted-foreground"
                  )}
                >
                  {label}
                </span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Camera overlay */}
      {showCamera && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/90">
          <div className="relative w-full max-w-2xl">
            <video ref={videoRef} className="w-full rounded-lg" autoPlay playsInline />
            <canvas ref={canvasRef} className="hidden" />
            <div className="absolute bottom-4 left-1/2 flex -translate-x-1/2 gap-4">
              <Button onClick={capturePhoto} size="lg">
                <Camera className="mr-2 h-5 w-5" />
                Capture
              </Button>
              <Button onClick={closeCamera} variant="outline" size="lg">
                Cancel
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Step: Upload */}
      {step === "upload" && (
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Drag & Drop */}
          <Card
            className={cn(
              "cursor-pointer transition-colors",
              dragActive ? "border-primary bg-primary/5" : "hover:border-primary/40"
            )}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => fileInputRef.current?.click()}
          >
            <CardContent className="flex flex-col items-center justify-center gap-4 p-12">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                <Upload className="h-8 w-8 text-primary" />
              </div>
              <div className="text-center">
                <p className="text-lg font-medium text-foreground">
                  Drop your document here
                </p>
                <p className="mt-1 text-sm text-muted-foreground">
                  or click to browse files
                </p>
              </div>
              <Badge variant="secondary">JPG, PNG, JPEG</Badge>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/jpg"
                className="hidden"
                onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
              />
            </CardContent>
          </Card>

          {/* Camera Capture */}
          <Card
            className="cursor-pointer transition-colors hover:border-primary/40"
            onClick={openCamera}
          >
            <CardContent className="flex flex-col items-center justify-center gap-4 p-12">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-chart-2/10">
                <Camera className="h-8 w-8 text-chart-2" />
              </div>
              <div className="text-center">
                <p className="text-lg font-medium text-foreground">
                  Capture with Camera
                </p>
                <p className="mt-1 text-sm text-muted-foreground">
                  Take a photo of your document
                </p>
              </div>
              <Badge variant="secondary">Live Camera</Badge>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Step: Constitution Selection */}
      {step === "constitution" && (
        <div className="flex flex-col gap-6">
          {/* Document Preview */}
          {previewUrl && (
            <Card>
              <CardHeader className="flex-row items-center justify-between">
                <div className="flex items-center gap-3">
                  <FileImage className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <CardTitle className="text-base">{file?.name}</CardTitle>
                    <CardDescription>
                      {file && (file.size / 1024).toFixed(1)} KB
                    </CardDescription>
                  </div>
                </div>
                <Button variant="ghost" size="icon" onClick={reset}>
                  <X className="h-4 w-4" />
                  <span className="sr-only">Remove file</span>
                </Button>
              </CardHeader>
              <CardContent>
                <div className="relative aspect-video w-full max-w-md overflow-hidden rounded-lg border border-border bg-secondary">
                  {previewUrl?.startsWith('data:') ? (
                    // Image preview
                    <img
                      src={previewUrl}
                      alt="Document preview"
                      className="h-full w-full object-contain"
                    />
                  ) : previewUrl?.includes('file-') ? (
                    // File icon preview
                    <div className="flex items-center justify-center h-full">
                      <img
                        src={previewUrl}
                        alt="Document icon"
                        className="h-16 w-16"
                      />
                      <span className="ml-2 text-muted-foreground">{file?.name}</span>
                    </div>
                  ) : null}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Constitution Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Select Governing Constitution</CardTitle>
              <CardDescription>
                Choose the constitution that governs the legal context of this document.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {constitutions.map((c) => (
                  <button
                    key={c.value}
                    onClick={() => setSelectedConstitution(c.value)}
                    className={cn(
                      "flex flex-col items-center gap-2 rounded-lg border p-4 text-center transition-all",
                      selectedConstitution === c.value
                        ? "border-primary bg-primary/10 ring-1 ring-primary"
                        : "border-border hover:border-primary/40 hover:bg-accent"
                    )}
                  >
                    <span className="text-2xl font-bold text-foreground">{c.flag}</span>
                    <span className="text-sm font-medium text-foreground">{c.label}</span>
                    <span className="text-xs text-muted-foreground">{c.description}</span>
                  </button>
                ))}
              </div>

              <div className="mt-6 flex gap-3">
                <Button variant="outline" onClick={reset}>
                  Back
                </Button>
                <Button
                  onClick={handleAnalyze}
                  disabled={!selectedConstitution}
                  className="gap-2"
                >
                  Start Analysis
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Step: Processing */}
      {step === "processing" && (
        <Card>
          <CardContent className="flex flex-col items-center gap-6 p-12">
            <div className="h-12 w-12 animate-spin rounded-full border-[3px] border-primary border-t-transparent" />
            <div className="text-center">
              <p className="text-lg font-medium text-foreground">Analyzing Document</p>
              <p className="mt-1 text-sm text-muted-foreground">
                Running AI-powered legal analysis pipeline...
              </p>
            </div>
            <div className="w-full max-w-md">
              <Progress value={progress} className="h-2" />
              <p className="mt-2 text-center text-xs text-muted-foreground">
                {progress < 30
                  ? "Extracting text with OCR..."
                  : progress < 60
                    ? "Classifying clauses..."
                    : progress < 90
                      ? "Generating legal analysis..."
                      : "Finalizing results..."}
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Step: Complete */}
      {step === "complete" && (
        <Card>
          <CardContent className="flex flex-col items-center gap-6 p-12">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-chart-2/10">
              <CheckCircle2 className="h-8 w-8 text-chart-2" />
            </div>
            <div className="text-center">
              <p className="text-lg font-medium text-foreground">Analysis Complete</p>
              <p className="mt-1 text-sm text-muted-foreground">
                Redirecting to results...
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Step: Error */}
      {step === "error" && (
        <Card className="border-destructive/50">
          <CardContent className="flex flex-col items-center gap-6 p-12">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-destructive/10">
              <AlertCircle className="h-8 w-8 text-destructive" />
            </div>
            <div className="text-center">
              <p className="text-lg font-medium text-foreground">Analysis Failed</p>
              <p className="mt-1 text-sm text-muted-foreground">{errorMessage}</p>
            </div>
            <Button onClick={reset}>Try Again</Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
