"use client";

import { AchievementList } from "@/components/profile/AchievementList";
import { ProfileHeader } from "@/components/profile/ProfileHeader";
import { ProfileSection } from "@/components/profile/ProfileSection";
import { StatsGrid } from "@/components/profile/StatsGrid";
import { WeekXpChart } from "@/components/profile/WeekXpChart";
import { Skeleton } from "@/components/ui/Skeleton";
import { useProfile } from "@/lib/queries";

export default function ProfilePage() {
  const { data: profile, isError, error } = useProfile();

  if (isError) {
    return <p className="mt-10 text-center text-text-muted">Could not load your profile: {error.message}</p>;
  }
  if (!profile) {
    return (
      <div className="flex flex-col gap-4 pt-6">
        <Skeleton className="h-28 w-full" />
        <Skeleton className="h-48 w-full" />
      </div>
    );
  }
  return (
    <div className="pb-10 pt-6">
      <ProfileHeader user={profile.user} />
      <ProfileSection title="Statistics">
        <StatsGrid profile={profile} />
      </ProfileSection>
      <ProfileSection title="Last 7 days">
        <WeekXpChart days={profile.week_xp} />
      </ProfileSection>
      <ProfileSection title="Achievements">
        <AchievementList achievements={profile.achievements} />
      </ProfileSection>
    </div>
  );
}
