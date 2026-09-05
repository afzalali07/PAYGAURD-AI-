import mongoose from 'mongoose';

const UserSchema=new mongoose.Schema({
  name:{type:String,required:true,trim:true,maxLength:80},
  email:{type:String,required:true,unique:true,lowercase:true,trim:true,index:true},
  passwordHash:{type:String,required:true},
  passwordSalt:{type:String,required:true},
  lastLoginAt:Date
},{timestamps:true});

export default mongoose.models.User||mongoose.model('User',UserSchema);
