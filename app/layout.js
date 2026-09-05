import './globals.css';
import AppChrome from '@/components/AppChrome';
import {Suspense} from 'react';

export const metadata = { title: 'PayGuard AI', description: 'Think Before You Pay.' };

export default function RootLayout({ children }) {
  return <html lang="en"><body><Suspense fallback={<main className="auth-main"/>}><AppChrome>{children}</AppChrome></Suspense></body></html>;
}
