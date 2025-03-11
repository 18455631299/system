document.addEventListener('DOMContentLoaded', function() {
  // Initialize Flatpickr for date/time pickers
  flatpickr("#start_date", {
    enableTime: true,
    time_24hr: true,
    dateFormat: "Y-m-d H:i",
    defaultDate: new Date(),
    minuteIncrement: 1
  });
  
  flatpickr("#end_date", {
    enableTime: true,
    time_24hr: true,
    dateFormat: "Y-m-d H:i",
    defaultDate: new Date(),
    minuteIncrement: 1
  });

  // Flash messages auto-hide
  const flashMessages = document.querySelectorAll('.alert');
  flashMessages.forEach(message => {
    setTimeout(() => {
      message.classList.add('fade');
      setTimeout(() => {
        message.remove();
      }, 500);
    }, 3000);
  });
});
