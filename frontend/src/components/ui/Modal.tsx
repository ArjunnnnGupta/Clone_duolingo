"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useEffect, type ReactNode } from "react";
import { createPortal } from "react-dom";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  // False when closing means a real decision (leaving a lesson): only the modal's own buttons act.
  isDismissible?: boolean;
  children: ReactNode;
}

export function Modal({ isOpen, onClose, isDismissible = true, children }: ModalProps) {
  useEffect(() => {
    if (!isOpen || !isDismissible) {
      return;
    }
    function closeOnEscape(event: KeyboardEvent) {
      if (event.key === "Escape") {
        onClose();
      }
    }
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [isOpen, isDismissible, onClose]);

  // Server render has no document; the modal only ever shows after a click anyway.
  if (typeof document === "undefined") {
    return null;
  }

  // Portalled to <body> so a transformed ancestor (e.g. the animated node popover) cannot
  // turn this fixed overlay into one that is positioned relative to itself.
  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center bg-scrim/60 px-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={isDismissible ? onClose : undefined}
        >
          <motion.div
            role="dialog"
            aria-modal="true"
            className="w-full max-w-[420px] rounded-2xl bg-surface p-6"
            initial={{ scale: 0.9, y: 16 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.9, y: 16 }}
            onClick={(event) => event.stopPropagation()}
          >
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body,
  );
}
