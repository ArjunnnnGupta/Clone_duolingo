export interface HealthResponse {
  status: "ok";
}

export interface ApiErrorBody {
  error: {
    code: string;
    message: string;
  };
}
