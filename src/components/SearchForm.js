// SearchForm.js
import React, { useState } from 'react';
import axios from 'axios';

const SearchForm = () => {
  const [name, setName] = useState('');
  const [flightId, setFlightId] = useState('');
  const [passengerId, setPassengerId] = useState('');
  const [eligibilityStatus, setEligibilityStatus] = useState('');
  const [isChecking, setIsChecking] = useState(false);

  const handleSearch = async () => {
    if (!name && !flightId && !passengerId) {
      setEligibilityStatus('Please fill out at least one search field.');
      return;
    }

    const searchData = { name, flightId, passengerId };

    try {
      setIsChecking(true);
      setEligibilityStatus('Checking eligibility...');
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const response = await axios.post('http://localhost:5000/search', searchData);
      
      if (response.data.isEligible) {
        setEligibilityStatus('Passenger is ELIGIBLE for insurance claim! ✅');
      } else {
        setEligibilityStatus('Passenger is NOT ELIGIBLE for insurance claim. ❌');
      }
    } catch (error) {
      setEligibilityStatus('Error during search. Please try again.');
      console.error(error);
    } finally {
      setIsChecking(false);
    }
  };

  const getEligibilityClass = () => {
    if (eligibilityStatus.includes('ELIGIBLE')) return 'status-success';
    if (eligibilityStatus.includes('NOT ELIGIBLE') || eligibilityStatus.includes('Error')) return 'status-error';
    if (eligibilityStatus.includes('Please fill')) return 'status-info';
    if (eligibilityStatus.includes('Checking')) return 'status-processing';
    return 'status-info';
  };

  const clearForm = () => {
    setName('');
    setFlightId('');
    setPassengerId('');
    setEligibilityStatus('');
  };

  return (
    <div className="search-section">
      <h3>INPUT RECORD TO SEARCH</h3>
      <div className="search-grid">
        <div className="input-group">
          <label htmlFor="name">Name:</label>
          <input
            id="name"
            type="text"
            placeholder="Enter passenger name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={isChecking}
          />
        </div>
        
        <div className="input-group">
          <label htmlFor="flightId">Flight #:</label>
          <input
            id="flightId"
            type="text"
            placeholder="Enter flight number"
            value={flightId}
            onChange={(e) => setFlightId(e.target.value)}
            disabled={isChecking}
          />
        </div>
        
        <div className="input-group">
          <label htmlFor="passengerId">Passenger ID:</label>
          <input
            id="passengerId"
            type="text"
            placeholder="Enter passenger ID"
            value={passengerId}
            onChange={(e) => setPassengerId(e.target.value)}
            disabled={isChecking}
          />
        </div>
      </div>
      
      <div style={{ display: 'flex', gap: '15px', justifyContent: 'center' }}>
        <button 
          className="check-btn" 
          onClick={handleSearch}
          disabled={isChecking}
        >
          {isChecking ? 'Checking...' : 'Check Eligibility'}
        </button>
        <button 
          className="check-btn"
          onClick={clearForm}
          disabled={isChecking}
          style={{ background: 'linear-gradient(90deg, #718096, #4a5568)' }}
        >
          Clear
        </button>
      </div>
      
      {eligibilityStatus && (
        <div className={`status-message ${getEligibilityClass()} ${isChecking ? 'processing' : ''}`}>
          {eligibilityStatus}
        </div>
      )}
    </div>
  );
};

export default SearchForm;