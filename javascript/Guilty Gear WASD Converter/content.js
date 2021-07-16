function selection() {
    return window.getSelection().toString()
}


let cs = "5K > 6S > 236K";

console.log("hello chrome :3");
console.log(cs);
console.log(convert_combostring(cs));


setTimeout(function(){ 

    console.log(convert_combostring(selection()));

}, 300);
