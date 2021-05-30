

// const socket = io("ws://localhost:5000");
const socket = io({secure: true});
// var socket = io();
socket.on('connect', function() {
    console.log("Connected to the server\n")
    socket.emit('join', {});
    socket.emit('send messages',{});
});
socket.on('open store',function(json) {
    console.log(json);
});
socket.on('close store',function(json) {
    console.log(json);
});
socket.on('remove employee',function(json) {
    console.log(json);
    togglePopup(json);
});
socket.on('buying product',function(json) {
    console.log(json);
    togglePopup(json)
});

socket.on('message',function(json) {
    console.log(json);
});
socket.on('close',function() {
    console.log("close connection");
    emit('close',{})
});

function togglePopup(){
    document.getElementById("popup-1").classList.toggle("active");
}

function togglePopup(data){
    document.getElementById("popup-1").classList.toggle("active");
    document.getElementById("data").innerHTML = data;
}