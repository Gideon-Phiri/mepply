import express from 'express';
import passport from 'passport';
import mongoose from 'mongoose';
import session from 'express-session';
import RedisStore from 'connect-redis';
import redis from 'redis';
import authRoutes from './routes/auth.js';
import dotenv from 'dotenv';
import cors from 'cors';
import rateLimit from 'express-rate-limit';

dotenv.config();

const app = express();

// Create and connect Redis client
const redisClient = redis.createClient({ url: process.env.REDIS_URL });
redisClient.on('error', (err) => console.log('Redis Client Error', err));

await redisClient.connect(); // Wait for Redis to connect

app.use(express.json()); // Parse JSON request bodies

// Redis-based session management
app.use(
  session({
    store: new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: true,
    cookie: {
      secure: process.env.NODE_ENV === 'production', // Set secure cookies in production
      httpOnly: true, // Prevent JavaScript access to cookies
    },
  })
);

// MongoDB connection
mongoose.connect(process.env.MONGO_URL)
  .then(() => console.log('MongoDB connected'))
  .catch((err) => console.log('MongoDB connection error:', err));

// Rate limiting to prevent brute-force attacks
const limiter = rateLimit({
  windowMs: 10 * 60 * 1000, // 10 minutes
  max: 40, // Limit each IP to 100 requests per window
  message: 'Too many requests, please try again later.',
});
app.use(limiter); // Apply rate limiting globally

// CORS configuration to allow trusted domains
const corsOptions = {
  origin: [
    'https://your-frontend-domain.com', // TODO: frontend domain will go here
    'https://another-service.com',      // Another microservice
    'http://localhost:4000',            // Allow local development
  ],
  optionsSuccessStatus: 200,
};
app.use(cors(corsOptions)); // Apply CORS

// Enforce HTTPS in production
if (process.env.NODE_ENV === 'production') {
  app.use((req, res, next) => {
    if (req.headers['x-forwarded-proto'] !== 'https') {
      return res.redirect(`https://${req.headers.host}${req.url}`);
    }
    next();
  });
}

// Passport configuration
import './config/passport.js';
app.use(passport.initialize());
app.use(passport.session());

// Routes
app.use('/auth', authRoutes);


export default app;
