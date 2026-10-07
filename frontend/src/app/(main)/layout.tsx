import { MobileTabBar } from "@/components/layout/MobileTabBar";
import { MobileTopBar } from "@/components/layout/MobileTopBar";
import { RightRail } from "@/components/layout/RightRail";
import { Sidebar } from "@/components/layout/Sidebar";

export default function MainLayout({ children }: LayoutProps<"/">) {
  return (
    <div className="min-h-screen md:pl-[88px] lg:pl-64">
      <Sidebar />
      <div className="flex justify-center gap-6">
        <main className="w-full max-w-[600px] px-4 pb-24 md:pb-10">
          <MobileTopBar />
          {children}
        </main>
        <RightRail />
      </div>
      <MobileTabBar />
    </div>
  );
}
