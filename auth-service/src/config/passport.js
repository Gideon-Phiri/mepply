import passport from 'passport';
import { Strategy as LocalStrategy } from 'passport-local';
import { Strategy as GoogleTokenStrategy } from 'passport-google-token';
import { Strategy as LinkedInTokenStrategy } from 'passport-linkedin-oauth2';
import bcrypt from 'bcryptjs';
import User from '../models/User.js';
import dotenv from 'dotenv';

dotenv.config();

// Local Strategy for Email/Password Authentication
passport.use(new LocalStrategy({
  usernameField: 'email',    // map 'email' to usernameField expected by passport-local
  passwordField: 'password', // map 'password' to passwordField expected by passport-local
  session: false             // disable sessions for JWT-based authentication
}, async (email, password, done) => {
  try {
    // Find user by email
    const user = await User.findOne({ email });
    if (!user) {
      return done(null, false, { message: 'Invalid email or password' });
    }

    // Compare passwords using bcrypt
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return done(null, false, { message: 'Invalid email or password' });
    }

    // Success: return the user
    return done(null, user);
  } catch (error) {
    return done(error);
  }
}));

// Google Token Strategy for Token-Based OAuth
passport.use(
  'google-token', new GoogleTokenStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: 'http://localhost:3000/auth/google/callback',
  },
  async (accessToken, refreshToken, profile, done) => {
    try {
      let user = await User.findOne({ googleId: profile.id });
      if (!user) {
        user = await User.create({
          googleId: profile.id,
          email: profile.emails[0].value,
          name: profile.displayName,
        });
      }
      return done(null, user);
    } catch (err) {
      done(err);
    }
  })
);


// LinkedIn Token Strategy for Token-Based OAuth
passport.use('linkedin-token', new LinkedInTokenStrategy({
  clientID: process.env.LINKEDIN_CLIENT_ID,
  clientSecret: process.env.LINKEDIN_CLIENT_SECRET,
  callbackURL: `${process.env.API_URL}/auth/linkedin/callback`,
  scope: ['r_emailaddress', 'r_liteprofile'],
}, async (accessToken, refreshToken, profile, done) => {
  try {
    let user = await User.findOne({ linkedinId: profile.id });
    if (!user) {
      user = new User({
        linkedinId: profile.id,
        name: profile.displayName,
        email: profile.emails[0].value,
      });
      await user.save();
    }
    done(null, user);
  } catch (error) {
    done(error, null);
  }
}));
