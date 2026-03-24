const rows=18
const cols=24

let maze=[]
let start=[0,0]
let goal=[17,23]

const grid=document.getElementById("grid")

function createGrid(){

for(let r=0;r<rows;r++){

maze[r]=[]

for(let c=0;c<cols;c++){

maze[r][c]=0

let cell=document.createElement("div")
cell.className="cell"
cell.dataset.r=r
cell.dataset.c=c

cell.onclick=()=>toggleWall(cell)

grid.appendChild(cell)

}

}

paint(start,"start")
paint(goal,"goal")
}

function toggleWall(cell){

let r=cell.dataset.r
let c=cell.dataset.c

if((r==start[0] && c==start[1]) || (r==goal[0] && c==goal[1])) return

if(maze[r][c]==0){
maze[r][c]=1
cell.classList.add("wall")
}else{
maze[r][c]=0
cell.classList.remove("wall")
}
}

function paint(pos,cls){

document.querySelectorAll(".cell").forEach(c=>{
if(c.dataset.r==pos[0] && c.dataset.c==pos[1])
c.classList.add(cls)
})
}

function generateMaze(){

document.querySelectorAll(".cell").forEach(c=>{

let r=c.dataset.r
let col=c.dataset.c

if(Math.random()<0.28){

maze[r][col]=1
c.classList.add("wall")

}else{

maze[r][col]=0
c.classList.remove("wall")
}

})

paint(start,"start")
paint(goal,"goal")
}

async function solve(){

let algo=document.getElementById("algo").value

let res=await fetch("/solve",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
maze:maze,
start:start,
goal:goal,
algorithm:algo
})
})

let data=await res.json()

animate(data.visited,"visited")

setTimeout(()=>{
animate(data.path,"path")
},500)

document.getElementById("stats").innerText=
`Algorithm: ${algo} | Nodes: ${data.nodes} | Path Length: ${data.length} | Time: ${data.time}s`
}

function animate(nodes,cls){

nodes.forEach((n,i)=>{

setTimeout(()=>{

document.querySelectorAll(".cell").forEach(c=>{
if(c.dataset.r==n[0] && c.dataset.c==n[1])
c.classList.add(cls)
})

},i*15)

})
}

createGrid()