import * as chai from 'chai'
import {default as chaiHttp, request} from 'chai-http'
import app from '../src/index.js';

chai.use(chaiHttp);
chai.should();

describe('Auth Service', () => {
  let server;

  // Start the server on a different port for testing
  before((done) => {
    server = app.listen(4000, () => {
      console.log('Test server running on port 4000');
      done();
    });
  });

  // Close the server after tests are done
  after(() => {
    server.close();
  });

  // Test GET /auth route
  it('should have a running server', (done) => {
    request.execute(server) // Using server running on port 4000
      .get('/auth')      // Make sure this matches the correct route
      .end((err, res) => {
        if (err) done(err);  // Handle request error
        res.should.have.status(200); // Expect 200 OK
        done();
      });
  });
});
