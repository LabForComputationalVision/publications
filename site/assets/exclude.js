function toggle_visibility(element) {
  var selected = $("input:checkbox")
      .map(function() {
        if ($(this).prop('checked')){return this.id}
      }).get().join(',.')
  $("ol.bibliography > div").show()
  $("." + selected).hide()
}
