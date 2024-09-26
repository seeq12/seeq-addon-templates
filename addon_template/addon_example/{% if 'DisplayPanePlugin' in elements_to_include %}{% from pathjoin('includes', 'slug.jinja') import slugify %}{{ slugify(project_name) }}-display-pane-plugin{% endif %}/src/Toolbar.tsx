import * as React from 'react';
import _ from 'lodash';

export function Toolbar(props) {
  const { } = props;

  const PADDING = 25;
  let _isMounted: boolean = false;
  let myRef = React.createRef<HTMLDivElement>();
  const [height, setHeight] = React.useState(0);
  let toolbarHeight;
  let _debouncedWindowResize = _.debounce(_handleWindowResize, 100);

  React.useEffect(() => {
    _isMounted = true;
    window.addEventListener('resize', _debouncedWindowResize);
    toolbarHeight = myRef.current.offsetHeight + PADDING;
    setHeight(calculateHeightForDropdowns());
    return () => {
      _isMounted = false;
      window.removeEventListener('resize', _debouncedWindowResize);
    };
  }, []);

  function calculateHeightForDropdowns() {
    return Math.max(0, window.innerHeight - toolbarHeight);
  }

  function _handleWindowResize() {
    if (_isMounted && myRef) {
      setHeight(calculateHeightForDropdowns());
    }
  }

  return (
    <div className="seeq-toolbar" ref={myRef}>
      <div>Example Visualization Display Pane Plugin</div>
    </div>
  );
}
