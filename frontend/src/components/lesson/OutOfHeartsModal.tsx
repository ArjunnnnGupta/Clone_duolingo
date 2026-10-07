"use client";

import { Mascot } from "@/components/mascot/Mascot";
import { Button } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";
import { Modal } from "@/components/ui/Modal";
import { useMe, useRefillHearts } from "@/lib/queries";

interface OutOfHeartsModalProps {
  isOpen: boolean;
  // Called with the hearts the server reports after a successful refill.
  onRefilled: (hearts: number) => void;
  onDecline: () => void;
  // In a lesson, a stray backdrop click or Escape must not count as "No thanks" and leave it.
  isDismissible: boolean;
}

// The price and any "not enough gems" message come from the server; the client never
// decides whether a refill is possible, it only asks.
export function OutOfHeartsModal({
  isOpen,
  onRefilled,
  onDecline,
  isDismissible,
}: OutOfHeartsModalProps) {
  const { data: me } = useMe();
  const refill = useRefillHearts();

  return (
    <Modal isOpen={isOpen} onClose={onDecline} isDismissible={isDismissible}>
      <div className="flex flex-col items-center gap-4 text-center">
        <Mascot className="h-28 w-28" />
        <h2 className="text-2xl font-extrabold">You ran out of hearts!</h2>
        <div className="flex w-full flex-col gap-2">
          <Button
            variant="secondary"
            disabled={refill.isPending || !me}
            onClick={() =>
              refill.mutate(undefined, { onSuccess: (updated) => onRefilled(updated.stats.hearts) })
            }
          >
            <span className="flex items-center justify-center gap-2">
              Refill
              {me && (
                <>
                  <Icon name="gem" className="h-5 w-5" />
                  {me.stats.refill_cost_gems}
                </>
              )}
            </span>
          </Button>
          <Button variant="ghost" onClick={onDecline}>
            No thanks
          </Button>
        </div>
        {refill.error && <p className="text-sm text-red">{refill.error.message}</p>}
      </div>
    </Modal>
  );
}
