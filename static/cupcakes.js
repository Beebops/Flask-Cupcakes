const baseURL = 'http://localhost:5000/api'

// on page load, await the response from /api/cupcakes route and use the json that gets returned from that function to render the list of cupcakes in the database

async function showCupcakes() {
  const response = await axios.get(`${baseURL}/cupcakes`)
  // response.data.cupcakes --> {cupcakes: [{id, flavor, rating, size, image}, ...]}
  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(createCupcakeHTML(cupcakeData))
    $('#cupcakes-list').append(newCupcake)
  }
}

// generate the HTML for all the cupcakes
function createCupcakeHTML(cupcake) {
  return `
    <div data-id="${cupcake.id}" class="container mb-4 text-center">
        <li class="list-group-item">
        ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
          <button id="delete-btn" class="btn btn-danger ms-4">Delete</button>
        </li>
      <img class="cupcake-image" src="${cupcake.image}">
    </div>  
  `
}

//handle form submit to add a new cupcake
$('#new-cupcake-form').on('submit', async function (e) {
  e.preventDefault()

  let flavor = $('#flavor').val()
  let size = $('#size').val()
  let rating = $('#rating').val()
  let image = $('#image').val()

  const newCupcakeRes = await axios.post(`${baseURL}/cupcakes`, {
    flavor,
    size,
    rating,
    image,
  })

  let newCupcake = $(createCupcakeHTML(newCupcakeRes.data.cupcake))
  $('#cupcakes-list').append(newCupcake)
  $('#new-cupcake-form').trigger('reset')
})

/** handle clicking delete to remove cupcake */
$('#cupcakes-list').on('click', '.btn-danger', async function (e) {
  e.preventDefault()
  let $cupcake = $(e.target).closest('div')
  console.log($cupcake)
  let cupcakeId = $cupcake.attr('data-id')

  await axios.delete(`${baseURL}/cupcakes/${cupcakeId}`)
  $cupcake.remove()
})

$(showCupcakes)
