"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { useToast } from "@/components/ui/ToastProvider";
import { ApiError } from "@/lib/api";
import { useMe, useUpdateSettings } from "@/lib/queries";

// Mirrors the server's limit; the server still validates (and trims) the name.
const MAX_NAME_LENGTH = 40;

export function DisplayNameForm() {
  const { data: me } = useMe();
  const updateSettings = useUpdateSettings();
  const showToast = useToast();
  const [draft, setDraft] = useState<string | null>(null);

  const savedName = me?.user.display_name ?? "";
  const name = draft ?? savedName;
  const isChanged = draft !== null && draft !== savedName;

  function save(event: FormEvent) {
    event.preventDefault();
    updateSettings.mutate(
      { display_name: name },
      {
        onSuccess: () => {
          setDraft(null);
          showToast("Settings saved");
        },
      },
    );
  }

  // The server's validation text names the request field ("body.display_name: ..."); say it plainly.
  const error = updateSettings.error;
  const errorMessage =
    error instanceof ApiError && error.code === "VALIDATION_ERROR"
      ? `Enter a name between 1 and ${MAX_NAME_LENGTH} characters.`
      : error?.message;

  return (
    <form onSubmit={save} className="flex flex-col gap-3">
      <label htmlFor="display-name" className="text-text-muted">
        Display name
      </label>
      <input
        id="display-name"
        value={name}
        disabled={!me}
        maxLength={MAX_NAME_LENGTH}
        onChange={(event) => {
          updateSettings.reset();
          setDraft(event.target.value);
        }}
        className="w-full rounded-2xl border-2 border-border bg-surface-subtle px-4 py-4 text-[17px] font-bold outline-none focus:border-blue"
      />
      {errorMessage && <p className="text-sm text-red">{errorMessage}</p>}
      <Button type="submit" disabled={!isChanged || updateSettings.isPending}>
        Save
      </Button>
    </form>
  );
}
