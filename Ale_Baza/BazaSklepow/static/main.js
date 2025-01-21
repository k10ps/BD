function updateRangeValue(id, value) {
    // Zaktualizuj wartość w odpowiednim elemencie <span>
    document.getElementById(id + '_value').textContent = value;
  }
  
  // Funkcja uruchamiana po załadowaniu strony, ustawiająca wartości początkowe
  document.addEventListener('DOMContentLoaded', function() {
    updateRangeValue(id, document.getElementById(id).value);
  });