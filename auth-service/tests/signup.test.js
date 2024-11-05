import * as chai from 'chai';
import { default as chaiHttp, request } from 'chai-http';
import app from '../src/index.js';
import User from '../src/models/User.js';

chai.use(chaiHttp);
chai.should();

describe('User Signup', () => {
  let server;

  before((done) => {
    server = app.listen(4000, () => {
      done();
    });
  });

  after(async () => {
    await User.deleteMany({});  // Cleanup users after tests
    server.close();
  });

  it('should successfully sign up a new user', (done) => {
    request.execute(server)
      .post('/auth/signup')
      .send({ email: 'temwanisha@gmail.com', password: 'testpassword', name: 'Temwa' })
      .end((err, res) => {
        res.should.have.status(201);
        res.body.should.have.property('message').eql('User created successfully');
        done();
      });
  });

  it('should block sign-up with disposable email', (done) => {
    request.execute(server)
      .post('/auth/signup')
      .send({ email: 'temporary@mailinator.com', password: 'Password123', name: 'Temporary User' })
      .end((err, res) => {
        res.should.have.status(400);
        res.body.should.have.property('message').eql('Disposable emails are not allowed');
        done();
      });
  });
});
