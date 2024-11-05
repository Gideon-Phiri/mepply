import * as chai from 'chai';
import { default as chaiHttp, request } from 'chai-http';
import app from '../src/index.js';

chai.use(chaiHttp);
chai.should();

describe('Social Login', () => {
  let server;

  before((done) => {
    server = app.listen(4000, () => {
      console.log('Test server running on port 4000');
      done();
    });
  });

  after((done) => {
    server.close(() => done());
  });

  it('should authenticate with Google', (done) => {
    request.execute(server)
      .post('/auth/google')
      .send({ token: 'mockGoogleToken' }) // Replace with valid token for live test
      .end((err, res) => {
        if (err) done(err);
        res.should.have.status(200);
        res.body.should.have.property('token');
        done();
      });
  });

  it('should authenticate with LinkedIn', (done) => {
    request.execute(server)
      .post('/auth/linkedin')
      .send({ token: 'mockLinkedInToken' }) // Replace with valid token for live test
      .end((err, res) => {
        if (err) done(err);
        res.should.have.status(200);
        res.body.should.have.property('token');
        done();
      });
  });
});
