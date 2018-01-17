$(document).ready(function(){

  $('.add-item').on('click', addInventoryItemType);
  $('.update-delete-item').on('click', updateInventoryItem);
  $('.delete-button').on('click', deleteInventoryItem);
  $('.request-inventory').on('click', requestInventory)
  $('.accept-button').on('click', acceptUserRequest)
  $('.delete-button').on('click', deleteUserRequest)
  $('.reject-button').on('click', rejectUserRequest)
  $('.update-button').on('click', updateUserRequest)

});

function addInventoryItemType(){
  let inventory_type = $(this).children().text()
  console.log(inventory_type)
  window.location.replace('/inventory/add_inventory_item/'+inventory_type)
}


function updateInventoryItem(){
  let inventory_item_name = $(this).children().text()
  window.location.replace('/inventory/update_inventory_item/'+inventory_item_name)
}

function deleteInventoryItem(){
  let inventory_item_id = $(this).children().text()
   window.location.replace('/inventory/delete_inventory_item/'+inventory_item_id)
}

function requestInventory(){
  let inventory_type_requested = $(this).children().text()
  window.location.replace('/inventory/request_inventory/'+inventory_type_requested)
}


function acceptUserRequest(){
  let inventory_mapping_id = $(this).children().text()
  window.location.replace('/inventory/assign_inventory_items/'+inventory_mapping_id)
}

function rejectUserRequest(){
  let inventory_mapping_id = $(this).children().text()
  window.location.replace('/inventory/reject_inventory_request/'+inventory_mapping_id)
}


function deleteUserRequest(){
  let inventory_mapping_id = $(this).children().text()
  window.location.replace('/inventory/delete_inventory_requested/'+inventory_mapping_id)
}

function updateUserRequest(){
  let inventory_mapping_id = $(this).children().text()
  window.location.replace('/inventory/update_inventory_requested/'+inventory_mapping_id)
}
