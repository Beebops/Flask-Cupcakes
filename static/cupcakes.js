const baseURL = 'http://localhost:5000/api'

async function showCupcakes() {
  const response = await axios.get(`${baseURL}/cupcakes`)
  console.log(response.data.cupcakes)
  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(createCupcakeHTML(cupcakeData))
    $('#cupcakes-list').append(newCupcake)
  }
}

// generate the HTML for all the cupcakes
function createCupcakeHTML(cupcake) {
  return `
      <li class="list-group-item" data-id="${cupcake.id}">
      ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
      <button class="btn btn-danger">Delete</button>
      </li>
      <img class="cupcake-image" src="${cupcake.image}">
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

$(showCupcakes)

// on page load, await the response from /api/cupcakes route and use the json that gets returned from that function to render the list of cupcakes in the database

// // response -> {cupcakes: [{id, flavor, rating, size, image}, ...]}
