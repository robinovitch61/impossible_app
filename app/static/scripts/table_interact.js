let strain_table = document.getElementById("strain_table")
if (strain_table) {
	for (row = 1; row < strain_table.rows.length; row++) {
		strain_table.rows[row].onclick = function() {
			window.location.href = '/strain/' + this.cells[0].innerHTML;
		};
		strain_table.rows[row].onmouseenter = function() {
			this.style.background="lightblue";
		};
		strain_table.rows[row].onmouseout = function() {
			this.style.background="white";
		};
	};
};

let plasmid_table = document.getElementById("plasmid_table")
if (plasmid_table) {
	for (row = 1; row < plasmid_table.rows.length; row++) {
		plasmid_table.rows[row].onclick = function() {
			window.location.href = '/plasmid/' + this.cells[0].innerHTML;
		};
		plasmid_table.rows[row].onmouseenter = function() {
			this.style.background="lightblue";
		};
		plasmid_table.rows[row].onmouseout = function() {
			this.style.background="white";
		};
	};
};

let gene_table = document.getElementById("gene_table")
if (gene_table) {
	for (row = 1; row < gene_table.rows.length; row++) {
		gene_table.rows[row].onclick = function() {
			window.location.href = '/gene/' + this.cells[0].innerHTML;
		};
		gene_table.rows[row].onmouseenter = function() {
			this.style.background="lightblue";
		};
		gene_table.rows[row].onmouseout = function() {
			this.style.background="white";
		};
	};
};