// src/SearchForm.js
import React, { useState } from 'react';
import axios from 'axios';

const SearchForm = () => {
  const [name, setName] = useState('');
  const [flightId, setFlightId] = useState('');
  const [passengerId, setPassengerId] = useState('');
  const [eligibilityStatus, setEligibilityStatus] = useState('');

  const handleSearch = async () => {
    if (!name && !flightId && !passengerId) {
      setEligibilityStatus('Please fill out at least one search field.');
      return;
    }

    const searchData = { name, flightId, passengerId };

    try {
      const response = await axios.post('http://localhost:5000/search', searchData);
      if (response.data.isEligible) {
        setEligibilityStatus('Eligible for insurance claim.');
      } else {
        setEligibilityStatus('Not eligible for insurance claim.');
      }
    } catch (error) {
      setEligibilityStatus('Error during search, please try again.');
      console.error(error);
    }
  };

  return (
    <div>
      <h3>Input Record to Search</h3>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="text"
        placeholder="Flight #"
        value={flightId}
        onChange={(e) => setFlightId(e.target.value)}
      />
      <input
        type="text"
        placeholder="Passenger ID"
        value={passengerId}
        onChange={(e) => setPassengerId(e.target.value)}
      />
      <button onClick={handleSearch}>Check Eligibility</button>
      <p>{eligibilityStatus}</p>
    </div>
  );
};

export default SearchForm;
