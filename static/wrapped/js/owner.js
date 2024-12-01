const visibility = document.getElementById("visibility")
const visibilityText = document.getElementById("visibilityText")

visibility.checked = isPublic
visibilityText.innerText = isPublic ? 'Public' : 'Private'

const extraContainer = document.getElementsByClassName("extra-visibility")
const extraVisibility = document.getElementById("extraVisibility")

function updateModal() {
    for (let extra of extraContainer) {
        if (isPublic) {
            extra.classList.add('hidden')
        } else {
            extra.classList.remove('hidden')
        }
    }
}

visibility.addEventListener('change', async (e) => {
    isPublic = e.target.checked
    await changeVisibility(id, isPublic)
    visibilityText.innerText = isPublic ? 'Public' : 'Private'
    updateModal()
})

extraVisibility.addEventListener('change', async (e) => {
    visibility.click()
})

updateModal()