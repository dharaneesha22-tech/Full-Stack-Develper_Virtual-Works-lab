let totalQuotes = 0;
let favorites = 0;
let xp = 0;

const quoteEl = document.getElementById("quote");
const authorEl = document.getElementById("author");

async function generateQuote(){

const res = await fetch('/get_quote');

const data = await res.json();

quoteEl.innerText = `"${data.quote}"`;

authorEl.innerText = "- " + data.author;

totalQuotes++;

xp += 10;

document.getElementById("quoteCount").innerText = totalQuotes;
document.getElementById("xp").innerText = xp;

updateLevel();

loadHistory();
}

function updateLevel(){

let level="Beginner";

if(xp>=100) level="Thinker";
if(xp>=300) level="Motivator";
if(xp>=600) level="Legend";

document.getElementById("level").innerText=level;
}

function copyQuote(){

navigator.clipboard.writeText(
quoteEl.innerText
);

alert("Copied");
}

function speakQuote(){

let speech = new SpeechSynthesisUtterance(
quoteEl.innerText
);

speechSynthesis.speak(speech);
}

async function saveFavorite(){

favorites++;

document.getElementById("favCount").innerText=favorites;

await fetch('/favorite',{
method:'POST',
headers:{
'Content-Type':'application/json'
},
body:JSON.stringify({
quote:quoteEl.innerText,
author:authorEl.innerText
})
});
}

function downloadQuote(){

let text=quoteEl.innerText+"\n"+authorEl.innerText;

let a=document.createElement("a");

a.href="data:text/plain;charset=utf-8,"+
encodeURIComponent(text);

a.download="quote.txt";

a.click();
}

async function loadHistory(){

const res = await fetch('/history');

const data = await res.json();

const list = document.getElementById("historyList");

list.innerHTML="";

data.forEach(item=>{

let li=document.createElement("li");

li.innerHTML=`${item[0]} - ${item[1]}`;

list.appendChild(li);

});
}

document.getElementById("themeBtn").onclick=()=>{

document.body.classList.toggle("light");
}

const ctx=document.getElementById('chart');

new Chart(ctx,{
type:'bar',
data:{
labels:['Viewed','Favorites','XP'],
datasets:[{
data:[10,5,50]
}]
}
});

loadHistory();