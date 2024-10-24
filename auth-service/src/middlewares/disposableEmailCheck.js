import { readFileSync } from 'fs';
import { resolve } from 'path';

const disposableDomains = JSON.parse(readFileSync(resolve('node_modules/disposable-email-domains/index.json'), 'utf-8'));

export const blockDisposableEmails = (req, res, next) => {
  const { email } = req.body;
  const domain = email.split('@')[1];

  if (disposableDomains.includes(domain)) {
    return res.status(400).json({ message: 'Disposable email addresses are not allowed' });
  }
  
  next();
};
