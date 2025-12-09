// src/App.js
import React from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import SearchForm from './components/SearchForm';

function App() {
  return (
    <div className="App">
      <h1>Passenger Insurance Claim</h1>
      <FileUpload />
      <SearchForm />
    </div>
  );
}

export default App;
