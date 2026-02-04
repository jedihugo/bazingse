'use client';

import Image from 'next/image';
import ThemeToggle from './ThemeToggle';

export default function Header() {
  return (
    <header className="tui-bg-panel border-b tui-border-color">
      <div className="max-w-7xl mx-auto px-1 py-1 sm:px-2 sm:py-2 md:px-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Image
            src="/bazingse-logo.png"
            alt="BaZingSe Logo"
            width={48}
            height={48}
            className="w-12 h-12 object-contain"
          />
          <div>
            <h1 className="text-xl font-bold tui-text">
              BaZingSe
            </h1>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
