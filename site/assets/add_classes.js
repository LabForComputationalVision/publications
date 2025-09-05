$.when( $.ready ).then(function() {
    const group_headers = $("h2.bibliography")
    var group_headers_text = group_headers.map(function() {
        return $.trim($(this).text());
    }).get()
    group_headers_text = group_headers_text.map(function(e) {
        return "<a href='#"+ e +"'>" + e + "</a>"
    })
    group_headers.parent().before(
        "<div id=links>"+ group_headers_text.join(" | ") +"</div>"
    )
    group_headers.wrap(function() {
        return "<div id='divider'><div id='divider-left'><a class='divider' name='" + $(this).text() + "'></a></div><div id='divider-right'><a class='divider' href='#pagetitle'>top</a></div></div>"
    })
    group_headers.each(function() {$(this).replaceWith($(this).text())})
})
