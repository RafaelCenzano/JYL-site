$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#example tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" autocomplete="false" placeholder="'+title+'" />' );
    } );
 
    // DataTable
    var table = $('#example').DataTable({
        initComplete: function () {
            // Apply the search
            this.api().columns().every( function () {
                var that = this;
 
                $( 'input', this.footer() ).on( 'keyup change clear', function () {
                    if ( that.search() !== this.value ) {
                        that
                            .search( this.value )
                            .draw();
                    }
                } );
            } );
        }
    });

} );

function isDarkModeEnabled() {
            const siteThemeFromStorage = window.localStorage.getItem("site-theme");
            return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches && (siteThemeFromStorage !== "light")) || siteThemeFromStorage === "dark";
}
let isDarkModePreferred = isDarkModeEnabled();

let theme = isDarkModePreferred ? "dark" : "light"

if (theme === "dark") {
    var all = document.getElementsByTagName("*");
    for (var i=0, max=all.length; i < max; i++) {
        if (all[i] != null) {
            var str = String(all[i].className)
            if (str.substring(str.length - 5, str.length) == 'light'){
                all[i].className = str.substring(0, str.length - 6);
            }
        }
    }
} else {
    var all = document.getElementsByTagName("*");

    for (var i=0, max=all.length; i < max; i++) {
        if (str.substring(str.length - 5, str.length) != 'light'){
            all[i].className += " light";
        }
    }
}