import crypto from 'crypto';
import {promisify} from 'util';

const scrypt=promisify(crypto.scrypt);
export const SESSION_COOKIE='payguard_session';
const secret=()=>process.env.AUTH_SECRET||process.env.PAYGUARD_SIGNING_SECRET||'payguard-local-development-secret-change-me';
const encode=value=>Buffer.from(value).toString('base64url');
const sign=value=>crypto.createHmac('sha256',secret()).update(value).digest('base64url');

export async function hashPassword(password,salt=crypto.randomBytes(16).toString('hex')){
  const hash=await scrypt(password,salt,64);
  return {passwordHash:Buffer.from(hash).toString('hex'),passwordSalt:salt};
}
export async function checkPassword(password,passwordHash,salt){
  const candidate=(await hashPassword(password,salt)).passwordHash;
  return candidate.length===passwordHash.length&&crypto.timingSafeEqual(Buffer.from(candidate),Buffer.from(passwordHash));
}
export function createSession(user){
  const payload=encode(JSON.stringify({sub:String(user._id||user.id),email:user.email,name:user.name,exp:Date.now()+7*86400000}));
  return `${payload}.${sign(payload)}`;
}
export function readSession(token){try{const [payload,signature]=token.split('.');const expected=sign(payload);if(!signature||signature.length!==expected.length||!crypto.timingSafeEqual(Buffer.from(signature),Buffer.from(expected)))return null;const data=JSON.parse(Buffer.from(payload,'base64url').toString());return data.exp>Date.now()?data:null}catch{return null}}
export const sessionCookie={httpOnly:true,sameSite:'lax',secure:process.env.NODE_ENV==='production',path:'/',maxAge:7*86400};
