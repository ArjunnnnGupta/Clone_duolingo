import { DevToolsPanel } from "@/components/settings/DevToolsPanel";
import { GoalPicker } from "@/components/settings/GoalPicker";
import { SettingsSection } from "@/components/settings/SettingsSection";

export default function SettingsPage() {
  return (
    <div className="pb-10 pt-6">
      <h1 className="text-3xl font-extrabold">Settings</h1>
      <SettingsSection title="Daily goal">
        <GoalPicker />
      </SettingsSection>
      <SettingsSection title="Developer tools">
        <DevToolsPanel />
      </SettingsSection>
    </div>
  );
}
