import User from '../models/User.js';
import bcrypt from 'bcryptjs';

export const signup = async (req, res) => {
  const { email, password, name } = req.body;
  try {
    // Check if user with the same email already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(409).json({ message: 'User with this email already exists' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const user = new User({ email, password: hashedPassword, name });
    await user.save();
    res.status(201).json({ message: 'User created successfully' });
  } catch (error) {
    // Enhanced error handling for MongoDB duplicate key error
    if (error.code === 11000) {
      return res.status(409).json({ message: 'Email is already registered' });
    }
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};
