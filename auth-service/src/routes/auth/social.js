import express from 'express';
import passport from 'passport';

const router = express.Router();

// Google OAuth Routes
router.get('/google', passport.authenticate('google', { scope: ['profile', 'email'] }));
router.get('/google/callback', passport.authenticate('google', { session: false }), (req, res) => {
  res.json({ token: req.user.token });
});

// LinkedIn OAuth Routes
router.get('/linkedin', passport.authenticate('linkedin'));
router.get('/linkedin/callback', passport.authenticate('linkedin', { session: false }), (req, res) => {
  res.json({ token: req.user.token });
});

export default router;
