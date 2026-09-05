import mongoose from 'mongoose';
const schema=new mongoose.Schema({
  userId:{type:String,required:true,index:true},beneficiary:{type:String,required:true,trim:true,index:true},beneficiaryAccountFingerprint:{type:String,index:true},amount:{type:Number,required:true,min:1},purpose:String,
  merchantCategory:{type:String,default:'other'},location:{type:String,default:'unknown'},deviceId:{type:String,default:'unknown'},transactionHour:Number,
  riskScore:Number,riskLevel:{type:String,enum:['LOW','MEDIUM','HIGH'],index:true},ruleRiskScore:Number,mlAnomalyScore:Number,isAnomaly:Boolean,riskReasons:[String],aiExplanation:String,
  modelVersion:String,riskThresholds:{medium:Number,high:Number},featureSnapshot:mongoose.Schema.Types.Mixed,
  feedbackLabel:{type:String,enum:['unreviewed','legitimate','suspicious'],default:'unreviewed',index:true},feedbackNote:String,reviewedAt:Date,
  paymentStatus:{type:String,enum:['completed','prevented','failed','pending']},razorpayOrderId:String,razorpayPaymentId:String
},{timestamps:true});
schema.index({userId:1,beneficiary:1,createdAt:-1});schema.index({userId:1,createdAt:-1});
export default mongoose.models.Transaction||mongoose.model('Transaction',schema);
