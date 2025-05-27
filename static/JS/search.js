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
        this.initData()

    }

    async initData() {
        const data = this.model.getQueryparameter();
        const result = await this.model.fetchData(data);
        if (result == false) {
            alert("發生錯誤，請重新查詢")
            window.location.href = '/'
        }
        if (result["books"].length === 0) {
            this.view.bookText.textContent = "查無相關資料";
            return
        }
        const books = result["books"];
        for (let index in books) {
            this.view.createContent(books[index]);
        }

    }
    init() {

        let token = localStorage.getItem('token');
        if (token) {
            this.view.memberCenter.style.display = "block"
            this.view.login.style.display = "none";
            this.view.signin.style.display = "none";

        }
    }
}

class Model {
    getQueryparameter() {
        const parameter = new URLSearchParams(window.location.search);
        const way = parameter.get('way');
        const value = parameter.get('value');
        const data = {
            "way": way,
            "value": value
        }
        return data
    }


    async fetchData(searchvalue) {
        try {
            const response = await fetch('/api/booksdata', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(searchvalue)
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Fetch error:", error);
            return false
        }
    }


    async addCollection(book_id) {
        const data = {
            "user_id": localStorage.getItem('token'),
            "book_id": book_id
        }
        try {
            const response = await fetch('api/collectbook', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem('token')
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (result["success"] == true) {
                alert("收藏成功");
            }
            if (result["success"] == false) {
                alert("收藏失敗");
            }
            ;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

}




class View {
    constructor() {
        this.bookText = document.querySelector("#book-text");


    }


    sourceColor(source) {
        if (source == "博客來") {
            return "#7ABD54"
        }
        if (source == "誠品") {
            return "#A50034"
        }
    }

    createContent(data) {
        const container = document.querySelector('#result-container');

        let bookItem = document.createElement("div");
        let bookName = document.createElement("h3");
        let bookImg = document.createElement("img");
        let bookAuthor = document.createElement("p");
        let bookPrice = document.createElement("p");
        let bookSource = document.createElement('p');
        let urlContainer = document.createElement("div");
        let bookUrl = document.createElement("a");
        let collectButton = document.createElement("a");

        bookItem.className = "book-item";
        bookName.className = "book-name";
        bookImg.className = "book-img";
        bookAuthor.className = "book-author";
        bookPrice.className = "book-price";
        bookSource.className = 'book-source';
        bookUrl.className = 'book-url';
        bookUrl.target = "_blank";
        urlContainer.className = "url-container";
        collectButton.className = "collect-button";

        bookItem.title = data.name
        bookName.textContent = data.name;
        bookImg.src = data.img;
        bookAuthor.textContent = data.author;
        bookPrice.textContent = data.price + " 元";
        bookSource.textContent = data.source;
        bookSource.style.backgroundColor = this.sourceColor(data.source);
        bookUrl.textContent = "前往購買";
        bookUrl.href = data.url;
        collectButton.textContent = "加入收藏";
        collectButton.id = data.id;



        bookItem.appendChild(bookName);
        bookItem.appendChild(bookImg);
        bookItem.appendChild(bookAuthor);
        bookItem.appendChild(bookPrice);
        bookItem.appendChild(bookSource);
        bookItem.appendChild(urlContainer);
        urlContainer.appendChild(bookUrl);
        urlContainer.appendChild(collectButton);
        container.appendChild(bookItem)

    }

    setCollectButton() {
        const collectButton = document.querySelectorAll('.collect-book');
        return collectButton
    }
}




