'use strict';

const pkg = require('./package.json');

module.exports = (api) => {
  const callerName = api.caller(caller => caller && caller.name);
  const isWebpack = callerName.startsWith('babel-loader');
  // Tools like jest cannot use es6 modules because they are based on node!
  const presetEnvOptions = isWebpack
    ? {
      modules: false,
      useBuiltIns: 'entry',
      corejs: 3,
      targets: pkg.browserslist
    }
    : {
      targets: {
        node: 'current'
      }
    };
  return {
    sourceType: "unambiguous",
    presets: [
      ["@babel/env", presetEnvOptions],
      "@babel/preset-react",
      "@babel/preset-typescript"
    ],
    "plugins": [
      [
        "@babel/plugin-proposal-decorators",
        {
          "legacy": true
        }
      ],
      "@babel/plugin-proposal-class-properties",
      "@babel/plugin-proposal-export-default-from",
      '@babel/plugin-proposal-object-rest-spread',
      '@babel/plugin-syntax-dynamic-import',
      '@babel/plugin-proposal-optional-chaining',
      '@babel/plugin-proposal-nullish-coalescing-operator',
      ['@babel/plugin-transform-runtime', {
        useESModules: false
      }],
    ]
  };
};
