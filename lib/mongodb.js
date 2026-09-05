import mongoose from 'mongoose';
let cached=global.mongooseCache||(global.mongooseCache={conn:null,promise:null});
export default async function dbConnect(){if(cached.conn)return cached.conn;if(!process.env.MONGODB_URI)throw new Error('MONGODB_URI is not configured');if(!cached.promise)cached.promise=mongoose.connect(process.env.MONGODB_URI,{bufferCommands:false,serverSelectionTimeoutMS:3500});try{cached.conn=await cached.promise;return cached.conn}catch(error){cached.promise=null;throw error}}
