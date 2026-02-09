import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { List } from './List.js';

function App() {
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newListName, setNewListName] = useState('');

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

  const createList = async () => {
    if (!newListName.trim()) return;
    try {
      await Axios.post('/list', { name: newListName.trim() });
      setNewListName('');
      fetchLists();
    } catch (err) {
      setError(err);
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
      {/* New List Creation UI */}
      <div className="new-list-form" style={{ margin: '1rem' }}>
        <input
          type="text"
          placeholder="Enter list name"
          value={newListName}
          onChange={(e) => setNewListName(e.target.value)}
          style={{ padding: '0.5rem', marginRight: '0.5rem' }}
        />
        <button onClick={createList} style={{ padding: '0.5rem' }}>
          Create List
        </button>
      </div>
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
