import React from 'react';
import Survey from './components/Survey'
import Status from './components/Status'
import Services from './components/Services'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import './App.css'

const App = () => {

  return(
    <div className='resp-wrapper'>
    <div className="d-flex justify-content-center">
      <h1 className="display-3">R. E. S. P.</h1>
      </div>

    <div className="resp-options">

    <Router>
      <div>
            <Survey/>
            <Link to="/status">
            <button type="button" className="btn btn-outline-primary">STATUS</button>
              </Link>
            <Link to="/services">
              <button type="button" className="btn btn-outline-primary">SERVICES</button>
                </Link>
      </div>
        <Route path="/status" component={Status} />
        <Route path="/services" component={Services} />
    </Router>
    </div>
    </div>
  )
}

export default App;
