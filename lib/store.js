import { seedTransactions } from './demoData';
import dbConnect from './mongodb'; import Transaction from '@/models/Transaction';
const memory=global.payguardStore||(global.payguardStore=seedTransactions.map(x=>({...x})));
export async function allTransactions(){try{if(process.env.MONGODB_URI){await dbConnect();return (await Transaction.find({userId:'demo-user'}).sort({createdAt:-1}).lean()).map(normalize)}}catch(e){console.warn('MongoDB fallback:',e.message)}return [...memory].sort((a,b)=>new Date(b.createdAt)-new Date(a.createdAt));}
export async function saveTransaction(data){const item={...data,userId:'demo-user',id:data.id||crypto.randomUUID(),createdAt:data.createdAt||new Date().toISOString()};try{if(process.env.MONGODB_URI){await dbConnect();return normalize((await Transaction.create(item)).toObject())}}catch(e){console.warn('MongoDB fallback:',e.message)}memory.push(item);return item;}
function normalize(x){return {...x,id:String(x._id||x.id),_id:undefined}}
