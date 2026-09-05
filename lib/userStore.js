import dbConnect from './mongodb';
import User from '@/models/User';

const users=global.payguardUsers||(global.payguardUsers=[]);
export async function findUser(email){const normalized=email.toLowerCase();if(process.env.MONGODB_URI){await dbConnect();return User.findOne({email:normalized})}return users.find(user=>user.email===normalized)||null}
export async function createUser(data){if(process.env.MONGODB_URI){await dbConnect();return User.create(data)}const user={...data,id:crypto.randomUUID(),createdAt:new Date()};users.push(user);return user}
