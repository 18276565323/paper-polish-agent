const backTop = document.querySelector('.back-top')

function updateBackTop() {
  backTop.classList.toggle('visible', window.scrollY > 520)
}

backTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

window.addEventListener('scroll', updateBackTop, { passive: true })
updateBackTop()
