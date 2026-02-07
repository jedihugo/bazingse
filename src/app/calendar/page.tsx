'use client';

import Header from '@/components/Header';
import DongGongCalendar from '@/components/DongGongCalendar';

export default function CalendarPage() {
  return (
    <div className="min-h-screen tui-bg">
      <Header />
      <main className="mx-auto main-content px-4 py-4">
        <div className="mx-auto" style={{ maxWidth: '800px' }}>
          <DongGongCalendar />
        </div>
      </main>
    </div>
  );
}
