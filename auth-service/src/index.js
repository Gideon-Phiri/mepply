import express from 'express';
import session from 'express-session';
import RedisStore from 'connect-redis';
import redis from 'redis';
import passport from 'passport';
import helmet from 'helmet';
import cors from 'cors';
import dotenv from 'dotenv';
import { globalRateLimiter } from './middlewares/rateLimiter.js';
import authRoutes from './routes/auth.js';
import connectDB from './config/db.js';

dotenv.config();

// Initialize express app
const app = express();

// Connect to MongoDB
connectDB();

// Initialize Redis client
const redisClient = redis.createClient({ url: process.env.REDIS_URL });
redisClient.on('error', (err) => console.log('Redis Client Error', err));
await redisClient.connect();

// Apply global rate limiter to all routes
app.use(globalRateLimiter);

// Apply CORS for trusted domains only
app.use(cors({
  origin: ['https://your-frontend-domain.com', 'http://localhost:4000'],
}));

// Apply Helmet for various security headers
app.use(helmet());

// Redis-based session management with secure cookies in production
app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: true,
  cookie: {
    secure: process.env.NODE_ENV === 'production', // Secure cookies in production
    httpOnly: true, // Prevent JavaScript access to cookies
  },
}));

// Passport initialization
import './config/passport.js';
app.use(passport.initialize());
app.use(passport.session());

// Mount /auth routes
app.use('/auth', authRoutes);

export default app;
