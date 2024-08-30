/* NOTE: This files is not transpiled, so be sure to write native browser compatible code here */
/* eslint-disable */

'use strict';

const getSeeqApi = (function () {
  const listeners = {};
  const lastValues = {};
  const pendingRequests = {};

  let port;

  const noop = function (...x) {};
  const nooutput = { log: noop, warn: noop };
  const debug = nooutput; // can replace this with 'console' to get debug logs to console

  function arrayRealLength(a) {
    return a.filter((e) => e !== undefined).length;
  }

  function createNonce() {
    let nonce = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    for (let i = 0; i < 20; i++) nonce += possible.charAt(Math.floor(Math.random() * possible.length));

    return pendingRequests[nonce] ? createNonce() : nonce;
  }

  function invoke(type, fn, args = [], transfer = []) {
    if (port) {
      const nonce = createNonce();
      const result = new Promise((resolve, reject) => (pendingRequests[nonce] = { resolve, reject }));
      port.postMessage({ type, payload: { function: fn, args }, nonce }, transfer);
      return result;
    }
  }

  function invokeVoid(fn, args = [], transfer = []) {
    debug.log('invoke void', fn, args);
    if (port) {
      port.postMessage({ type: 'invokeVoid', payload: { function: fn, args } }, transfer);
    }
  }

  function unsubscribe(fn) {
    debug.log('unsubscribe listener', fn);
    if (port) {
      port.postMessage({ type: 'invokeVoid', payload: { function: fn, unsubscribe: true } }, []);
    }
  }

  function generateApi(apiConfig, done) {
    const API = {};
    apiConfig.properties.forEach(function (property) {
      if (property.path === 'ROOT') {
        API[property.name] = property.value;
      } else {
        const pathParts = property.path.split('.');
        let parent = API;
        for (let i = 0; i < pathParts.length; i++) {
          if (parent[pathParts[i]] === undefined) {
            parent[pathParts[i]] = {};
          }
          parent = parent[pathParts[i]];
        }
        parent[property.name] = property.value;
      }
    });

    apiConfig.functions.forEach(function (fn) {
      let parent = API;
      if (fn.path !== 'ROOT') {
        const pathParts = fn.path.split('.');
        for (let i = 0; i < pathParts.length; i++) {
          if (parent[pathParts[i]] === undefined) {
            parent[pathParts[i]] = {};
          }
          parent = parent[pathParts[i]];
        }
      }
      const callName = fn.path + ' -> ' + fn.name;
      const type = apiConfig[callName].type;
      if (type === 'listenTo') {
        listeners[callName] = [];
        parent[fn.name] = function (listener) {
          const idx = listeners[callName].length;
          listeners[callName].push(listener);
          if (idx === 0) {
            invokeVoid(callName);
          } else if (lastValues[callName] !== undefined) {
            const version = lastValues[callName].version;
            setTimeout(() => {
              if (version === lastValues[callName].version) {
                listener(lastValues[callName].value);
              }
            });
          }
          return function () {
            delete listeners[callName][idx];
            if (arrayRealLength(listeners[callName]) === 0) {
              listeners[callName] = [];
              delete lastValues[callName];
              unsubscribe(callName);
            }
          };
        };
      } else if (type === 'invokeVoid') {
        parent[fn.name] = function () {
          invokeVoid(callName, Array.prototype.slice.call(arguments));
        };
      } else if (type === 'invoke' || type === 'invokeAsync') {
        parent[fn.name] = function () {
          return invoke(type, callName, Array.prototype.slice.call(arguments));
        };
      }
    });

    done(API);
  }

  function onMessageFactory(apiGenerationDone) {
    return function (event) {
      if (event.isTrusted && event.data.type) {
        const m = event.data;
        if (m.type === 'apiConfig') {
          generateApi(m.payload, apiGenerationDone);
        } else if (m.type === 'invocationResult' && pendingRequests[m.nonce] && m.payload) {
          if (m.payload.error === undefined) {
            pendingRequests[m.nonce].resolve(m.payload.result);
          } else {
            pendingRequests[m.nonce].reject(m.payload.error);
          }
          delete pendingRequests[m.nonce];
        } else if (m.type === 'listenerUpdate' && m.payload && arrayRealLength(listeners[m.payload.name]) > 0) {
          const version = lastValues[m.payload.name] !== undefined ? lastValues[m.payload.name].version + 1 : 0;
          lastValues[m.payload.name] = {
            version,
            value: Object.freeze(m.payload.value),
          };
          listeners[m.payload.name].forEach((l) => l(m.payload.value));
        }
        debug.log('message received in plugin', m);
      }
    };
  }

  const SEEQ = new Promise(function (resolve) {
    const init = function (event) {
      if (event.isTrusted && event.source === window.parent && event.data === 'init') {
        port = event.ports[0];
        port.onmessage = onMessageFactory(resolve);
        window.removeEventListener('message', init, false);
        port.postMessage({ type: 'init successful' });
      }
    };
    window.addEventListener('message', init, false);
  });

  return () => SEEQ;
})();
