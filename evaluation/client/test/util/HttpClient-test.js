/*! @license ©2014 Ruben Verborgh - Multimedia Lab / iMinds / Ghent University */
var HttpClient = require('../../lib/util/HttpClient');

var EventEmitter = require('events').EventEmitter,
    Iterator = require('../../lib/iterators/Iterator');

describe('HttpClient', function () {
  describe('The HttpClient module', function () {
    it('should be a function', function () {
      HttpClient.should.be.a('function');
    });

    it('should make HttpClient objects', function () {
      HttpClient().should.be.an.instanceof(HttpClient);
    });

    it('should be an HttpClient constructor', function () {
      new HttpClient().should.be.an.instanceof(HttpClient);
    });
  });

  describe('An HttpClient without arguments', function () {
    var request = new EventEmitter();
    var createRequest = sinon.stub().returns(request);
    var client = new HttpClient({ request: createRequest });

    describe('get http://example.org/foo', function () {
      var response = client.get('http://example.org/foo'), contentType;
      request.emit('response', createResponse([1, 2, 3], 'text/html;encoding=utf8'));

      it('should call request once with the URL and accept "*/*"', function () {
        createRequest.should.have.been.calledOnce;
        createRequest.should.have.been.calledWithMatch({
          url: 'http://example.org/foo',
          method: 'GET',
          headers: { accept: '*/*' },
        });
      });

      it("should return an iterator with the response's contents", function (done) {
        response.should.be.an.iteratorOf([1, 2, 3], done);
      });

      it('should set the status code', function (done) {
        response.getProperty('statusCode', function (statusCode) {
          statusCode.should.equal(200);
          done();
        });
      });

      it('should set the content type', function (done) {
        response.getProperty('contentType', function (contentType) {
          contentType.should.equal('text/html');
          done();
        });
      });
    });
  });

  describe('An HttpClient with content type "text/turtle"', function () {
    var request = new EventEmitter();
    var createRequest = sinon.stub().returns(request);
    var client = new HttpClient({ request: createRequest, contentType: 'text/turtle' });

    describe('get http://example.org/foo', function () {
      var response = client.get('http://example.org/foo'), contentType;
      request.emit('response', createResponse([1, 2, 3], 'text/turtle;encoding=utf8'));

      it('should call request once with the URL and accept "text/turtle"', function () {
        createRequest.should.have.been.calledOnce;
        createRequest.should.have.been.calledWithMatch({
          url: 'http://example.org/foo',
          method: 'GET',
          headers: { accept: 'text/turtle' },
        });
      });

      it('should return the request value', function (done) {
        response.should.be.an.iteratorOf([1, 2, 3], done);
      });

      it('should set the status code', function (done) {
        response.getProperty('statusCode', function (statusCode) {
          statusCode.should.equal(200);
          done();
        });
      });

      it('should set the content type', function (done) {
        response.getProperty('contentType', function (contentType) {
          contentType.should.equal('text/turtle');
          done();
        });
      });
    });
  });
});

// Creates a dummy HTTP response
function createResponse(contents, contentType) {
  var response = Iterator.fromArray(contents);
  response.statusCode = 200;
  response.headers = { 'content-type': contentType };
  return response;
}
