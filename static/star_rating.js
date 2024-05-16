document.addEventListener('DOMContentLoaded', function() {
    const starRatingElements = document.querySelectorAll('.star-rating');

    starRatingElements.forEach(function(element) {
        let rating = parseInt(element.dataset.rating);

        for (let i = 1; i <= 5; i++) {
            const starIcon = document.createElement('i');
            starIcon.classList.add('fas', 'fa-star');

            if (i <= rating) {
                starIcon.classList.add('rated');
            }

            starIcon.addEventListener('mouseover', function() {
                highlightStars(element, i);
            });

            starIcon.addEventListener('mouseout', function() {
                highlightStars(element, rating);
            });

            starIcon.addEventListener('click', function() {
                rating = i;
                highlightStars(element, rating);
                setRatingInput(element, rating);
            });

            element.appendChild(starIcon);
        }
    });
});

function highlightStars(element, rating) {
    const starIcons = element.querySelectorAll('.fa-star');

    starIcons.forEach(function(starIcon, index) {
        if (index < rating) {
            starIcon.classList.add('rated');
        } else {
            starIcon.classList.remove('rated');
        }
    });
}

function setRatingInput(element, rating) {
    const form = element.closest('form');
    const ratingInput = form.querySelector('#rating');

    if (!ratingInput) {
        const newRatingInput = document.createElement('input');
        newRatingInput.type = 'hidden';
        newRatingInput.name = 'rating';
        newRatingInput.id = 'rating';
        form.appendChild(newRatingInput);
        ratingInput = newRatingInput;
    }

    ratingInput.value = rating;
}