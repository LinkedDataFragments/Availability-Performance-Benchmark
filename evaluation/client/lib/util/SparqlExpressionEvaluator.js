/*! @license ©2014 Ruben Verborgh - Multimedia Lab / iMinds / Ghent University */
/** A SparqlExpressionEvaluator evaluates SPARQL expressions into values. */

var N3Util = require('n3').Util;

// Creates a function that evaluates the given expression
function SparqlExpressionEvaluator(expression) {
  if (!expression) return noop;
  var evaluator = evaluators[expression && expression.type || null];
  if (!evaluator) throw new Error('Unsupported expression type: ' + expression.type);
  return evaluator(expression);
}

// Evaluates the expression with the given bindings
SparqlExpressionEvaluator.evaluate = function (expression, bindings) {
  return SparqlExpressionEvaluator(expression)(bindings);
};

// The null operation
function noop () { }

// Creates an identity function for the given value
function createIdentityFunction(value) {
  return function () { return value; };
}

// Evaluators for each of the expression types
var evaluators = {
  // Does nothing
  null: function () { return noop; },

  // Evaluates a constant number
  number:   function (expression) { return createIdentityFunction(expression.value); },

  // Evaluates a constant literal
  literal:  function (expression) { return createIdentityFunction(expression.value); },

  // Evaluates a variable
  variable: function (expression) {
    return (function (varName) {
      return function (bindings) {
        if (!bindings || !(varName in bindings))
          throw new Error('Cannot evaluate variable ' + varName + ' because it is not bound.');
        return bindings[varName];
      };
    })(expression.value);
  },

  // Evaluates an operator
  operator: function (expression) {
    // Find the operator and check the number of arguments matches the expression
    var operatorName = expression.operator, operator = operators[operatorName];
    if (!operator)
      throw new Error('Unsupported operator: ' + expression.operator + '.');
    if (operator.length !== expression.arguments.length)
      throw new Error('Invalid number of arguments for ' + expression.operator +
                      ': ' + expression.arguments.length +
                      ' (expected: ' + operator.length + ').');

    // Special case: some operators accept expressions instead of evaluated expressions
    if (operator.acceptsExpressions) {
      return (function (operator, args) {
        return function (bindings) {
          return operator.apply(bindings, args);
        };
      })(operator, expression.arguments);
    }

    // Parse the expressions for each of the arguments
    var argumentExpressions = new Array(expression.arguments.length);
    for (var i = 0; i < expression.arguments.length; i++)
      argumentExpressions[i] = SparqlExpressionEvaluator(expression.arguments[i]);

    // Create a function that evaluates the operator with the arguments and bindings
    return (function (operator, argumentExpressions) {
      return function (bindings) {
        // Evaluate the arguments
        var args = new Array(argumentExpressions.length);
        for (var i = 0; i < argumentExpressions.length; i++) {
          var arg = args[i] = argumentExpressions[i](bindings);
          // Convert the arguments if necessary
          switch (operator.type) {
            case 'numeric':
              isFinite(arg) || (args[i] = parseFloat(N3Util.getLiteralValue(arg)));
              break;
            case 'boolean':
              if (arg !== false && arg !== true)
                throw new Error(operatorName + ' needs a boolean but got: ' + arg + '.');
              break;
          }
        }
        // Call the operator on the evaluated arguments
        return operator.apply(null, args);
      };
    })(operator, argumentExpressions);
  },
};

// Operators for each of the operator types
var operators = {
  '+':  function (a, b) { return a  +  b; },
  '-':  function (a, b) { return a  -  b; },
  '*':  function (a, b) { return a  *  b; },
  '/':  function (a, b) { return a  /  b; },
  '=':  function (a, b) { return a === b; },
  '!=': function (a, b) { return a !== b; },
  '<':  function (a, b) { return a  <  b; },
  '<=': function (a, b) { return a  <= b; },
  '>':  function (a, b) { return a  >  b; },
  '>=': function (a, b) { return a  >= b; },
  '!':  function (a)    { return !a;      },
  'and':function (a, b) { return a &&  b; },
  'or': function (a, b) { return a ||  b; },
  lang: function (a)    {
    return '"' + N3Util.getLiteralLanguage(a).toLowerCase() + '"';
  },
  langmatches: function (a, b) {
    return a.toLowerCase() === b.toLowerCase();
  },
  regex: function (subject, pattern) {
    return new RegExp(N3Util.getLiteralValue(pattern)).test(subject);
  },
  str: function (a) {
    return N3Util.isLiteral(a) ? a : '"' + a + '"';
  },
  'http://www.w3.org/2001/XMLSchema#double': function (a) {
    a = a.toFixed();
    if (a.indexOf('.') < 0) a += '.0';
    return '"' + a + '"^^<http://www.w3.org/2001/XMLSchema#double>';
  },
  bound: function (a) {
    if (a.type !== 'variable')
      throw new Error('BOUND expects a variable but got: ' + a.type + '.');
    return a.value in this;
  },
};

// Tag all operators that expect their arguments to be numeric
[
  '+', '-', '*', '/', '<', '<=', '>', '>=',
  'http://www.w3.org/2001/XMLSchema#double',
].forEach(function (operatorName) {
  operators[operatorName].type = 'numeric';
});

// Tag all operators that expect their arguments to be boolean
[
  '!', 'or', 'and',
].forEach(function (operatorName) {
  operators[operatorName].type = 'boolean';
});

// Tag all operators that take expressions instead of evaluated expressions
operators.bound.acceptsExpressions = true;

module.exports = SparqlExpressionEvaluator;
