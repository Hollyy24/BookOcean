window.addEventListener("DOMContentLoaded", function () {
    const model = new Model()
    const view = new View()
    const controller = new Controller(model, view)

})


class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;
        this.init()


        this.view.homePage.addEventListener("click", () => {
            window.location.href = "/"
        })

        this.view.logOut.addEventListener("click", () => {
            this.model.userLogout();
            window.location.href = "/";

        })


    }

    async init() {
        let token = localStorage.getItem('token');
        if (!token) {
            window.location.href = "/";
        }

        const result = await this.model.getCollection();
        if (result["success"] == false) {
            this.view.personalCollection.textContent = "尚無收藏書籍"
            return
        }
        this.view.createCollect(result["data"])
        return
    }
}

class Model {
    async getCollection() {
        try {
            let token = localStorage.getItem('token')
            const response = await fetch('/api/collectbook', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': `Bearer ${token}`,
                }
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }


    userLogout() {
        let token = localStorage.getItem('token');
        localStorage.removeItem('token');
    }
}


class View {
    constructor() {
        this.homePage = document.querySelector('#nav-title');
        this.logOut = document.querySelector('#logout');
        this.profile = document.querySelector("#profile");
        this.personalCollection = document.querySelector("#personal-collection");

    }

    createCollect(data) {
        for (let index in data) {

            this.personalCollection.innerHTML = "";
            let collectContainer = document.createElement("div");
            let bookName = document.createElement("p");
            let bookImg = document.createElement("img");
            let bookAuthor = document.createElement("p");
            let bookPrice = document.createElement("p");
            let bookUrl = document.createElement("a");

            collectContainer.className = "collect-container";
            bookName.className = "collecct-name";
            bookImg.className = "collect-img";
            bookAuthor.className = "collect-author";
            bookPrice.className = "collect-price";
            bookUrl.className = "collect-url";

            collectContainer.id = data[index].id;
            bookName.textContent = data[index].book_name;
            bookImg.src = data[index].book_img_url;
            bookAuthor.textContent = data[index].book_author;
            bookPrice.textContent = data[index].book_price;
            bookUrl.href = data[index].book_url;

            collectContainer.appendChild(bookName);
            collectContainer.appendChild(bookImg);
            collectContainer.appendChild(bookAuthor);
            collectContainer.appendChild(bookPrice);
            collectContainer.appendChild(bookUrl);

            this.personalCollection.appendChild(collectContainer);
        }
    }
}




