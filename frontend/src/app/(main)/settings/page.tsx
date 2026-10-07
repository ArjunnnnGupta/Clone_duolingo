import { DevToolsPanel } from "@/components/settings/DevToolsPanel";
import { DisplayNameForm } from "@/components/settings/DisplayNameForm";
import { GoalPicker } from "@/components/settings/GoalPicker";
import { SettingsSection } from "@/components/settings/SettingsSection";
import { ThemeToggle } from "@/components/settings/ThemeToggle";

export default function SettingsPage() {
  return (
    <div className="pb-10 pt-6">
      <h1 className="text-3xl font-extrabold">Settings</h1>
      <SettingsSection title="Profile">
        <DisplayNameForm />
      </SettingsSection>
      <SettingsSection title="Appearance">
        <ThemeToggle />
      </SettingsSection>
      <SettingsSection title="Daily goal">
        <GoalPicker />
      </SettingsSection>
      <SettingsSection title="Developer tools">
        <DevToolsPanel />
      </SettingsSection>
    </div>
  );
}
