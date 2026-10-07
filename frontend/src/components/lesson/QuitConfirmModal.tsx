import { Mascot } from "@/components/mascot/Mascot";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";

interface QuitConfirmModalProps {
  isOpen: boolean;
  isQuitting: boolean;
  errorMessage: string | null;
  onKeepLearning: () => void;
  onEndSession: () => void;
}

export function QuitConfirmModal({
  isOpen,
  isQuitting,
  errorMessage,
  onKeepLearning,
  onEndSession,
}: QuitConfirmModalProps) {
  return (
    <Modal isOpen={isOpen} onClose={onKeepLearning}>
      <div className="flex flex-col items-center gap-4 text-center">
        <Mascot className="h-28 w-28" />
        <h2 className="text-2xl font-extrabold">
          Wait, don&apos;t go! You&apos;ll lose your progress if you quit now
        </h2>
        <div className="flex w-full flex-col gap-2">
          <Button variant="secondary" onClick={onKeepLearning}>
            Keep learning
          </Button>
          <Button variant="ghost" disabled={isQuitting} onClick={onEndSession}>
            End session
          </Button>
        </div>
        {errorMessage && <p className="text-sm text-red">{errorMessage}</p>}
      </div>
    </Modal>
  );
}
