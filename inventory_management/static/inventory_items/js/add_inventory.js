$(document).ready(function(){

  $('.show-items').on('click', showInventoryItemList);

});

function showInventoryItemList(){
  let itemSelected = $(this).children().text()
  window.location.replace('/inventory/list_inventory/'+itemSelected)
}

