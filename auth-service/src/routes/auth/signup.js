import express from 'express';
import { signup } from '../../controllers/signupController.js';
import { signupValidation } from '../../middlewares/inputValidation.js';
//import { blockDisposableEmails } from '../../middlewares/disposableEmailCheck.js';

const router = express.Router();

// POST /auth/signup
router.post('/signup', signupValidation, signup);

export default router;
