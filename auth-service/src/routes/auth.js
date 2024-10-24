import express from 'express';
import passport from 'passport';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import User from '../models/User.js';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { check, validationResult } from 'express-validator';
import redis from 'redis';

// Initialize Redis client
const redisClient = redis.createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

// Read the disposable email domains JSON file once at the start
const disposableDomains = JSON.parse(
  readFileSync(resolve('node_modules/disposable-email-domains/index.json'), 'utf-8')
);

const router = express.Router();

// GET /auth route for testing purposes
router.get('/', (req, res) => {
  res.status(200).json({ message: 'Auth route is working' });
});

// Sign-up route (email) with validation and password hashing
router.post(
  '/signup',
  [
    check('email').isEmail().withMessage('Invalid email address'),
    check('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters long'),
    check('name').notEmpty().withMessage('Name is required'),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { email, password, name } = req.body;
    const domain = email.split('@')[1];

    // Check if email domain is disposable
    if (disposableDomains.includes(domain)) {
      return res.status(400).json({ message: 'Disposable emails are not allowed' });
    }

    try {
      // Hash the password before saving it
      const hashedPassword = await bcrypt.hash(password, 10);
      const user = new User({ email, password: hashedPassword, name });
      await user.save();
      res.status(201).json({ message: 'User created successfully' });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
);

// Login route (email) with failed attempt tracking in Redis and JWT generation
router.post(
  '/login',
  [
    check('email').isEmail().withMessage('Invalid email address'),
    check('password').exists().withMessage('Password is required'),
  ],
  async (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { email } = req.body;

    // Track failed login attempts in Redis
    const failedAttempts = await redisClient.get(`failedAttempts:${email}`);
    if (failedAttempts && failedAttempts >= 5) {
      return res.status(429).json({ message: 'Too many login attempts. Try again later.' });
    }

    passport.authenticate('local', { session: false }, async (err, user) => {
      if (err) return next(err);

      if (!user) {
        // Increment failed login attempts
        await redisClient.incr(`failedAttempts:${email}`);
        await redisClient.expire(`failedAttempts:${email}`, 15 * 60); // Expire after 15 minutes
        return res.status(400).json({ message: 'Login failed' });
      }

      // Reset failed attempts on successful login
      await redisClient.del(`failedAttempts:${email}`);

      // Generate JWT token
      const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
      return res.json({ token });
    })(req, res, next);
  }
);

export default router;
