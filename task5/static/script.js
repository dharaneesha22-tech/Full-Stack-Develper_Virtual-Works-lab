let chart;

async function loadStats(){

let response = await fetch("/stats");
let data = await response.json();

document.getElementById("total").innerText =
data.total;

document.getElementById("available").innerText =
data.available;

document.getElementById("busy").innerText =
data.busy;

document.getElementById("health").innerText =
data.health + "%";

updateChart(data.available,data.busy);
}

async function toggleStatus(id){

let response = await fetch(
"/toggle/"+id,
{
method:"POST"
}
);

let data = await response.json();

let feed = document.getElementById("feed");

let item = document.createElement("li");

item.innerText =
"Employee status changed to " +
data.status;

feed.prepend(item);

location.reload();
}

function updateChart(av,busy){

const ctx =
document.getElementById("teamChart");

if(chart){
chart.destroy();
}

chart = new Chart(ctx,{

type:"doughnut",

data:{
labels:[
"Available",
"Busy"
],

datasets:[{
data:[av,busy]
}]
}

});
}

document
.getElementById("search")
.addEventListener("keyup",function(){

let value =
this.value.toLowerCase();

let rows =
document.querySelectorAll("tbody tr");

rows.forEach(row=>{

let text =
row.innerText.toLowerCase();

row.style.display =
text.includes(value)
?
""
:
"none";

});

});

loadStats();

setInterval(loadStats,3000);