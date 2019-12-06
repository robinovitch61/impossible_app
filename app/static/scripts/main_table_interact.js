let table = document.getElementById("microbe_table")

for (row = 1; row < table.rows.length; row++) {
	table.rows[row].onclick = function() {
		window.location.href += '/' + this.cells[0].innerHTML;
    };
	table.rows[row].onmouseenter = function() {
		this.style.background="lightblue";
    };
    table.rows[row].onmouseout = function() {
		this.style.background="white";
    };
};