import express from 'express';
import passport from 'passport';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { signupValidation, loginValidation } from '../middlewares/inputValidation.js';
import { blockDisposableEmails } from '../middlewares/disposableEmailCheck.js';
import { signUpRateLimiter, loginRateLimiter } from '../middlewares/rateLimiter.js';
import User from '../models/User.js';

const router = express.Router();

// GET /auth route for testing purposes
router.get('/', (req, res) => {
  res.status(200).json({ message: 'Auth route is working' });
});

// POST /auth/signup route with rate limiting, validation, and disposable email checks
router.post('/signup', signUpRateLimiter, signupValidation, blockDisposableEmails, async (req, res) => {
  const { email, password, name } = req.body;
  try {
    const hashedPassword = await bcrypt.hash(password, 10); // Hash password
    const user = new User({ email, password: hashedPassword, name });
    await user.save();
    res.status(201).json({ message: 'User created successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// POST /auth/login route with rate limiting and validation
router.post('/login', loginRateLimiter, loginValidation, (req, res, next) => {
  passport.authenticate('local', { session: false }, (err, user, info) => {
    if (err) return next(err);
    if (!user) return res.status(400).json({ message: info.message });

    // Generate JWT token
    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    return res.json({ token });
  })(req, res, next);
});

export default router;
