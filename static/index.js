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
                this.view.renderBooksResult(result["books"])
                this.view.renderEsliteResult(result["eslite"])

                return
            }
            if (result["success"] == false) {
                const Message = result["Message"]
                alert(Message)
                return
            }
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
        this.resultEslite = document.querySelector("#result-eslite");
        this.resultBooks = document.querySelector("#result-books");

    }

    renderEsliteResult(data) {
        console.log(data);

        let content = "";
        for (let i in data) {
            const book = data[i];
            content += `${book.book_name} / ${book.book_author} / ${book.book_price}\n`;
        }

        this.resultEslite.textContent = content;
    }
    renderBooksResult(data) {
        console.log(data);

        let content = "";
        for (let i in data) {
            const book = data[i];
            content += `${book.book_name} / ${book.book_author} / ${book.book_price}\n`;
        }

        this.resultBooks.textContent = content;
    }
}   
