import mongoose from 'mongoose'
import bcrypt from 'bcryptjs'

const userSchema = new mongoose.Schema({
  googleId: { type: String },
  linkedInId: { type: String },
  email: { type: String, unique: true },
  password: { type: String },
  name: { type: String, required: true },
  subscription: { type: String, default: 'basic' }, // Subscription-based access control
  createdAt: { type: Date, default: Date.now }
})


const User = mongoose.model('User', userSchema)

export default User
