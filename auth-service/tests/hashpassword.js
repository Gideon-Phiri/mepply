import bcrypt from 'bcryptjs';


bcrypt.hash('testpassword', 10, function(err, hash) {
  if (err) throw err;
  console.log("Hashed password:", hash);
});
