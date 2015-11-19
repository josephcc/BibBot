import React from 'react';
import {Router} from 'director';

import MainPage from './pages/main_page.jsx';


var PAGE_MAIN = "_ROUTE_PAGE_MAIN_";

export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    var router = Router({
      '/': function() {
		  this.setState({page: PAGE_MAIN});
	  }.bind(this),
    });
    router.init("/");
  }

  getPage() {
    switch (this.state.page) {
      case PAGE_MAIN:
        return (<MainPage></MainPage>);
        break;
      case "":
        return (<div></div>);
        break;
      default:
        return (<div>404 Page Not Found: { this.state.page }</div>);
        break;
    }
  }

  componentDidUpdate() {
  }

  render() {
    return (
      <div id='page'>
        { this.getPage() }
      </div>
    );
  }

}

React.render(<App/>, document.body);

