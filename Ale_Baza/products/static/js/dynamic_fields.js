(function($) {
    $(document).ready(function() {
        function toggleFields() {
            var selectedCategory = $('#id_kategoria').val();

            // Ukryj wszystkie pola specyfikacji
            $('.spec-telewizor, .spec-komputer, .spec-monitor').closest('.form-row').hide();

            // Pokaż odpowiednie pola w zależności od kategorii
            if (selectedCategory === 'telewizor') {
                $('.spec-telewizor').closest('.form-row').show();
            } else if (selectedCategory === 'komputer') {
                $('.spec-komputer').closest('.form-row').show();
            } else if (selectedCategory === 'monitor') {
                $('.spec-monitor').closest('.form-row').show();
            }
        }

        // Wywołaj funkcję przy zmianie kategorii
        $('#id_kategoria').on('change', toggleFields);

        // Wywołaj funkcję przy ładowaniu strony
        toggleFields();
    });
})(django.jQuery);
