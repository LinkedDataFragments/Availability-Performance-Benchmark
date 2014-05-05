/*! @license ©2014 Ruben Verborgh - Multimedia Lab / iMinds / Ghent University */

var DistinctIterator = require('../../lib/iterators/DistinctIterator');

var Iterator = require('../../lib/iterators/Iterator');

describe('DistinctIterator', function () {
  describe('The DistinctIterator module', function () {
    it('should make DistinctIterator objects', function () {
      DistinctIterator().should.be.an.instanceof(DistinctIterator);
    });

    it('should be a DistinctIterator constructor', function () {
      new DistinctIterator().should.be.an.instanceof(DistinctIterator);
    });

    it('should make Iterator objects', function () {
      DistinctIterator().should.be.an.instanceof(Iterator);
    });

    it('should be an Iterator constructor', function () {
      new DistinctIterator().should.be.an.instanceof(Iterator);
    });
  });

  describe('A DistinctIterator without source', function () {
    var iterator = new DistinctIterator();
    it('should have ended', function () {
      iterator.ended.should.be.true;
    });
  });

  describe('A DistinctIterator having an infinite window length', function () {
    describe('with a single item', function () {
      var iterator = new DistinctIterator(Iterator.single(1));
      it('should return the item', function (done) {
        iterator.should.be.an.iteratorOf([1], done);
      });
    });

    describe('with 8 items', function () {
      var iterator = new DistinctIterator(Iterator.fromArray([2, 1, 3, 3, 1, 2, 4, 2]));
      it('should return the unique items', function (done) {
        iterator.should.be.an.iteratorOf([2, 1, 3, 4], done);
      });
    });
  });

  describe('A DistinctIterator having window length 2', function () {
    describe('with a single item', function () {
      var iterator = new DistinctIterator(Iterator.single(1), { window: 2 });
      it('should return the item', function (done) {
        iterator.should.be.an.iteratorOf([1], done);
      });
    });

    describe('with 8 items', function () {
      var iterator = new DistinctIterator(Iterator.fromArray([2, 1, 3, 3, 1, 2, 4, 2]), { window: 2 });
      it('should return the sorted items', function (done) {
        iterator.should.be.an.iteratorOf([2, 1, 3, 2, 4], done);
      });
    });
  });
});
