import {NextResponse} from 'next/server';import {cookies} from 'next/headers';import {readSession,SESSION_COOKIE} from '@/lib/auth';
export async function GET(){const user=readSession(cookies().get(SESSION_COOKIE)?.value);return user?NextResponse.json({user:{id:user.sub,name:user.name,email:user.email}}):NextResponse.json({error:'Unauthorized'},{status:401})}
