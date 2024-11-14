import User from '../models/User.js';

export const signup = async (req, res) => {
  const { email, password, name } = req.body;
  try {
    // Check if a user with the same email already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(409).json({ message: 'User with this email already exists' });
    }

    // Create a new user
    const user = new User({ email, password, name });
    await user.save();

    res.status(201).json({ message: 'User created successfully' });

  } catch (error) {  // Add catch block here
    // Enhanced error handling for MongoDB duplicate key error
    if (error.code === 11000) {
      return res.status(409).json({ message: 'Email is already registered' });
    }
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};
