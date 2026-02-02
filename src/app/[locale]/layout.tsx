import LocaleProvider from './LocaleProvider';

export default function LocaleLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <LocaleProvider>{children}</LocaleProvider>;
}
