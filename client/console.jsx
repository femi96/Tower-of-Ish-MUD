'use strict';

class ClientConsole extends React.Component {
  constructor(props) {
    super(props);

    /*
      log - array of messages to display on client console
      value - value of current input
    */

    this.state = {
      log: [],
      value: '',
    };

    // Setup form handle functions
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleEventFromServer = this.handleEventFromServer.bind(this);

    // Setup socket
    // this.socket = new WebSocket('wss://echo.websocket.org');
    this.socket = new WebSocket('ws://localhost:8000');
    console.log("Try to Connect");

    // Socket on open
    this.socket.onopen = function (event) {
      console.log("Connected");
      // this.send("Ping"); 
    };

    // Socket on receive message
    var handleEventFromServer = this.handleEventFromServer;
    this.socket.onmessage = handleEventFromServer;

    // Socket on error
    this.socket.onerror = function (error) {
      console.log(error);
    };
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();

    // Exit if empty input
    if (this.state.value == '') {
      return;
    }

    // Send input to server
    this.socket.send(this.state.value);

    // Add input to log then reset input
    this.setState({
      log: this.state.log.concat(["> " + this.state.value]),
      value: '',
    }, this.scrollToBottom);
  }

  handleEventFromServer(event) {
    console.log(event.data);

    // Add message to log
    this.setState({
      log: this.state.log.concat([event.data]),
    }, this.scrollToBottom);
  }

  scrollToBottom() {
    this.logEnd.scrollIntoView({ behavior: "smooth" });
  }

  render() {

    // Create log lines
    const logItems = this.state.log.map((entry, index) =>
      <div className="log_line" key={index.toString()}>{entry}</div>
    );

    // Return console
    return (
      <div className="console">
        <div className="console_log">
          {logItems}
          <div style={{ float:"left", clear: "both" }} ref={(el) => { this.logEnd = el; }}></div>
        </div>

        <div className="console_input">
          <form onSubmit={this.handleSubmit}>
            <input className="input_text" type="text" value={this.state.value} onChange={this.handleChange} autoComplete="off"></input>
            <input className="input_submit" type="submit" value="Send"></input>
          </form>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <ClientConsole />,
  document.getElementById('console')
);