import * as chai from 'chai'
import {default as chaiHttp, request} from 'chai-http'
import app from '../src/index.js'

chai.use(chaiHttp)
chai.should()
//console.log(chai.request)
// Use a different port for tests
const testPort = 4000

describe('Auth Service', () => {
  let server
  before((done) => {
    // Start the server on a different port for testing
    server = app.listen(testPort, done)
  })

  after(() => {
    // Close the server after tests are done
    server.close()
  })

  it('should have a running server', (done) => {
    request.execute(app)   // Setting up an app
      .get('/auth')
      .end((err, res) => {
        res.should.have.status(200)
        done()
      })
  })
})
