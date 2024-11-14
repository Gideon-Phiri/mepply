import mongoose from 'mongoose'
import bcrypt from 'bcryptjs'

const userSchema = new mongoose.Schema({
  googleId: { type: String },
  linkedInId: { type: String },
  email: { type: String, unique: true },
  password: { type: String },
  subscription: { type: String, default: 'basic' }, // Subscription-based access control
  createdAt: { type: Date, default: Date.now }
})

// Hash the password before saving
userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next()
  this.password = await bcrypt.hash(this.password, 10)
  next()
})

const User = mongoose.model('User', userSchema)

export default User
