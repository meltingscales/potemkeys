"use strict";

let list = [1, 2, 3, 4, 5];

function double_number(x) {
    return x * 2;
}

console.log(list); // Gives [1,2,3,4,5]
console.log(list.map(double_number)); // Gives [2,4,6,8,10]