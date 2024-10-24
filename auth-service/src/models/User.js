import mongoose from 'mongoose'
import bcrypt from 'bcryptjs'

const userSchema = new mongoose.Schema({
  googleId: { type: String },
  appleId: { type: String },
  email: { type: String, unique: true },
  password: { type: String }, // For email authentication
  name: { type: String, required: true },
  role: { type: String, default: 'user' }, // Role-based access control
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
