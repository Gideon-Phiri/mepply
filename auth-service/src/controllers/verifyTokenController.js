import jwt from 'jsonwebtoken';


export const verifyToken = (req, res) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'Token is missing!' });
  }

  try {
    // Verify token with the same secret used for signing
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Send back decoded user information if token is valid
    return res.status(200).json({ userId: decoded.id });
  } catch (error) {
    console.error("Error verifying token:", error);
    return res.status(401).json({ message: 'Invalid or expired token' });
  }
};
