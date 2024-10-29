import express from 'express';
import { requestPasswordReset, resetPassword } from '../../controllers/passwordController.js';

const router = express.Router();

// POST /auth/request-password-reset
router.post('/request-password-reset', requestPasswordReset);

// POST /auth/reset-password
router.post('/reset-password', resetPassword);

export default router;
