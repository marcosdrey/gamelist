const all_reviews = document.querySelectorAll('.review-block')
const btnBack = document.querySelector('.back-btn-review')
const btnNext = document.querySelector('.next-btn-review')

btnBack.addEventListener('click', ()=>{
    changeItems(-1)
})

btnNext.addEventListener('click', ()=>{
    changeItems(1)
})

function changeItems(n) {
    let shouldExit = false
    let valueToAppear = null  
    if (n === -1) {
        all_reviews.forEach(review => {
            if (!review.classList.contains('d-none')) {
                const value = Number(review.getAttribute('value'))
                review.classList.add('d-none')
                valueToAppear = value-1
                shouldExit = true
            }
            if (shouldExit) {
                return
            }
        })
        if (valueToAppear >= 0) {
            all_reviews[valueToAppear].classList.remove('d-none')
        } else {
            all_reviews[all_reviews.length-1].classList.remove('d-none')
        }
        
    } 
    else {
        all_reviews.forEach(review => {
            if (!review.classList.contains('d-none')) {
                const value = Number(review.getAttribute('value'))
                review.classList.add('d-none')
                valueToAppear = value+1
                shouldExit = true
            }
            if (shouldExit) {
                return
            }
        })
        if (valueToAppear <= all_reviews.length-1) {
            all_reviews[valueToAppear].classList.remove('d-none')
        } else {
            all_reviews[0].classList.remove('d-none')
        }
    }
}