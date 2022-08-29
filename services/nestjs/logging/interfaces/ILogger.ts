export interface ILogger {
    message: string
    timestamp: Date
    level: "error" | "warn" | "info" | "debug" | "http"
    data?: Record<string, any> 
    status?: number
}