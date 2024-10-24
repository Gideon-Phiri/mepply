import { body } from 'express-validator';

export const signupValidation = [
  body('email').isEmail().withMessage('Must be a valid email address'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters long'),
  body('name').notEmpty().withMessage('Name is required'),
];

export const loginValidation = [
  body('email').isEmail().withMessage('Must be a valid email address'),
  body('password').exists().withMessage('Password is required'),
];
