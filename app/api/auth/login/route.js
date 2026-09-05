import {NextResponse} from 'next/server';
import {findUser} from '@/lib/userStore';
import {checkPassword,createSession,SESSION_COOKIE,sessionCookie} from '@/lib/auth';

export async function POST(request){try{const {email='',password=''}=await request.json();const user=await findUser(String(email).trim().toLowerCase());if(!user||!await checkPassword(String(password),user.passwordHash,user.passwordSalt))return NextResponse.json({error:'Email or password is incorrect.'},{status:401});user.lastLoginAt=new Date();if(user.save)await user.save();const response=NextResponse.json({user:{name:user.name,email:user.email}});response.cookies.set(SESSION_COOKIE,createSession(user),sessionCookie);return response}catch(error){console.error('Login error:',error.message);return NextResponse.json({error:'Sign in is temporarily unavailable.'},{status:500})}}
