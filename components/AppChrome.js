'use client';
import {usePathname} from 'next/navigation';
import Sidebar from './Sidebar';
export default function AppChrome({children}){const auth=usePathname()==='/login';if(auth)return <main className="auth-main">{children}</main>;return <div className="app-shell"><Sidebar/><main className="main"><header className="topbar"><div><span className="eyebrow">INTELLIGENT PAYMENT SAFETY</span></div><div className="top-actions"><span className="live-dot"/>Protection active <span className="demo">DEMO MODE</span></div></header>{children}</main></div>}
