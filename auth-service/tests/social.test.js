import * as chai from 'chai';
import { default as chaiHttp, request } from 'chai-http';
import app from '../src/index.js';

chai.use(chaiHttp);
chai.should();

describe('Social Login', () => {
    let server;

    before((done) => {
    server = app.listen(4000, () => done());
  });

  after((done) => {
    if (server) server.close(done);
  });


    it('should authenticate with Google', (done) => {
       request.execute(app)
          .get('/auth/google') // Endpoint for initiating Google OAuth
          .end((err, res) => {
            if (err) return done(err);
            res.should.have.status(200);
            res.body.should.have.property('token');
            done();
      });
  });

  it('should authenticate with LinkedIn', (done) => {
    request.execute(app)
      .get('/auth/linkedin') // Endpoint for initiating LinkedIn OAuth
      .end((err, res) => {
        if (err) return done(err);
        res.should.have.status(200);
        res.body.should.have.property('token');
        done();
      });
  });
});
