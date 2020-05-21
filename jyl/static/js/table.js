$(document).ready(function () {
$('#selectedColumn').DataTable({
  "aaSorting": [],
  columnDefs: [{
  orderable: false,
  targets: 3
  },{
  orderable: false,
  targets: 5
  }]
});
  $('.dataTables_length').addClass('bs-select');
});