import passport from 'passport';
import { Strategy as LocalStrategy } from 'passport-local';
//import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
//import { Strategy as LinkedInStrategy } from 'passport-linkedin-oauth2';
import bcrypt from 'bcryptjs';
import User from '../models/User.js';
import dotenv from 'dotenv';

dotenv.config();

// Local Strategy for Email/Password Authentication
passport.use(new LocalStrategy({
  usernameField: 'email',
  passwordField: 'password',
}, async (email, password, done) => {
  try {
    const user = await User.findOne({ email });
    if (!user) {
      return done(null, false, { message: 'Invalid email or password' });
    }
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return done(null, false, { message: 'Invalid email or password' });
    }
    return done(null, user);
  } catch (error) {
    return done(error);
  }
}));

// Google OAuth Strategy
/*passport.use(
  new GoogleStrategy({
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


// LinkedIn OAuth Strategy
passport.use(new LinkedInStrategy({
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

// Serialize and Deserialize user instances for session management
passport.serializeUser((user, done) => done(null, user.id));
passport.deserializeUser(async (id, done) => {
  const user = await User.findById(id);
  done(null, user);
});*/
