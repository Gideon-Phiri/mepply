import express from 'express';
import { verifyToken } from '../../controllers/verifyTokenController.js';


const router = express.Router();

// GET /auth/verify-token - Token verification endpoint for microservices
router.get('/verifyToken', verifyToken);

export default router;
