"use strict";

function asdf() {

}

function showRepoCount(username) {

    var request = new XMLHttpRequest();
    request.onload = function () {

        console.log(this);
        console.log(this.responseText);

        var responseObj = JSON.parse(this.responseText);
        window.alert(responseObj.name + " has " + responseObj.public_repos + " public repositories!");
    };

    request.open('get', 'https://api.github.com/users/' + username, true)
    request.send();
// => Giovanni Funchal has 8 public repositories!


}

