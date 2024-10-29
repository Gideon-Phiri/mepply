import express from 'express';
import { login } from '../../controllers/loginController.js';
import { loginValidation } from '../../middlewares/inputValidation.js';

const router = express.Router();

// POST /auth/login
router.post('/login', loginValidation, login);

export default router;
