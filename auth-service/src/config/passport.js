import GoogleStrategy from 'passport-google-oauth20'
import AppleStrategy from 'passport-apple'
import LocalStrategy from 'passport-local'
import User from '../models/User.js'
import bcrypt from 'bcryptjs'

export default function(passport) {
  // Google OAuth 2.0
  passport.use(
    new GoogleStrategy(
      {
        clientID: process.env.GOOGLE_CLIENT_ID,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        callbackURL: '/auth/google/callback',
      },
      async (accessToken, refreshToken, profile, done) => {
        const existingUser = await User.findOne({ googleId: profile.id })
        if (existingUser) return done(null, existingUser)

        const newUser = new User({ googleId: profile.id, name: profile.displayName })
        await newUser.save()
        done(null, newUser)
      }
    )
  )

  // Apple OAuth 2.0
  passport.use(
    new AppleStrategy(
      {
        clientID: process.env.APPLE_CLIENT_ID,
        clientSecret: process.env.APPLE_CLIENT_SECRET,
        callbackURL: '/auth/apple/callback',
      },
      async (accessToken, refreshToken, profile, done) => {
        const existingUser = await User.findOne({ appleId: profile.id })
        if (existingUser) return done(null, existingUser)

        const newUser = new User({ appleId: profile.id, name: profile.displayName })
        await newUser.save()
        done(null, newUser)
      }
    )
  )

  // Local strategy for email/password login
  passport.use(
    new LocalStrategy(
      { usernameField: 'email' },
      async (email, password, done) => {
        try {
          const user = await User.findOne({ email })
          if (!user) return done(null, false, { message: 'User not found' })

          const isMatch = await bcrypt.compare(password, user.password)
          if (!isMatch) return done(null, false, { message: 'Incorrect password' })

          return done(null, user)
        } catch (error) {
          return done(error)
        }
      }
    )
  )

  passport.serializeUser((user, done) => done(null, user.id))
  passport.deserializeUser((id, done) => User.findById(id, done))
}
