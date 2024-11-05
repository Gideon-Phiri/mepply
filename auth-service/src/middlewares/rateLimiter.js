import rateLimit from 'express-rate-limit';

// Global rate limiter for all routes
export const globalRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per 15 minutes for all routes
  message: 'Too many requests, please try again later.',
});

// Custom rate limiter for login routes
export const loginRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Limit to 5 requests per 15 minutes for login/signup
  message: 'Too many login/signup attempts, please try again later.',
});

// Custom rate limiter for sign-up routes
export const signUpRateLimiter = rateLimit({
  windowMs: 20 * 60 * 1000, // 15 minutes 
  max: 5, // Limit to 5 requests per 20 minutes for signup
  message: 'Too many signup attempts, please try again later.',                                                           });

export const passwordResetLimiter = rateLimit({
  windowMs: 30 * 60 * 1000, // 30 minutes
  max: 3, // 3 requests per 30 minutes
  message: 'Too many password reset attempts, please try again later.',
});
