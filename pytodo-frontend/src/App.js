import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { List } from './List';

function App() {
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchLists = async () => {
    try {
      const response = await Axios.get('/v1/lists');
      setLists(response.data.lists);
      setLoading(false);
    } catch (err) {
      setError(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLists();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1 className="App-title">PyTodo</h1>
      </header>
      {error && (
        <div className="error-message">
          Failed to fetch lists: {error.message}
        </div>
      )}
      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <List lists={lists} />
      )}
    </div>
  );
}

export default App;
