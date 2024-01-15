// Add squares
const squares = document.querySelector('.squares');
for (var i = 1; i < 365; i++) {
  const level = Math.floor(Math.random() * 3);  
  squares.insertAdjacentHTML('beforeend', `<li data-level="${level}"></li>`);
}

// Fetch dates 
fetch('/questions')
  .then(response => response.json())
  .then(dates => {

    dates.forEach(date => {
      const square = document.createElement('li');
    
      squaresList.appendChild(square);
    });

  });

// Handle date click
function handleDateClick(date) {

  // Fetch question 
  fetch(`/questions/${date}`) 
    .then(response => response.json())
    .then(question => {
      // Display question 
      console.log(question);
    });

}