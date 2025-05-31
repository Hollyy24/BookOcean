window.addEventListener("DOMContentLoaded", function () {
    const model = new Model()
    const view = new View()
    const controller = new Controller(model, view)

})


class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;

        this.init(this.view.page)
        this.view.searchButton.addEventListener("click", async (event) => {
            event.preventDefault()
            const searchWay = this.view.searchWay.value
            const searchValue = this.view.searchInput.value.trim()
            console.log(searchValue, searchWay)
            if (searchValue) {
                window.location.href = `/search/?way=${searchWay}&value=${searchValue}`;
            } else {
                alert("請輸入關鍵字");
            }
        })
        this.view.searchLeft.addEventListener("click", async () => {
            this.view.page -= 1;
            if (this.view.page < 0) {
                alert("最前頁")
                this.view.page = 0
                return
            }
            const search = this.model.getQueryparameter()
            const data = {
                "way": search.way,
                "value": search.value
            }
            const result = await this.model.fetchData(data, (this.view.page * 4))
            if (result == false) {
                alert("發生錯誤，請重新查詢")
                window.location.href = '/'
            }
            if (result["books"].length === 0) {
                this.view.bookText.textContent = "查無相關資料";
                return
            }
            const books = result["books"];
            this.view.bookContainer.textContent = ""
            for (let index in books) {
                this.view.createContent(books[index]);
            }
            document.querySelectorAll(".collect-button").forEach(button => {
                button.addEventListener("click", () => {
                    const book = button.id;
                    this.model.addCollection(book);
                });
            })

        })
        this.view.searchRight.addEventListener("click", async () => {
            this.view.page += 1;
            const search = this.model.getQueryparameter()
            const data = {
                "way": search.way,
                "value": search.value
            }
            const result = await this.model.fetchData(data, (this.view.page * 4) - 1)
            if (result == false) {
                alert("發生錯誤，請重新查詢")
                window.location.href = '/'
            }
            if (result["books"].length === 0) {
                alert("資料到底")
                return
            }
            const books = result["books"];
            this.view.bookContainer.textContent = ""
            for (let index in books) {
                this.view.createContent(books[index]);
            }
            document.querySelectorAll(".collect-button").forEach(button => {
                button.addEventListener("click", () => {
                    const book = button.id;
                    this.model.addCollection(book);
                });
            })

        })
    }



    async init(page) {
        const data = this.model.getQueryparameter();
        const result = await this.model.fetchData(data, page);
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
        document.querySelectorAll(".collect-button").forEach(button => {
            button.addEventListener("click", () => {
                const book = button.id;
                this.model.addCollection(book);
            });
        })
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


    async fetchData(searchvalue, page) {
        const search_data = {
            "way": searchvalue.way,
            "value": searchvalue.value,
            "page": page
        }
        try {
            const response = await fetch('/api/booksdata', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(search_data)
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Fetch error:", error);
            return false
        }
    }


    async addCollection(book) {
        const token = localStorage.getItem('token')
        if (!token) {
            alert("請先登入")
            return
        }
        const data = {
            "token": token,
            "book_source": book.split("/")[0],
            "book_id": book.split("/")[1]
        }
        try {
            const response = await fetch('/api/collect', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
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
        this.collectButton = document.querySelectorAll(".collect-button");
        this.searchForm = document.querySelector(".searchForm");
        this.searchWay = document.querySelector('.search-category')
        this.searchInput = document.querySelector(".search-input");
        this.searchButton = document.querySelector(".search-button");
        this.bookContainer = document.querySelector('.book-container');

        this.page = 0;
        this.searchLeft = document.querySelector("#search-left");
        this.searchRight = document.querySelector("#search-right");

    }


    sourceColor(source) {
        if (source == "博客來") {
            return "#7ABD54"
        }
        if (source == "誠品") {
            return "#A50034"
        }
        if (source == "三民") {
            return "#FFD400"
        }
    }

    createContent(data) {


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
        collectButton.id = `${data.source}/${data.id}`;

        urlContainer.appendChild(bookUrl);
        urlContainer.appendChild(collectButton)


        bookItem.appendChild(bookName);
        bookItem.appendChild(bookImg);
        bookItem.appendChild(bookAuthor);
        bookItem.appendChild(bookPrice);
        bookItem.appendChild(bookSource);
        bookItem.appendChild(urlContainer);
        this.bookContainer.append(bookItem)


    }

    setCollectButton() {
        const collectButton = document.querySelectorAll('.collect-book');
        return collectButton
    }
}




