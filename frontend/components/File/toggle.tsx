import React, { useState } from 'react';

function ToggleButton() {
  const [isActive, setIsActive] = useState(false);
  
  const handleToggle = async () => {
    const data = { isActive };
    const json = JSON.stringify(data);

    try {
      const response = await fetch('http://127.0.0.1:5000/active/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
          },
          body: json,
      });

      // Process the response as needed
    } catch (error) {
      console.error('Error:', error);
      // Handle the error
    }

      // Toggle the state after the API call is completed
      setIsActive(!isActive);
  };

  return (
    <button
      onClick={handleToggle}
      className={`bg-${isActive ? 'green' : 'gray'}-500 text-white px-4 py-2 rounded`}
    >
      {isActive ? 'Deactivate' : 'Activate'}
    </button>
  );
}

export default ToggleButton;