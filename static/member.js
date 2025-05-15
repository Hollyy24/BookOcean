window.addEventListener("DOMContentLoaded", function () {
    const model = new Model()
    const view = new View()
    const controller = new Controller(model, view)

})


class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;


        let token = localStorage.getItem('token');
        if (!token) {
            window.location.href = "/";
        }

        this.view.logOut.addEventListener("click", () => {
            this.model.userLogout();
            window.location.href = "/";

        })
    }
}

class Model {
    async gerCollection() {
    }
    userLogout() {
        let token = localStorage.getItem('token');
        localStorage.removeItem('token');
    }
}


class View {
    constructor() {
        this.logOut = document.querySelector('#logout')
        this.profile = document.querySelector("#profile");
        this.personalCollection = document.querySelector("#personal-collection");

    }
}




