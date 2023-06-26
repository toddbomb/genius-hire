import React, { useEffect, useState, useRef } from 'react';

function ButtonCarousel() {
  const [buttonData, setButtonData] = useState([]);
  const buttonContainerRef = useRef(null);

  useEffect(() => {
    fetchDataFromBackend().then((data) => {
      setButtonData(data);
    }).catch((error) => {
      console.error('Error:', error);
      // Handle the error
    });
  }, []);

  useEffect(() => {
    startButtonCarousel();
  }, [buttonData]);

  const startButtonCarousel = () => {
    const buttonContainer = buttonContainerRef.current;
    if (buttonContainer) {
      const buttonsWidth = buttonContainer.scrollWidth;
      const carouselWidth = buttonContainer.offsetWidth;

      if (buttonsWidth > carouselWidth) {
        const animationDuration = buttonsWidth / 100; // Adjust the value to control the carousel speed
        buttonContainer.style.animation = `carousel-animation ${animationDuration}s steps(1, end) infinite`;
      } else {
        buttonContainer.style.animation = 'none';
      }
    }
  };

  const fetchDataFromBackend = async () => {
    // Replace this with your actual API call or function to fetch the button data from the backend
    // Example: const response = await fetch('http://your-api-endpoint');
    // Parse the response and return the button data
    // Example: const data = await response.json();
    // return data;

    // For now, let's use a mock data array
    const initialData = [
      { id: 1, text: 'What candidates have the most skills related to the job description?' },
      { id: 2, text: 'List candidates with leadership experience.' },
      { id: 3, text: 'What candidates have worked in react.js?' },
      { id: 4, text: 'Generate a framework for evaluating candidates during interview.' },
    ];

    // Create a new array with the first element moved to the end
    const updatedData = [...initialData.slice(1), initialData[0]];

    return updatedData;
  };

  const handleButtonClick = async (buttonText) => {
    const data = { buttonText };
    const json = JSON.stringify(data);

    try {
      const response = await fetch('http://127.0.0.1:5000/chat/', {
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
  };

  return (
    <div className="flex items-center justify-center">
      <div className="w-full overflow-x-auto">
        <div className="flex items-center justify-between px-4" ref={buttonContainerRef}>
          {buttonData.map((button) => (
            <button
              key={button.id}
              className="px-4 py-2 rounded-lg hover:bg-[#E0A0D4] hover:bg-opacity-80 hover:text-[#252425] mr-4 border font-semibold border-[#181818] border-1"
              onClick={() => handleButtonClick(button.text)}
            >
              {button.text}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ButtonCarousel;
