import jwt from 'jsonwebtoken';
import passport from 'passport';
import dotenv from 'dotenv';

dotenv.config();


export const login = (req, res, next) => {
  passport.authenticate('local', { session: false }, (err, user, info) => {
    if (err) {
      return res.status(500).json({ message: 'Server error', error: err.message });
    }
    if (!user) {
      return res.status(400).json({ message: info.message });
    }

    // Generate a JWT token if authentication succeeds
    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    return res.json({ token });
  })(req, res, next);
};
