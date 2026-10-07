"use client";

import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { Toast } from "./Toast";

const TOAST_DURATION_MS = 2500;

type ShowToast = (message: string) => void;

const ToastContext = createContext<ShowToast>(() => {});

export function useToast(): ShowToast {
  return useContext(ToastContext);
}

export function ToastProvider({ children }: { children: ReactNode }) {
  // A fresh object per call, so showing the same message again still restarts the timer.
  const [toast, setToast] = useState<{ message: string } | null>(null);
  const showToast = useCallback((message: string) => setToast({ message }), []);

  useEffect(() => {
    if (toast === null) {
      return;
    }
    const timer = setTimeout(() => setToast(null), TOAST_DURATION_MS);
    return () => clearTimeout(timer);
  }, [toast]);

  return (
    <ToastContext.Provider value={showToast}>
      {children}
      <Toast message={toast?.message ?? null} />
    </ToastContext.Provider>
  );
}
