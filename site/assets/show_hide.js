function show_hide() {
  $("#bibtex").toggle()
  if ($("#showhide").text() == "[show]") {
    $("#showhide").text("[hide]")
  } else {
    $("#showhide").text("[show]")
  }
}
