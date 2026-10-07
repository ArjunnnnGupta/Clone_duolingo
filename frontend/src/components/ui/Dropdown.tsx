"use client";

import { useEffect, type ReactNode } from "react";

interface DropdownProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
}

// A panel that hangs from the nearest `relative` ancestor (the stats bar). A transparent layer
// behind it catches outside clicks; the trigger buttons sit above that layer (z-50) so they stay
// clickable.
export function Dropdown({ isOpen, onClose, children }: DropdownProps) {
  useEffect(() => {
    if (!isOpen) {
      return;
    }
    function closeOnEscape(event: KeyboardEvent) {
      if (event.key === "Escape") {
        onClose();
      }
    }
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [isOpen, onClose]);

  if (!isOpen) {
    return null;
  }
  return (
    <>
      <button
        aria-hidden="true"
        tabIndex={-1}
        className="fixed inset-0 z-40 cursor-default"
        onClick={onClose}
      />
      <div className="absolute inset-x-0 top-full z-50 mt-3 rounded-2xl border-2 border-border bg-surface p-4">
        {children}
      </div>
    </>
  );
}
