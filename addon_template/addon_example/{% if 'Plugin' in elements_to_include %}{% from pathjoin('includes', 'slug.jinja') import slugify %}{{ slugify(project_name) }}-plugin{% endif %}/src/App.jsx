// @ts-ignore: TS2532 
import React, { useEffect, useState } from 'react';
import { Toolbar } from './Toolbar';
import _ from 'lodash';
import './App.scss';
import Chart from './Chart';
import { useWindowSize } from './hooks';

let fetching = false;
let lastData;
let signals;
let range;
let seeq;

function App() {
  const [isPresentationMode, setPM] = useState(false);
  const [chart, setChart] = useState();
  const [initPromises, setInitPromises] = useState([]);
  const [data, setData] = useState([]);
  const TOOLBAR_HEIGHT = 50;
  const CHART_ID = 'theChart';
  const size = useWindowSize();

  useEffect(() => {
    if (!seeq) {
      getSeeqApi().then((_seeq) => {
        seeq = _seeq;
        setPM(_seeq.isPresentationWorkbookMode);
        setChart(new Chart(CHART_ID));
        _seeq.subscribeToSignals(init(signals => syncSignals(signals)));
        _seeq.subscribeToDisplayRange(init(range => syncDisplayRange(range)));
        Promise.all(initPromises).then(() => _seeq.pluginRenderComplete());
      });
    }

    if (chart && size.width && size.height) {
      chart.render(size.width, size.height - TOOLBAR_HEIGHT, data);
    }
  });

  function syncSignals(_signals) {
    // Only display signals and properties that can have an average value computed
    const newSignals = _.chain(_signals)
      .reject(s => s.valueUnitOfMeasure === 'string')
      .map(s => _.pick(s, ['id', 'name', 'color', 'valueUnitOfMeasure']))
      .value();

    if (!_.isEqual(newSignals, signals)) {
      signals = newSignals;
      fetchAverageValuesData();
    }
  }

  function syncDisplayRange(_range) {
    range = _range;
    fetchAverageValuesData();
  }

  function fetchAverageValuesData() {
    if (!signals || !range || fetching) {
      return;
    }

    const cancellationGroup = 'fetchAverageCancellationGroup';
    const startIso = new Date(range.start).toISOString();
    const endIso = new Date(range.end).toISOString();
    fetching = true;

    _.chain(signals)
      .map(s => {
        seeq.setTrendDataStatusLoading(s.id);

        const formula = `group(capsule("${startIso}", "${endIso}")).toTable('stats').addStatColumn('series', $series, average())`;
        const parameters = { series: s.id };

        return seeq.runFormula({ formula, parameters, cancellationGroup })
          .then(results => {
            const average = _.get(results, 'data.table.data[0][2]');
            const header = _.get(results, 'data.table.headers[2]');
            const valueUnitOfMeasure = header.type === 'string' ? 'string' : header.units;
            let dummySample = [{ key: range.start + 1, value: average }, { key: range.end - 1, value: average }];

            seeq.setTrendDataStatusSuccess({
              id: s.id,
              samples: dummySample,
              timingInformation: results.info.timingInformation,
              meterInformation: results.info.meterInformation,
              valueUnitOfMeasure,
              warningCount: results.data.warningCount,
              warningLogs: results.data.warningLogs
            });

            return { id: s.id, name: s.name, color: s.color, valueUnitOfMeasure, value: average };
          })
          .catch(error => {
            seeq.catchItemDataFailure(s.id, cancellationGroup, error);
          });
      })
      .thru(promises => Promise.all(promises))
      .value()
      .then(newData => {
        if (!_.isEqual(newData, lastData)) {
          setData(newData);
          lastData = newData;
        }
      })
      .finally(() => {
        fetching = false;
      });
  }

  // Wraps a callback function and resolves a promise when the callback is completed
  function init(func) {
    let resolve;
    setInitPromises(initPromises.push(new Promise(r => { resolve = r; })));
    return (...args) => {
      func(...args);
      resolve();
    };
  };

  const toolbar = !isPresentationMode ? (<Toolbar />) : null;

  return (
    <div className="App">
      {toolbar}
      <div className="chartContainer">
        <div id={CHART_ID}></div>
      </div>
    </div>
  );
}

export default App;
