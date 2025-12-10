// FileUpload.js
import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setStatus(`Selected: ${selectedFile.name}`);
  };

  const handleFileUpload = async () => {
    if (!file) {
      setStatus('Please choose a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setIsProcessing(true);
      setStatus('Processing file... (TRANSFORM)');
      
      // Simulate processing delay for better UX
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      setStatus('File processed successfully!');
      console.log(response.data);
      
      // Reset file input
      document.querySelector('input[type="file"]').value = '';
      setFile(null);
    } catch (error) {
      setStatus('File upload failed. Please try again.');
      console.error(error);
    } finally {
      setIsProcessing(false);
    }
  };

  const getStatusClass = () => {
    if (status.includes('success')) return 'status-success';
    if (status.includes('failed') || status.includes('Please choose')) return 'status-error';
    if (status.includes('Processing')) return 'status-processing';
    if (status.includes('Selected:')) return 'status-info';
    return 'status-info';
  };

  return (
    <div className="upload-section">
      <h3>PLEASE SELECT FILE TO UPLOAD</h3>
      <div className="file-input-container">
        <label className="custom-file-input">
          Choose File
          <input 
            type="file" 
            accept=".csv,.txt" 
            onChange={handleFileChange} 
            disabled={isProcessing}
          />
        </label>
        {file && <span className="file-name">{file.name}</span>}
        <button 
          className="upload-btn" 
          onClick={handleFileUpload}
          disabled={isProcessing}
        >
          {isProcessing ? 'Processing...' : 'Upload'}
        </button>
      </div>
      {status && (
        <div className={`status-message ${getStatusClass()} ${isProcessing ? 'processing' : ''}`}>
          {status}
        </div>
      )}
    </div>
  );
};

export default FileUpload;