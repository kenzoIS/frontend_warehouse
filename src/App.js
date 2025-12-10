// src/App.js
import React from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import SearchForm from './components/SearchForm';

function App() {
  return (
    <div className="App">
      <h1>Passenger Insurance Claim System</h1>
      <FileUpload />
      <div className="separator"></div>
      <SearchForm />
      <div style={{ 
        textAlign: 'center', 
        marginTop: '30px', 
        color: '#718096',
        fontSize: '0.9rem',
        fontStyle: 'italic'
      }}>
        <p>Connected to Kafka Stream | Data Processing System v1.0</p>
      </div>
    </div>
  );
}

export default App;