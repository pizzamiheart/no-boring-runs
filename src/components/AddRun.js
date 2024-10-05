import React, { useState } from 'react';

function AddRun() {
  const [distance, setDistance] = useState('');
  const [date, setDate] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Implement add run logic
    console.log('Add run:', distance, date);
  };

  return (
    <div>
      <h2>Add New Run</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Distance (miles)"
          value={distance}
          onChange={(e) => setDistance(e.target.value)}
          step="0.1"
          min="0.1"
        />
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          max={new Date().toISOString().split('T')[0]}
        />
        <button type="submit">Save Run</button>
      </form>
    </div>
  );
}

export default AddRun;
