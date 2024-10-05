import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import AddRun from './components/AddRun';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>No Boring Runs 🏃</h1>
        </header>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />
          <Route path="/dashboard" component={Dashboard} />
          <Route path="/add-run" component={AddRun} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
