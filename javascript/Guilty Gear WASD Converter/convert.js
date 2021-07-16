// Guilty Gear:Strive convert weird "conventional" control notation to Default WASD Keyboard
// Because I'm too lazy to use numpad or mentally convert :3

/*
7 8 9 
4 5 6
1 2 3
*/

const UP = "W";
const LEFT = "A";
const DOWN = "S";
const RIGHT = "D";

const PUNCH = "U";
const KICK = "J";
const SLASH = "I";
const HEAVYSLASH = "K";

const DUST = "O";

const DASH = "Q";
const ROMANCANCEL = "E"; //custom, added by me
const PSYCHBURST = "R"; //custom, added by me

const keymap = {
    "1": LEFT + DOWN,
    "2": DOWN,
    "3": RIGHT + DOWN,

    "4": LEFT,
    "5": "",
    "6": RIGHT,

    "7": LEFT + UP,
    "8": UP,
    "9": RIGHT + UP,

    "P": PUNCH,
    "K": KICK,
    "S": SLASH,
    "H": HEAVYSLASH,
    "D": DUST,

};

function convert_combostring(combostring) {
    ret = "";

    console.log(combostring);

    for (let char of combostring) {
        if (char in keymap) {
            let converted = keymap[char];

            if (converted != "") { //not empty, i.e. "5" (neutral position)
                ret += "[" + converted + "]";
            }
        }
        else {
            console.log("Not converting '" + char + "' as it is not in keymap...");
            ret += char;
        }
    }

    return ret;

}
