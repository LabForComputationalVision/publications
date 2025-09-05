$.when( $.ready ).then(function() {
  if ($("#bibliography-year").length) {
    $("input#radio-year").prop('checked', true)
  } else if ($("#bibliography-type").length) {
    $("input#radio-type").prop('checked', true)
  } else if ($("#bibliography-author").length) {
    $("input#radio-author").prop('checked', true)
  }
})
