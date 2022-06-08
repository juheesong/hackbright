'use strict';

function Main() {
  return (
    <React.Fragment>
      <h1>This site was created by Balloonicorn!</h1>
      <div>
        <a href="http://www.github.com/hackbrightacademy" target="_blank" rel="noreferrer">
          My Github!
        </a>
      </div>
      <div>
        <a href="/">Back to the Homepage</a>
      </div>
    </React.Fragment>
  );
}

ReactDOM.render(<Main />, document.querySelector('#main'));

