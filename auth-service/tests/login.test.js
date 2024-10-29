import * as chai from 'chai';
import { default as chaiHttp, request } from 'chai-http';
import app from '../src/index.js';  
import User from '../src/models/User.js';
import bcrypt from 'bcryptjs';

chai.use(chaiHttp);
chai.should();

describe('User Login', () => {
  let server;

  before(async (done) => {
    // Seed a user for login tests
    await User.create({ email: 'nishatemwa@gmail.com', password: await bcrypt.hash('testpassword', 10), name: 'Temwa' });
    server = app.listen(4000, () => done());
  });

  after(async (done) => {
    await User.deleteMany({});
    if (server) server.close(done);
  });

  it('should login successfully with correct credentials', (done) => {
    request.execute(server)
      .post('/auth/login')
      .send({ email: 'nishatemwa@gmail.com', password: 'testpassword' })
      .end((err, res) => {
        res.should.have.status(200);
        res.body.should.have.property('token');  // Ensure JWT token is returned
        done();
      });
  });

  it('should fail to login with incorrect credentials', (done) => {
    request.execute(server)
      .post('/auth/login')
      .send({ email: 'nishatemwa@gmail.com', password: 'wrongpassword' })
      .end((err, res) => {
        res.should.have.status(400);
        res.body.should.have.property('message').eql('Invalid email or password');
        done();
      });
  });
});
