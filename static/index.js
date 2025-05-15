window.addEventListener("DOMContentLoaded", function () {
    const model = new Model()
    const view = new View()
    const controller = new Controller(model, view)

})

console.log("rrrrrr")

class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;

        this.view.searchButton.addEventListener("click", async (event) => {
            event.preventDefault()
            console.log("here")
            const bookName = this.view.searchInput.value
            const result = await this.model.fetchData(bookName);
            if (result["success"] == true) {
                console.log("ok")
                if (result["books"]) {
                    this.view.renderResult(result["books"], this.view.bookContainer)
                }
                if (result["eslite"]) {
                    console.log("誠品")
                    this.view.renderResult(result["eslite"], this.view.esliteContainer)
                }

            }
            if (result["success"] == false) {
                const Message = result["Message"]
                alert(Message)
                return
            }
            return
        })

    }


}

class Model {
    async fetchData(bookName) {
        try {
            const response = await fetch('/api/booksdata', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "name": bookName })
            });
            const data = await response.json();
            console.log(data)
            return data;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }


}


class View {
    constructor() {
        this.searchForm = document.querySelector("#searchForm");
        this.searchInput = document.querySelector("#search-input");
        this.searchButton = document.querySelector("#search-button");
        this.bookContainer = document.querySelector(".book-container");
        this.bookContainer = document.querySelector("#bookshop-container")
        this.esliteContainer = document.querySelector("#eslite-container")


    }


    renderResult(arry, container) {
        container.innerHTML = "";
        for (let i in arry) {
            this.createContent(arry[i], container)
        }
    }




    createContent(data, container) {

        let bookItem = document.createElement("div");
        let bookName = document.createElement("h2");
        let bookImg = document.createElement("img");
        let bookAuthor = document.createElement("p");
        let bookPrice = document.createElement("p");

        bookItem.className = "book-item";
        bookName.className = "book-name";
        bookImg.className = "book-img";
        bookAuthor.className = "book-author";
        bookPrice.className = "book-price";

        bookName.textContent = data.book_name;
        bookImg.src = "#";
        bookAuthor.textContent = data.book_author;
        bookPrice.textContent = data.book_price;

        bookItem.appendChild(bookName);
        bookItem.appendChild(bookImg);
        bookItem.appendChild(bookAuthor);
        bookItem.appendChild(bookPrice);

        container.appendChild(bookItem);

    }
}
