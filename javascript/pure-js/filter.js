'use strict';

let list = [1, 2, 3, 4, 5];

function is_odd(number) {
    if (number % 2 === 1) {
        return true;
    } else {
        return false;
    }
}

console.log(list); // Gives [1,2,3,4,5]
console.log(list.filter(is_odd)); // Gives [1,3,5]
