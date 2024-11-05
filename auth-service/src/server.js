import app from './index.js';
import helmet from 'helmet';
import dotenv from 'dotenv';

dotenv.config();

// Enforce HTTPS and HSTS in production
if (process.env.NODE_ENV === 'production') {
  app.use((req, res, next) => {
    if (req.headers['x-forwarded-proto'] !== 'https') {
      return res.redirect(`https://${req.headers.host}${req.url}`);
    }
    next();
  });

  // Apply HSTS to enforce HTTPS
  app.use(helmet.hsts({
    maxAge: 31536000, // One year in seconds
    includeSubDomains: true, // Apply to all subdomains
  }));
}

// Server configuration
const PORT = process.env.PORT || 3000;

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

export default app;
