const ROWS = 18
const COLS = 24

let grid = Array(ROWS).fill().map(()=>Array(COLS).fill(0))

let start = [4,4]
let goal = [13,19]

let isDrawing=false

function init(){

const gridDiv = document.getElementById("grid")

for(let r=0;r<ROWS;r++){

for(let c=0;c<COLS;c++){

let cell=document.createElement("div")

cell.className="cell"

cell.id=`cell-${r}-${c}`

cell.onmousedown=()=>{

isDrawing=true
toggleWall(r,c)

}

cell.onmouseover=()=>{

if(isDrawing) toggleWall(r,c)

}

cell.onmouseup=()=>{

isDrawing=false

}

gridDiv.appendChild(cell)

}

}

updateUI()

}

function toggleWall(r,c){

if((r==start[0]&&c==start[1])||(r==goal[0]&&c==goal[1])) return

grid[r][c]=grid[r][c]==0?1:0

document.getElementById(`cell-${r}-${c}`).classList.toggle("wall")

}

function updateUI(){

document.getElementById(`cell-${start[0]}-${start[1]}`).classList.add("start")

document.getElementById(`cell-${goal[0]}-${goal[1]}`).classList.add("goal")

}

async function solve(){

const algo=document.getElementById("algo").value

const res=await fetch("/solve",{

method:"POST",
headers:{"Content-Type":"application/json"},

body:JSON.stringify({

grid,
start,
goal,
algorithm:algo

})

})

const data=await res.json()

document.getElementById("stats").innerText=`Time: ${data.time}`

data.visited.forEach((n,i)=>{

setTimeout(()=>{

let cell=document.getElementById(`cell-${n[0]}-${n[1]}`)

if(!cell.classList.contains("start")&&!cell.classList.contains("goal"))

cell.classList.add("visited")

if(i===data.visited.length-1) animatePath(data.path)

},i*10)

})

}

function animatePath(path){

path.forEach((n,i)=>{

setTimeout(()=>{

document.getElementById(`cell-${n[0]}-${n[1]}`).classList.add("path")

},i*30)

})

}

function generateMaze(){

for(let r=0;r<ROWS;r++){

for(let c=0;c<COLS;c++){

if(Math.random()<0.25) toggleWall(r,c)

}

}

}

init()
