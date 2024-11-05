import passport from 'passport';
import jwt from 'jsonwebtoken';

export const googleLogin = (req, res, next) => {
  passport.authenticate('google-token', { session: false }, (err, user) => {
    if (err || !user) {
      return res.status(400).json({ message: 'Google authentication failed' });
    }

    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.json({ token });
  })(req, res, next);
};

export const linkedinLogin = (req, res, next) => {
  passport.authenticate('linkedin-token', { session: false }, (err, user) => {
    if (err || !user) {
      return res.status(400).json({ message: 'LinkedIn authentication failed' });
    }

    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.json({ token });
  })(req, res, next);
};
